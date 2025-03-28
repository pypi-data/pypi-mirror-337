from collections.abc import Callable

import attrs

from liblaf import grapes

from . import TimerRecords


@attrs.define
class TimedFunction[**P, T](TimerRecords):
    _func: Callable[P, T] = attrs.field(alias="func")

    def __attrs_post_init__(self) -> None:
        self.label = self.label or grapes.full_qual_name(self._func) or "Function"

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        self._start()
        result: T = self._func(*args, **kwargs)
        self._end()
        self.log_record(depth=3)
        return result
