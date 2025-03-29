from __future__ import annotations

import asyncio
import datetime as dt
import functools
import logging
from decimal import Decimal
from typing import (
    Any,
    Awaitable,
    Callable,
    Concatenate,
    Iterable,
    Mapping,
    Self,
)

import aiohttp
import orjson
import yarl

from .account import AccountInfo, PublicAccountInfo
from .accrual import Accrual, AccrualDetalization, Accruals, MonthAccrual
from .bills import QrCodes
from .errors import (
    AccountBindingError,
    AccountNotFound,
    AuthorizationError,
    AuthorizationRequired,
    ParsingError,
    SessionRequired,
)
from .meters import MeterInfoHistory, MeterValue, PublicMeterInfo
from .parsers import parse_account, parse_accounts, parse_meters, parse_token
from .payment import Payment
from .utils import (
    data_attr,
    date_attr,
    date_last_accrual,
    date_to_str,
    str_normalize,
    str_to_date,
    to_decimal,
)

_LOGGER = logging.getLogger(__name__)

_MIN_DATE = dt.date(2018, 1, 1)
_MAX_DATE = dt.date(2099, 12, 31)

_BASE_URL = yarl.URL("https://lk.erkc63.ru")

type ClientMethod[T, **P] = Callable[Concatenate[ErkcClient, P], Awaitable[T]]


def api[T, **P](
    *,
    auth_required: bool = False,
    public: bool = False,
) -> Callable[[ClientMethod[T, P]], ClientMethod[T, P]]:
    """Декоратор методов клиента"""

    def decorator(func: ClientMethod[T, P]):
        @functools.wraps(func)
        def _wrapper(self: ErkcClient, *args: P.args, **kwargs: P.kwargs):
            if not self.opened:
                raise SessionRequired("Сессия не открыта.")

            if public:
                if self.authorized:
                    raise AuthorizationRequired(
                        "Публичный API работает без авторизации."
                    )

            elif auth_required:
                if not self.authorized:
                    raise AuthorizationRequired("Требуется авторизация.")

            return func(self, *args, **kwargs)

        return _wrapper

    return decorator


