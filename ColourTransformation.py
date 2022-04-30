import math


def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df / mx) * 100
    v = mx * 100
    return h, s, v


def closest_color(input_hsv, palette):
    # set the distance to be a max long
    # initialise closest_colour to empty
    shortest_distance, closest_colour = 9223372036854775807, None

    # iterate through all the colours
    # for each colour in the list, find the Euclidean distance to the one selected by the user
    h_weight = 0.45
    s_weight = 0.1
    v_weight = 0.45

    for colour in palette:
        # since your colours are in 3D space, perform the calculation in each respective space
        current_distance = math.sqrt(
            (pow((colour[0] - input_hsv[0]) * h_weight, 2)) +
            (pow((colour[1] - input_hsv[1]) * s_weight, 2)) +
            (pow((colour[2] - input_hsv[2]) * v_weight, 2))
        )

        # update the distance along with the corresponding colour
        if current_distance < shortest_distance:
            shortest_distance = current_distance
            closest_colour = colour

    return closest_colour
