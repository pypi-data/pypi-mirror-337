from functools import wraps
from typing import cast

from flametracker.rendering import RenderNode
from flametracker.tracking import ActionNode
from flametracker.types import F

from . import UntrackedActionNode


class Tracker:
    active_tracker: "Tracker|None" = None

    def __init__(self):
        self.root = ActionNode(self, None, "@root", (), {})
        self.current = None

    def __enter__(self):
        assert Tracker.active_tracker is None
        Tracker.active_tracker = self
        self.root.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert Tracker.active_tracker == self
        self.root.__exit__(exc_type, exc_val, exc_tb)
        Tracker.active_tracker = None

    def start(self):
        self.__enter__(self)

    def stop(self):
        assert Tracker.active_tracker in (self, None)
        Tracker.active_tracker = None

        try:
            self.root.__exit__(None, None, None)
        except AssertionError:
            return False
        return True

    def to_render(self, group_min_percent: float, use_calls_as_value: bool):
        return RenderNode.from_action(
            self.root, group_min_percent * self.root.length, use_calls_as_value
        )

    def to_dict(self, group_min_percent: float = 0.01, use_calls_as_value=False):
        return self.to_render(group_min_percent, use_calls_as_value).to_dict()

    def to_str(self, group_min_percent: float = 0.1, ignore_args: bool = False):
        return self.to_render(group_min_percent, True).to_str(ignore_args)

    def to_flamegraph(
        self, group_min_percent: float = 0.01, splited=False, use_calls_as_value=False
    ):
        return self.to_render(group_min_percent, use_calls_as_value).to_flamegraph(
            splited,
        )

    def action(self, name: str, *args, **kargs):
        return ActionNode(self, self.current, name, args, kargs)


def action(name: str, *args, **kargs):
    return (
        Tracker.active_tracker.action(name, *args, **kargs)
        if Tracker.active_tracker
        else UntrackedActionNode
    )


def wrap(fn: F) -> F:
    @wraps(fn)
    def call(*args, **kargs):
        tracker = Tracker.active_tracker
        if tracker:
            with tracker.action(fn.__name__, *args, **kargs) as action:
                result = fn(*args, **kargs)
                action.set_result(result)
                return result
        else:
            return fn(*args, **kargs)

    return cast(F, call)
