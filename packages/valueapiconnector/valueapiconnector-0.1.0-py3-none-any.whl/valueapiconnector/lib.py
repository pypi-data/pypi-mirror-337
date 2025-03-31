from enum import Enum
import requests
from typing import Any, Callable, Dict, Optional, Self
import urllib.parse
import json
from abc import ABC
from datetime import datetime, date, time
from functools import singledispatchmethod
import string
import random


class ValueAPIConnector:
    def __init__(self, base_url: str):
        self.base_url = base_url
        if not self.base_url.endswith("/"):
            self.base_url += "/"

    def get_context(
        self, context_name: str, auth_token: Optional[str] = None
    ) -> "ValueAPIContext":
        return ValueAPIContext(context_name, self, auth_token)


class ValueDataType(Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    DATE = "date"
    TIME = "time"
    STRING_LIST = "string_list"
    INTEGER_LIST = "integer_list"
    FLOAT_LIST = "float_list"
    BOOLEAN_LIST = "boolean_list"
    JSON = "json"


class ValueResponse[T]:
    def __init__(self, value: Optional[T], error: Optional[str] = None) -> None:
        self.__value = value
        self.__error = error

    @staticmethod
    def with_error(error: str) -> "ValueResponse":
        return ValueResponse(None, error)

    @staticmethod
    def ok(value: T) -> "ValueResponse":
        return ValueResponse[T](value)

    @property
    def is_okay(self) -> bool:
        return not self.is_error

    @property
    def is_error(self) -> bool:
        return self.__error is not None

    @property
    def error(self) -> Optional[str]:
        return self.__error

    def when_error(self, error_callback: Callable[[str], None]) -> Self:
        if self.is_error:
            error_callback(str(self.__error))
        return self

    def when_okay(self, okay_callback: Callable[[T], None]) -> Self:
        if self.is_okay and self.__value is not None:
            okay_callback(self.__value)
        return self

    def unwrap(self) -> Optional[T]:
        return self.__value

    def unwrap_or_default(self, default: T) -> T:
        if self.is_okay and self.__value is not None:
            return self.__value
        else:
            return default

    def unwrap_or_on_error(self, error_callback: Callable[[str], None]) -> Optional[T]:
        if self.is_okay:
            return self.__value
        else:
            error_callback(str(self.__error))

    def __str__(self) -> str:
        return "Valid Value Response."


def Ok(value) -> ValueResponse:
    return ValueResponse.ok(value)


def Error(error: str):
    return ValueResponse.with_error(error)


class ValueAPIContext:
    def __init__(
        self,
        context_name: str,
        connector: ValueAPIConnector,
        auth_token: Optional[str] = None,
    ):
        self.connector = connector
        self.context_name = context_name
        self.auth_token = auth_token

    def get_value(
        self, value_name: str, data_type: ValueDataType = ValueDataType.STRING
    ) -> "ValueAPIValue":
        return ValueAPIValue(value_name, self, data_type)

    def generate_auth_token(self) -> ValueResponse[str]:
        new_token = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=50)
        )
        if self.update_auth_token(new_token):
            return Ok(new_token)
        else:
            return Error("Can not generate auth token.")

    def update_auth_token(self, new_token: str) -> bool:
        result = self.get_value("auth_token").push(new_token)
        if result.is_okay:
            self.auth_token = new_token
        return result.is_okay

    def delete_auth_token(self) -> bool:
        result = self.get_value("auth_token").delete()
        if result.is_okay:
            self.auth_token = None
        return result.is_okay

    def __str__(self) -> str:
        return self.connector.base_url + urllib.parse.quote(self.context_name)

    def _get_auth_header(self):
        return {"Authorization": self.auth_token} if self.auth_token else {}


