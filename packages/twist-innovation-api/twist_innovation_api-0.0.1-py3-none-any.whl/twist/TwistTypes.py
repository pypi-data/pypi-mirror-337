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

from enum import Enum

class DeviceVariant(Enum):
    NO_VARIANT = 0xFFFF
    NONE = 0x0000
    LED_4_BUTTON_4 = 0x0001
    LED_1_BUTTON_1 = 0x0002
    MONO_LIGHT_4 = 0x0003
    MONO_LIGHT_2 = 0x0004
    TEMP_1_HUM_1_PIR_1_LUX_1_VOC_1 = 0x0005
    MONO_LIGHT_1_BUTTON_1 = 0x0006
    RGB_1_TUNABLE_WHITE_1 = 0x0007
    BUTTON_8 = 0x0008
    MONO_LIGHT_2_LUX2BRIGHTNESS_1 = 0x0009
    RGB_1_MONO_LIGHT_2 = 0x000A
    LUX_1_UV_1_TEMP_1_HUM_1_WINDSPEED_1_GUSTSPEED_1_WINDDIR_1_RAINFALL_1_PRES_1 = 0x000B
    RGB_1 = 0x000C
    BUTTON_6_LUX_6 = 0x00D2  # Corrected 0x000D2 to 0x00D2
    BUTTON_4 = 0x000E
    TUNABLE_WHITE_2 = 0x000F
    WIND_1_LUX_1_RAIN_1 = 0x0010
    BUTTON_1 = 0x0011
    PULSE_CONTACT_2 = 0x0012
    TBSHUTTER_1 = 0x0013
    MONO_LIGHT_32 = 0x0142
    REPEATER_1 = 0x0015
    REPEATER_1_LED_1 = 0x0016
    LED_12 = 0x0172
    BUTTON_12 = 0x0182
    CBSHUTTER_1_VOLTAGE_1_CURRENT_1 = 0x0019
    TBSHUTTER_6 = 0x001A
    CBSHUTTER_1_MONO_LIGHT_1 = 0x001B
    CBSHUTTER_1 = 0x001C
    MONO_LIGHT_1 = 0x001D
    HEATER_1 = 0x001E
    PBSHUTTER_1 = 0x001F
    CBSHUTTER_2_MONO_LIGHT_4_TEMPERATURE_1 = 0x0020
    GATEWAY_1_WEATHER_1_TEMPERATURE_1_WIND_1_RAIN_1 = 0x0021
    CBSHUTTER_3 = 0x0022
    BUTTON_10 = 0x0023
    MATRIX_1 = 0x0024
    RAIN_1 = 0x0025
    RAIN_1_TEMPERATURE_1_WIND_1_WEATHER_1 = 0x0026
    LOUVRE_2_MONO_LIGHT_4_TEMPERATURE_1 = 0x0027
    LOUVRE_2_MONO_LIGHT_4 = 0x0028


class Models(Enum):
    LOUVRE = 0
    MONO_LIGHT = 1

class ContextErrors(Enum):
    ERROR = 0
    WARNING = 1
    INFO = 2
    PRIO = 3
    ACTUAL = 4
    REQUESTED = 5
    MAX = 6