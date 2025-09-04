# colors.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022-2023, Gradience Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from gradience.backend.globals import adw_variables_prefixes, adw_palette_prefixes

from gradience.backend.logger import Logger

logging = Logger(logger_name="ColorUtils")


def rgb_to_hash(rgb) -> [str, float]:
    """
    This function converts rgb or rgba-formatted color code to an hexadecimal code.

    Alpha channel from RGBA color codes is passed without any conversion
    as a second return variable and is completely ignored in hexadecimal codes
    to remain compliant with web stantards.
    """
    if rgb.startswith("rgb"):
        rgb_values = rgb.strip("rgb()")

    if rgb.startswith("rgba"):
        rgb_values = rgb.strip("rgba()")

    rgb_list = rgb_values.split(",")

    red = int(rgb_list[0])
    green = int(rgb_list[1])
    blue = int(rgb_list[2])
    alpha = None

    if len(rgb_list) == 4:
        alpha = float(rgb_list[3])

    hex_out = [f"{red:x}", f"{green:x}", f"{blue:x}"]

    for i, hex_part in enumerate(hex_out):
        if len(hex_part) == 1:
            hex_out[i] = "0" + hex_part

    return "#" + "".join(hex_out), alpha

def argb_to_color_code(argb, alpha=None) -> str:
    """
    This function can return either an hexadecimal or rgba-formatted color code.

    By default this function returns hexadecimal color codes.
    If alpha parameter is specified, then the function will return
    an rgba-formatted color code.
    """
    rgba_base = "rgba({0}, {1}, {2}, {3})"

    red = redFromArgb(argb)
    green = greenFromArgb(argb)
    blue = blueFromArgb(argb)
    if not alpha:
        alpha = alphaFromArgb(argb)

    if alpha in (255, 0.0):
        return hexFromArgb(argb)

    return rgba_base.format(red, green, blue, alpha)

def adjust_brightness(argb, factor: float, alpha=None) -> int:
    """
    Adjust the brightness of an ARGB color.

    Returns a new ARGB integer which can be passed to argb_to_color_code.
    """
    red = redFromArgb(argb)
    green = greenFromArgb(argb)
    blue = blueFromArgb(argb)
    if alpha is None:
        alpha = alphaFromArgb(argb)

    # Apply brightness factor and clamp to 0-255
    red = max(0, min(255, int(red * factor)))
    green = max(0, min(255, int(green * factor)))
    blue = max(0, min(255, int(blue * factor)))

    # Recombine into a single ARGB integer
    return (alpha << 24) | (red << 16) | (green << 8) | blue

def color_vars_to_color_code(variables: dict, palette: dict) -> dict:
    """
    This function converts GTK color variables to color code
    (hexadecimal code if no transparency channel, RGBA format if otherwise).

    You can bypass passing a `palette` parameter if you put an None value to it.
    This isn't recommended however, because in most cases you'll be unable to determine
    if variables you pass don't contain any palette color variables.
    """

    output = variables

    if palette == None:
        logging.warning("Palette parameter in `color_vars_to_color_code()` function not set. Incoming bugs ahead!")

    def __has_palette_prefix(color):
        return any(prefix in color for prefix in adw_palette_prefixes)

    def __has_variable_prefix(color):
        return any(prefix in color for prefix in adw_variables_prefixes)

    def __update_vars(var_type, variable, color_value):
        if var_type == "palette":
            output[variable] = palette[color_value[:-1]][color_value[-1:]]
        elif var_type == "variable":
            output[variable] = output[color_value]

        color_variable_name = output[variable].strip()[1:]

        if __has_palette_prefix(output[variable]):
            __update_vars("palette", variable, color_variable_name)

        if __has_variable_prefix(output[variable]):
            __update_vars("variable", variable, color_variable_name)

    for variable, color in output.items():
        color_value = color.strip()[1:] # Strip spaces and remove '@' from the beginning of the color variable

        if __has_palette_prefix(color_value) and palette != None:
            __update_vars("palette", variable, color_value)

        if __has_variable_prefix(color_value):
            __update_vars("variable", variable, color_value)

    return output


# /**
#  * Returns the alpha component of a color in ARGB format.
#  */
def alphaFromArgb(argb):
    return argb >> 24 & 255


# /**
#  * Returns the red component of a color in ARGB format.
#  */
def redFromArgb(argb):
    return argb >> 16 & 255


# /**
#  * Returns the green component of a color in ARGB format.
#  */
def greenFromArgb(argb):
    return argb >> 8 & 255


# /**
#  * Returns the blue component of a color in ARGB format.
#  */
def blueFromArgb(argb):
    return argb & 255


def hexFromArgb(argb):
    r = redFromArgb(argb)
    g = greenFromArgb(argb)
    b = blueFromArgb(argb)
    outParts = [f'{r:x}', f'{g:x}', f'{b:x}']
    # Pad single-digit output values
    for i, part in enumerate(outParts):
        if (len(part) == 1):
            outParts[i] = '0' + part
    return '#' + ''.join(outParts)
