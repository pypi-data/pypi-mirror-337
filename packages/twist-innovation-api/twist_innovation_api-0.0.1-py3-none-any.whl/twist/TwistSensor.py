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

from .TwistDevice import TwistModel


class TwistSensor(TwistModel):
    def __init__(self, model_id: int, parent_device: TwistDevice):
        super().__init__(model_id, parent_device)

    def context_msg(self, payload: str):
        self.parse_general_context(payload)

    def print_context(self):
        print(f"Sensor Device: {self.parent_device.twist_id}, Model: {self.model_id}")