class ValueAPIValue:
    list_sep = ";-.-;"

    def __init__(
        self,
        value_name: str,
        context: ValueAPIContext,
        data_type: ValueDataType = ValueDataType.STRING,
    ):
        self.value_name = value_name
        self.context = context
        self.data_type = data_type
        assert self.context is not None
        assert self.value_name is not None
        assert self.data_type is not None

    def pull(self) -> ValueResponse:
        response = requests.get(self.url, headers=self.__headers)
        if response.status_code == 401:
            return Error("No authorization, please provide an access token")
        elif response.status_code >= 300:
            return Error(f"{response.status_code} Error: {response.reason}")
        if response.status_code < 299:
            try:
                val = response.content.decode("utf-8")
                match self.data_type:
                    case ValueDataType.STRING:
                        return Ok(val)
                    case ValueDataType.INTEGER:
                        return Ok(int(val))
                    case ValueDataType.FLOAT:
                        return Ok(float(val))
                    case ValueDataType.BOOLEAN:
                        return Ok("true" == val.lower() or "1" == val)
                    case ValueDataType.DATETIME:
                        return Ok(datetime.fromisoformat(val))
                    case ValueDataType.DATE:
                        return Ok(date.fromisoformat(val))
                    case ValueDataType.TIME:
                        return Ok(time.fromisoformat(val))
                    case ValueDataType.STRING_LIST:
                        return Ok(
                            tuple(val.split(ValueAPIValue.list_sep))
                            if len(val) > 0
                            else tuple()
                        )
                    case ValueDataType.INTEGER_LIST:
                        return Ok(
                            tuple(map(int, val.split(ValueAPIValue.list_sep)))
                            if len(val) > 0
                            else tuple()
                        )
                    case ValueDataType.FLOAT_LIST:
                        return Ok(
                            tuple(map(float, val.split(ValueAPIValue.list_sep)))
                            if len(val) > 0
                            else tuple()
                        )
                    case ValueDataType.BOOLEAN_LIST:
                        return Ok(
                            tuple([
                                "true" == v.lower() or "1" == v
                                for v in val.split(ValueAPIValue.list_sep)
                            ])
                            if len(val) > 0
                            else tuple()
                        )
                    case ValueDataType.JSON:
                        return Ok(json.loads(val) if len(val) > 0 else {})
            except Exception as e:
                return Error(f"Error while casting value type. {e}")
        return Error("Error pulling value. Unknown error.")

    @singledispatchmethod
    def push(self, value) -> ValueResponse[str]:
        return Error("Value type not registered")

    @push.register
    def _(self, value: str) -> ValueResponse[str]:
        response = requests.post(self.url, str(value), headers=self.__headers)
        if response.status_code == 200:
            return Ok("ok")
        else:
            return Error(f"{response.status_code} Error. {response.reason}")

    @push.register
    def _(self, value: datetime | date | time) -> ValueResponse[str]:
        return self.push(value.isoformat())

    @push.register
    def _(self, value: float | int | bool) -> ValueResponse[str]:
        return self.push(str(value))

    @push.register
    def _(self, value: set | list | tuple) -> ValueResponse[str]:
        return self.push(ValueAPIValue.list_sep.join(map(str, value)))

    @push.register
    def _(self, value: dict) -> ValueResponse[str]:
        try:
            return self.push(json.dumps(value))
        except Exception as e:
            return Error("Can not dump dict value to json." + e)

    def delete(self) -> ValueResponse[str]:
        response = requests.delete(self.url, headers=self.__headers)
        if response.status_code == 200:
            return Ok("ok")
        else:
            return Error(f"{response.status_code} Error. {response.reason}")

    @property
    def __headers(self) -> Dict[str, str]:
        return self.context._get_auth_header()

    @property
    def __url_value_name(self) -> str:
        return urllib.parse.quote(self.value_name)

    @property
    def url(self) -> str:
        return f"{self.context}/{self.__url_value_name}"


class ValueABC(ABC):
    def __init__(
        self,
        context: ValueAPIContext,
        identifier: Optional[int] = None,
    ):
        if identifier is None:
            value_name = self.__class__.__name__
        else:
            value_name = self.__class__.__name__ + "_" + str(identifier)
        self._value_api = context.get_value(value_name, ValueDataType.JSON)
        # TODO: handle auth! and exceptions!
        self.__dict__ |= self._value_api.pull().unwrap()

    def __setattr__(self, name: str, value: Any, /) -> None:
        super().__setattr__(name, value)
        if name == "_value_api":
            return
        if "_value_api" not in self.__dict__:
            raise ValueError(
                f"You need to call 'super().__init__(context)' in the __init__ function of {self.__class__.__name__} at first statement!"
            )

        data = self.__dict__.copy()
        del data["_value_api"]
        self._value_api.push(data)
