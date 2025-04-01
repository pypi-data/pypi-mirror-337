# Copyright (C) 2025 Twist Innovation
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the GNU General Public License for more details:
# https://www.gnu.org/licenses/gpl-3.0.html

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from TwistDevice import TwistDevice
from .TwistTypes import ContextErrors
from .TwistDevice import TwistModel
from enum import Enum


class TwistLouvre(TwistModel):
    class EventIndexes(Enum):
        OPEN = 0
        STOP = 1
        CLOSE = 2
        TOGGLE = 3
        VALUE = 4

    def __init__(self, model_id: int, parent_device: TwistDevice):
        super().__init__(model_id, parent_device)
        self.operating_time = 0
        self.current = 0

    def context_msg(self, payload: str):
        data = self.parse_general_context(payload)

        for ctx in data["cl"]:
            index, value = self._get_value_from_context(ctx)
            if index < ContextErrors.MAX.value:
                if ContextErrors(index) == ContextErrors.ACTUAL:
                    self.actual_state = round(value[0] / 655.35, 0)
                elif ContextErrors(index) == ContextErrors.REQUESTED:
                    self.requested_state = round(value[0] / 655.35, 0)
            else:
                if index == 6:
                    self.operating_time = value[0]
                elif index == 7:
                    self.current = value[0]

    def open(self):
        self._activate_event(TwistLouvre.EventIndexes.OPEN)

    def stop(self):
        self._activate_event(TwistLouvre.EventIndexes.STOP)

    def close(self):
        self._activate_event(TwistLouvre.EventIndexes.CLOSE)

    def toggle(self):
        self._activate_event(TwistLouvre.EventIndexes.TOGGLE)

    def set_value(self, value: int, fading_time: int | None = None):
        if fading_time is not None:
            raise NotImplementedError("Fading time can't be used in this model")
        else:
            self._activate_event(TwistLouvre.EventIndexes.VALUE, value)

    def _activate_event(self, index: TwistLouvre.EventIndexes, value: int | None = None,
                        fading_time: int | None = None):
        data = {
            "i": index.value
        }

        if value is None:
            data["vl"] = []
        elif fading_time is None:
            data["vl"] = [value]
        else:
            data["vl"] = [value, fading_time]

        self.parent_device.api.activate_event(self, data)

    def print_context(self):
        print(
            f"Louvre Device: {self.parent_device.twist_id}, Model: {self.model_id},  Actual: {self.actual_state}, "
            f"Requested: {self.requested_state}, Operating: {self.operating_time}, Current: {self.current}")
