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


class TwistRgb(TwistModel):
    class EventIndexes(Enum):
        SET = 0
        CLEAR = 1
        VALUE = 2
        TOGGLE = 3
        VALUE_FADING = 4

    def __init__(self, model_id: int, parent_device: TwistDevice):
        super().__init__(model_id, parent_device)

        self.actual_h = 0
        self.actual_s = 0
        self.actual_v = 0
        self.requested_h = 0
        self.requested_s = 0
        self.requested_v = 0

        self.operating_time = 0

    def turn_on(self):
        self._activate_event(TwistRgb.EventIndexes.SET)

    def turn_off(self):
        self._activate_event(TwistRgb.EventIndexes.CLEAR)

    def toggle(self):
        self._activate_event(TwistRgb.EventIndexes.TOGGLE)

    def set_value(self, value: list[int, int, int], fading_time: int | None = None):
        if fading_time is None:
            self._activate_event(TwistRgb.EventIndexes.VALUE, value)
        else:
            self._activate_event(TwistRgb.EventIndexes.VALUE_FADING, value, fading_time)

    def _activate_event(self, index: TwistRgb.EventIndexes, value: list[int, int, int] | None = None,
                        fading_time: int | None = None):
        data = {
            "i": index.value
        }

        if value is None:
            data["vl"] = []
        elif fading_time is None:
            data["vl"] = value
        else:
            value.append(fading_time)
            data["vl"] = value

        self.parent_device.api.activate_event(self, data)

    def context_msg(self, payload: str):
        data = self.parse_general_context(payload)

        for ctx in data["cl"]:
            index, value = self._get_value_from_context(ctx)
            if index < ContextErrors.MAX.value:
                if ContextErrors(index) == ContextErrors.ACTUAL:
                    self.actual_h = round(value[0] / 655.35, 0)
                    self.actual_s = round(value[1] / 655.35, 0)
                    self.actual_v = round(value[2] / 655.35, 0)
                elif ContextErrors(index) == ContextErrors.REQUESTED:
                    self.requested_h = round(value[0] / 655.35, 0)
                    self.requested_s = round(value[0] / 655.35, 0)
                    self.requested_v = round(value[0] / 655.35, 0)
            else:
                if index == 6:
                    self.operating_time = value[0]

    def print_context(self):
        print(f"Rgb Device: {self.parent_device.twist_id}, Model: {self.model_id}, "
              f"Actual: h{self.actual_h} s{self.actual_s} v{self.actual_v}")
