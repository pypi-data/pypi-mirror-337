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

import json
from .TwistTypes import ContextErrors


class TwistModel():
    def __init__(self, model_id: int, parent_device: TwistDevice):
        self.actual_state: int = 0
        self.requested_state: int = 0
        self.model_id: int = model_id
        self.parent_device = parent_device
        self.errors = {
            "error": None,
            "warning": None,
            "info": None,
            "prio": None
        }

    def print_context(self):
        print("function is not supported")

    def parse_general_context(self, payload: str):
        data = json.loads(payload)

        for ctx in data["cl"]:
            index, value = self._get_value_from_context(ctx)
            if index >= ContextErrors.MAX.value:
                pass
            elif ContextErrors(index) == ContextErrors.ERROR:
                self.errors["error"] = value
            elif ContextErrors(index) == ContextErrors.WARNING:
                self.errors["warning"] = value
            elif ContextErrors(index) == ContextErrors.INFO:
                self.errors["info"] = value
            elif ContextErrors(index) == ContextErrors.PRIO:
                self.errors["prio"] = value
        return data

    def _get_value_from_context(self, ctx: dict):
        return ctx["i"], ctx["vl"]

    def context_msg(self, payload):
        raise NotImplementedError("Function not supported for this model")

    def turn_on(self):
        raise NotImplementedError("Function not supported for this model")

    def turn_off(self):
        raise NotImplementedError("Function not supported for this model")

    def open(self):
        raise NotImplementedError("Function not supported for this model")

    def stop(self):
        raise NotImplementedError("Function not supported for this model")

    def close(self):
        raise NotImplementedError("Function not supported for this model")

    def toggle(self):
        raise NotImplementedError("Function not supported for this model")

    def set_value(self, value: int | list[int, int] | list[int, int, int], fading_time: int | None = None):
        raise NotImplementedError("Function not supported for this model")
