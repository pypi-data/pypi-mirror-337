from time import perf_counter
from typing import Optional

from flametracker.types import Tracker


class ActionNode:
    __slots__ = (
        "tracker",
        "parent",
        "group",
        "start",
        "end",
        "args",
        "kargs",
        "result",
        "children",
    )

    def __init__(
        self,
        tracker: "Tracker",
        parent: Optional["ActionNode"],
        group: str,
        args: tuple,
        kargs: dict,
    ):
        self.tracker = tracker
        self.parent = parent
        self.group = group
        self.start = 0.0
        self.end = 0.0
        self.args = args
        self.kargs = kargs
        self.result = ()
        self.children: list["ActionNode"] = []

        if parent:
            parent.children.append(self)

    @property
    def length(self) -> float:
        return (self.end - self.start) * 1000

    def set_result(self, result):
        self.result = result

    def __enter__(self):
        assert self.tracker.current == self.parent and self.start == 0.0
        self.start = perf_counter()
        self.tracker.current = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert self.tracker.current == self
        self.end = perf_counter()
        self.tracker.current = self.parent
