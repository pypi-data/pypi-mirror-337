from collections.abc import Callable

import attrs

from liblaf import grapes

from ._base import TimerRecords


@attrs.define
class TimedFunction[**P, T](TimerRecords):
    _func: Callable[P, T] = attrs.field(alias="func")

    def __attrs_post_init__(self) -> None:
        self.label = self.label or grapes.pretty_func(self._func).plain or "Function"

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        self._start()
        result: T = self._func(*args, **kwargs)
        self._end()
        self.log_record(depth=2)
        return result
