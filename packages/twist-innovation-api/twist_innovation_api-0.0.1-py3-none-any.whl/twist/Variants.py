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

from .TwistLight import TwistLight
from .TwistLouvre import TwistLouvre
from .TwistRgb import TwistRgb
from .TwistSensor import TwistSensor
from .TwistCbShutter import TwistCbShutter
from .TwistTypes import DeviceVariant

model_dict = {
    DeviceVariant.LOUVRE_2_MONO_LIGHT_4: [TwistLouvre, TwistLouvre, TwistLight, TwistLight, TwistLight,
                                          TwistLight],
    DeviceVariant.RGB_1: [TwistRgb],
    DeviceVariant.MONO_LIGHT_4: [TwistLight, TwistLight, TwistLight, TwistLight],
    DeviceVariant.GATEWAY_1_WEATHER_1_TEMPERATURE_1_WIND_1_RAIN_1: [TwistSensor, TwistSensor, TwistSensor,
                                                                    TwistSensor, TwistSensor],
    DeviceVariant.CBSHUTTER_1_MONO_LIGHT_1: [TwistCbShutter, TwistLight],
}
