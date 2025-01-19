import datetime
import time
from math import floor
from typing import Self

STRING_FORMATS = ("%Y-%m-%dT%H:%M", "%Y-%m-%d", "%Y-%m-%d %H:%M")


class Timestamp(int):
    def to_datetime(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(int(self))

    @classmethod
    def from_datetime(cls, dt: datetime.datetime) -> Self:
        return cls(floor(dt.replace(tzinfo=datetime.timezone.utc).timestamp()))

    @classmethod
    def from_string(cls, s: str):
        assert isinstance(s, str)

        for string_format in STRING_FORMATS:
            try:
                dt = datetime.datetime.strptime(s, string_format)
            except ValueError:
                continue
            return cls.from_datetime(dt)
        raise ValueError("Invalid datetime format.")

    @classmethod
    def now(cls):
        return cls(floor(time.time()))

    def __str__(self) -> str:
        return self.to_datetime().strftime("%Y-%m-%d %H:%M")

    def __repr__(self):
        return f"{self.__class__.__name__}({int(self)})"