class ErkcClient:
    """Клиент личного кабинета ЕРКЦ."""

    _cli: aiohttp.ClientSession
    _login: str | None
    _password: str | None
    _token: str | None
    _accounts: tuple[int, ...] | None

    def __init__(
        self,
        login: str | None = None,
        password: str | None = None,
        *,
        session: aiohttp.ClientSession | None = None,
        auth: bool | None = None,
        close_connector: bool | None = None,
    ) -> None:
        """Инициализация клиента.

        Parameters:
            login: E-mail личного кабинета. Опционально.
            password: Пароль личного кабинета. Опционально.
            session: Внешняя клиентская сессия `aiohttp.ClientSession`. Опционально.
            auth: Авторизоваться при открытии. Если не указано, будет `True` при указании `login` and `password`.
            close_connector: Закрыть коннектор сессии при закрытии. Если не указано, будет `True` если `session` также не указан.
        """

        self._cli = session or aiohttp.ClientSession()
        self._login = login
        self._password = password
        self._accounts = None
        self._token = None
        self._auth = bool(login and password) if auth is None else auth
        self._close_connector = (
            (not session) if close_connector is None else close_connector
        )

    async def __aenter__(self) -> Self:
        try:
            await self.open()

        except Exception:
            await self.close()
            raise

        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.close()

    def __call__(self, *, auth: bool) -> Self:
        self._auth = auth
        return self

    def _post(self, path: str, **data: Any):
        data["_token"] = self._token
        _LOGGER.debug("POST: path='%s', data=%s", path, data)
        return self._cli.post(_BASE_URL.joinpath(path), data=data)

    def _get(self, path: str, **params: Any):
        _LOGGER.debug("GET: path='%s', params=%s", path, params)
        return self._cli.get(_BASE_URL.joinpath(path), params=params)

    async def _ajax(
        self, func: str, account: int | str | None, **params: Any
    ) -> Any:
        async with self._get(
            f"ajax/{self._account(account)}/{func}", **params
        ) as x:
            return await x.json(loads=orjson.loads)

    def _history(
        self,
        what: str,
        account: int | str | None,
        start: dt.date,
        end: dt.date,
    ) -> Awaitable[list[list[str]]]:
        params = {"from": date_to_str(start), "to": date_to_str(end)}
        return self._ajax(f"{what}History", account, **params)

    def _update_token(self, html: str) -> None:
        self._token = parse_token(html)
        _LOGGER.debug("CSRF токен: %s", self._token)

    def _update_accounts(self, html: str) -> None:
        self._accounts = tuple(parse_accounts(html))
        _LOGGER.debug("Привязанные лицевые счета: %s", self._accounts)

    @property
    def connector_closed(self) -> bool:
        """Коннектор сессии закрыт."""

        return self._cli.closed

    @property
    def opened(self) -> bool:
        """Сессия открыта."""

        return self._token is not None

    @property
    def authorized(self) -> bool:
        """Клиент авторизован."""

        return self._accounts is not None

    @property
    def accounts(self) -> tuple[int, ...]:
        """Привязанные лицевые счета."""

        if self._accounts is None:
            raise AuthorizationRequired("Не авторизован в личном кабинете.")

        return self._accounts

    @property
    def account(self) -> int:
        """Основной лицевой счет."""

        if x := self.accounts:
            return x[0]

        raise AccountNotFound("Основной лицевой счет не найден.")

    def _account(self, account: int | str | None) -> int:
        if account is None:
            return self.account

        assert (account := int(account)) > 0

        if account in self.accounts:
            return account

        raise AccountNotFound("Лицевой счет %d не найден.", account)

    async def open(
        self,
        login: str | None = None,
        password: str | None = None,
        auth: bool | None = None,
    ) -> None:
        """Открыть сессию с опциональной авторизацией в личном кабинете.

        Parameters:
            login: E-mail личного кабинета. Опционально. Будет сохранен в клиенте в случае успешной авторизации.
            password: Пароль личного кабинета. Опционально. Будет сохранен в клиенте в случае успешной авторизации.
            auth: Авторизоваться при открытии. Если не указано, берет из клиента.

        Raises:
            AuthorizationError: При ошибке авторизации.
        """

        if not self.opened:
            _LOGGER.debug("Открытие сессии.")

            async with self._get("login") as x:
                self._update_token(await x.text())

        if auth is None:
            auth = self._auth

        if not auth or self.authorized:
            return

        _LOGGER.debug("Авторизация.")

        login, password = login or self._login, password or self._password

        if not (login and password):
            raise AuthorizationError("Не указаны параметры входа.")

        _LOGGER.debug("Авторизация в личном кабинете %s", login)

        async with self._post("login", login=login, password=password) as x:
            if x.url == x.history[0].url:
                raise AuthorizationError(
                    "Ошибка авторизации. Проверьте данные входа."
                )

            self._update_accounts(await x.text())

        _LOGGER.debug("Авторизация в личном кабинете %s успешна.", login)

        # Сохраняем актуальную пару логин-пароль
        self._login, self._password = login, password

    async def close(self, close_connector: bool | None = None) -> None:
        """Выход из личного кабинета и закрытие клиентской сессии.

        Parameters:
            close_connector: Закрыть коннектор. Если не указан, параметр берется из клиента.
        """

        if close_connector is None:
            close_connector = self._close_connector

        try:
            if self.authorized:
                _LOGGER.debug("Выход из личного кабинета %s.", self._login)

                async with self._get("logout") as x:
                    # выход из аккаунта выполняет редирект на
                    # страницу входа с новым токеном сессии
                    self._update_token(await x.text())

                self._accounts = None

        finally:
            if close_connector:
                _LOGGER.debug("Закрытие коннектора сессии.")

                await self._cli.close()
                self._token = None

    @api(auth_required=True)
    async def download_pdf(
        self,
        accrual: Accrual,
        *,
        peni: bool = False,
    ) -> bytes | None:
        """Загрузка квитанции в формате PDF.

        Parameters:
            accrual: Объект квитанции.
            peni: Загрузить квитанцию для оплаты пени.

        Returns:
            Данные в формате `PDF` при успехе или `None` при неудаче.
        """

        if not (id := accrual.peni_id if peni else accrual.bill_id):
            return

        try:
            account = accrual.account
            json = await self._ajax("getReceipt", account, receiptId=id)
            filename: str = json["fileName"]
            path = f"account/{account}/receipts/download"

            async with self._get(path, kvit=filename) as x:
                _LOGGER.debug(
                    "Загрузка квитанции '%s', размер %d байт.",
                    filename,
                    x.content_length,
                )
                return await x.read()

        except Exception:
            return

    @api(auth_required=True)
    async def qr_codes(self, accrual: Accrual) -> QrCodes:
        """Загружает PDF квитанции и извлекает QR коды оплаты.

        Parameters:
            accrual: квитанция.

        Returns:
            Возвращает объект `QrCodes`.
        """

        result = await asyncio.gather(
            self.download_pdf(accrual, peni=False),
            self.download_pdf(accrual, peni=True),
        )

        return QrCodes(*result)

    @api(auth_required=True)
    async def year_accruals(
        self,
        year: int | None = None,
        *,
        account: int | str | None = None,
        limit: int | None = None,
        include_details: bool = False,
    ) -> list[Accrual]:
        """Запрос квитанций лицевого счета за год.

        Если год не уточняется - используется текущий.

        Parameters:
            year: год.
            account: номер лицевого счета. Если `None` - будет использоваться
                основной лицевой счет личного кабинета.
            limit: кол-во последних квитанций в ответе. По-умолчанию все квитанции за год.
            include_details: дополнительный запрос детализированных затрат на каждую
                квитанцию в полученном результате. По-умолчанию: `False`.
        """

        account = self._account(account)

        resp: list[list[str]] = await self._ajax(
            func="getReceipts",
            account=account,
            year=year or date_last_accrual().year,
        )

        db: dict[dt.date, Accrual] = {}

        for data in resp:
            date = date_attr(data[0])

            if limit and limit == len(db) and date not in db:
                break

            record = db.setdefault(
                date,
                Accrual(
                    account=account,
                    date=date,
                    summa=to_decimal(data[1]),
                    peni=to_decimal(data[2]),
                ),
            )

            id = data_attr(data[5])

            match data[3]:
                case "общая":
                    record.bill_id = id
                case "пени":
                    record.peni_id = id
                case _ as x:
                    raise ParsingError("Неизвестный тип квитанции '%s'.", x)

        result = list(db.values())

        if include_details:
            await self.update_accruals(result)

        return result

    @api(auth_required=True)
    async def update_accrual(self, accrual: Accruals) -> None:
        """Обновление детализированных данных квитанции или начисления.

        Parameters:
            accrual: квитанция/начисление для обновления.
        """

        resp: list[list[str]] = await self._ajax(
            "accrualsDetalization",
            accrual.account,
            month=accrual.date.strftime("01.%m.%y"),
        )

        accrual.details = {
            str_normalize(x[0]): AccrualDetalization(*map(to_decimal, x[1:]))
            for x in resp
        }

    @api(auth_required=True)
    async def update_accruals(self, accruals: Iterable[Accruals]) -> None:
        """Обновление детализированных данных квитанций или начислений.

        Parameters:
            accruals: квитанции/начисления для обновления.
        """

        await asyncio.gather(*map(self.update_accrual, accruals))

    @api(auth_required=True)
    async def meters_history(
        self,
        *,
        start: dt.date | None = None,
        end: dt.date | None = None,
        account: int | str | None = None,
    ) -> list[MeterInfoHistory]:
        """Запрос счетчиков лицевого счета с историей показаний.

        Если даты не уточняются - результат будет включать все доступные показания.

        Parameters:
            start: дата начала периода.
            end: дата окончания периода (включается в ответ).
            account: номер лицевого счета. Если `None` - будет использоваться основной лицевой счет личного кабинета.
        """

        start, end = start or _MIN_DATE, end or _MAX_DATE

        assert start <= end

        db: dict[tuple, list[MeterValue]] = {}

        while True:
            _LOGGER.debug("Requesting meters history from %s to %s", start, end)
            history = await self._history("counters", account, start, end)

            # Лимит записей ответа сервера - 25. Контроль превышения на случай изменения API.
            assert (num := len(history)) <= 25

            # Множество для проверки содержания в ответе данных от одной даты.
            unique_dates = set()

            for _, key, date, value, consumption, source in history:
                key = tuple(key.split(", счетчик №", 1))
                unique_dates.add(end := str_to_date(date[27:35]))
                db.setdefault(key, []).append(
                    MeterValue(
                        date=end,
                        value=Decimal(value),
                        consumption=Decimal(consumption),
                        source=source,
                    )
                )

            if num < 25:
                break

            # Возможен баг: если в один день число записей больше лимита,
            # то сервер не сможет вернуть полный результат ни при каких условиях.
            # Этот случай крайне маловероятен, но выполнена проверка и обход ситуации.
            if len(unique_dates) == 1:
                _LOGGER.warning("Результат может содержать неполные данные")

                if start == end:
                    break

                end -= dt.timedelta(days=1)

                _LOGGER.warning("Применен обход")

        # Исключаем дублирование записей из наложенных ответов и конвертируем в кортеж
        return [
            MeterInfoHistory(*k, history=list(dict.fromkeys(v)))
            for k, v in db.items()
        ]

    @api(auth_required=True)
    async def accruals_history(
        self,
        *,
        start: dt.date | None = None,
        end: dt.date | None = None,
        account: int | str | None = None,
        include_details: bool = False,
    ) -> list[MonthAccrual]:
        """Запрос начислений за заданный период.

        Если даты не уточняются - результат будет включать все доступные показания.

        Parameters:
            start: дата начала периода.
            end: дата окончания периода (включается в ответ).
            account: номер лицевого счета. Если `None` - будет использоваться
                основной лицевой счет личного кабинета.
            include_details: дополнительный запрос детализированных затрат на каждое
                начисление в полученном результате. По-умолчанию: `False`.
        """

        account = self._account(account)
        start, end = start or _MIN_DATE, end or _MAX_DATE

        assert start <= end

        history = await self._history("accruals", account, start, end)

        result: list[MonthAccrual] = []

        for date, *decimals in history:
            decimals = map(to_decimal, decimals)
            accrual = MonthAccrual(
                account, date_attr(date), *decimals, details=None
            )

            # запрос поломан. возвращает нулевые начисления в невалидном диапазоне дат.
            # при первом нулевом начислении прерываем цикл, так как далее все начисления тоже нулевые.
            if not accrual.summa:
                break

            result.append(accrual)

        if include_details:
            await self.update_accruals(result)

        return result

    @api(auth_required=True)
    async def payments_history(
        self,
        *,
        start: dt.date | None = None,
        end: dt.date | None = None,
        account: int | str | None = None,
    ) -> list[Payment]:
        """Запрос истории платежей за заданный период.

        Если даты не уточняются - результат будет включать все доступные показания.

        Parameters:
            start: дата начала периода.
            end: дата окончания периода (включается в ответ).
            account: номер лицевого счета. Если `None` - будет использоваться
                основной лицевой счет личного кабинета.
        """

        start, end = start or _MIN_DATE, end or _MAX_DATE

        assert start <= end

        x = await self._history("payments", account, start, end)
        payments = (
            Payment(date_attr(x0), to_decimal(x1), x3) for x0, x1, x3 in x
        )

        # Ответ содержит нулевые платежи (внутренние перерасчеты). Применим фильтр.
        return [x for x in payments if x.summa]

    @api(auth_required=True)
    async def account_info(
        self,
        account: int | str | None = None,
    ) -> AccountInfo:
        """Запрос информации о лицевом счете.

        Parameters:
            account: номер лицевого счета. Если `None` - используется основной счет.
        """

        async with self._get(f"account/{self._account(account)}") as x:
            return parse_account(await x.text())

    @api(auth_required=True)
    async def account_add(
        self,
        account: int | str | PublicAccountInfo,
        last_bill_amount: Decimal = Decimal(),
    ) -> None:
        """Привязка лицевого счета к аккаунту личного кабинета.

        Parameters:
            account: номер или публичная информация о лицевом счете
            last_bill_amount: сумма последнего начисления.
                Может быть взята автоматически из публичной информации о счете.
        """

        if isinstance(account, PublicAccountInfo):
            last_bill_amount = last_bill_amount or account.balance
            account = account.account

        assert (account := int(account)) > 0

        if account in self.accounts:
            return

        if last_bill_amount <= 0:
            raise AccountBindingError("Сумма последнего начисления не указана")

        _LOGGER.debug("Привязка лицевого счета %d", account)

        async with self._post(
            "account/add",
            account=account,
            summ=last_bill_amount,
        ) as x:
            self._update_accounts(await x.text())

        if account not in self.accounts:
            raise AccountBindingError(
                "Не удалось привязать лицевой счет %d", account
            )

    @api(auth_required=True)
    async def account_rm(self, account: int | str) -> None:
        """Отвязка лицевого счета от аккаунта личного кабинета.

        Parameters:
            account: номер лицевого счета.
        """

        assert (account := int(account)) > 0

        if account not in self.accounts:
            _LOGGER.debug("Лицевой счет %d не привязан.", account)
            return

        async with self._post(f"account/{account}/remove") as x:
            self._update_accounts(await x.text())

        if account in self.accounts:
            raise AccountBindingError(
                "Не удалось отвязать лицевой счет %d", account
            )

    async def _set_meters_values(
        self,
        path: str,
        values: Mapping[int, Decimal],
    ) -> None:
        if not values:
            return

        async with self._get(path) as x:
            meters = parse_meters(await x.text())

        data: dict[str, Any] = {}

        # Если используем без авторизации - извлечем номер лицевого счета
        # из пути запроса и добавим в данные запроса
        if not path.startswith("account"):
            data["ls"] = int(path.rsplit("/", 1)[-1])

        for id, value in values.items():
            if m := meters.get(id):
                if value > m.value:
                    data[f"counters[{id}_0][value]"] = value
                    data[f"counters[{id}_0][rawId]"] = id
                    data[f"counters[{id}_0][tarif]"] = 0

                    continue

                raise ValueError(
                    f"Новое значение счетчика {id} должно быть выше текущего {m.value}"
                )

            raise ValueError(f"Счетчик {id} не найден")

        async with self._post(path, **data) as x:
            await x.text()

    @api(auth_required=True)
    async def meters_info(
        self, account: int | str | None = None
    ) -> Mapping[int, PublicMeterInfo]:
        """Запрос информации о приборах учета по лицевому счету.

        Возвращает словарь `идентификатор - информация о приборе учета`.

        Включает следующую информацию:
        - Внутренний идентификатор (для отправки новых показаний)
        - Серийный номер
        - Дата последнего показания
        - Последнее показание
        """

        async with self._get(f"account/{self._account(account)}/counters") as x:
            return parse_meters(await x.text())

    @api(auth_required=True)
    async def set_meters_values(
        self,
        values: Mapping[int, Decimal],
        *,
        account: int | str | None = None,
    ) -> None:
        """Передача новых показаний приборов учета.

        Parameters:
            values: словарь `идентификатор прибора - новое показание`.
            account: номер лицевого счета.
        """

        await self._set_meters_values(
            f"account/{self._account(account)}/counters", values
        )

    @api(public=True)
    async def pub_meters_info(
        self, account: int | str
    ) -> Mapping[int, PublicMeterInfo]:
        """Запрос публичной информации о приборах учета по лицевому счету.

        Возвращает словарь `идентификатор - информация о приборе учета`.

        Включает следующую информацию:
        - Внутренний идентификатор (для отправки новых показаний)
        - Серийный номер
        - Дата последнего показания
        - Последнее показание

        Parameters:
            account: номер лицевого счета.
        """

        assert (account := int(account)) > 0

        async with self._get(f"counters/{account}") as x:
            return parse_meters(await x.text())

    @api(public=True)
    async def pub_set_meters_values(
        self,
        account: int | str,
        values: Mapping[int, Decimal],
    ) -> None:
        """Передача новых показаний приборов учета без авторизации.

        Parameters:
            account: номер лицевого счета.
            values: словарь `идентификатор прибора - новое показание`.
        """

        assert (account := int(account)) > 0

        await self._set_meters_values(f"counters/{account}", values)

    @api(public=True)
    async def pub_account_info(
        self, account: int | str
    ) -> PublicAccountInfo | None:
        """Запрос открытой информации по лицевому счету.

        Parameters:
            account: номер лицевого счета.
        """

        assert (account := int(account)) > 0

        async with self._get("payment/checkLS", ls=account) as x:
            json: Mapping[str, Any] = await x.json(loads=orjson.loads)

        if json["checkLS"]:
            return PublicAccountInfo(
                account,
                str_normalize(json["address"]),
                to_decimal(json["balanceSumma"]),
                to_decimal(json["balancePeni"]),
            )

        _LOGGER.info("Лицевой счет %d не найден.", account)

    @api(public=True)
    async def pub_accounts_info(
        self, accounts: Iterable[int | str]
    ) -> Mapping[int, PublicAccountInfo]:
        """Запрос открытой информации по лицевым счетам.

        Parameters:
            accounts: номера лицевых счетов.
        """

        result = await asyncio.gather(*map(self.pub_account_info, accounts))

        return {x.account: x for x in result if x}
