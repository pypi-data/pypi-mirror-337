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
    from TwistAPI import TwistAPI

from .TwistTypes import DeviceVariant
from .TwistModel import TwistModel

from .Variants import model_dict

class TwistDevice:
    def __init__(self, twist_id: int, hw: int, var: DeviceVariant, api: TwistAPI):
        self.twist_id = twist_id
        self.hw = hw
        self.var = var
        self.api = api

        self.model_list: list[TwistModel] = list()

        model_id = 0
        if self.var in model_dict:
            for model in model_dict[self.var]:
                self.model_list.append(model(model_id, self))
                model_id += 1

    def context_msg(self, model_id: int, payload: str):
        self.model_list[model_id].context_msg(payload)
        return self.model_list[model_id]
