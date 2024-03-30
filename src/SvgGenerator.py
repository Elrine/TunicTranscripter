from svgwrite import container, shapes, Drawing, masking, path
from .PhonicConverter import split_list

LIST_LINE = [
    (0, 6),
    (1, 6),
    (2, 6),
    (3, 7),
    (4, 7),
    (5, 7),
    (0, 1, 9),
    (1, 2, 10),
    (2, 3, 3),
    (3, 4, 11),
    (4, 5, 12)
]

VERTEX = [
    (55, 25), (30, 5), (5, 25), (5, 85), (30, 105), (55, 85), (30, 45), (30, 65), (30, 55), (55, 5), (5, 5), (5, 105), (55, 105)
]

def get_coord(line : int) -> tuple[int, int]:
    return VERTEX[line]

def use_line(code : int, index : int) -> shapes.Line:
    if code & (1 << index):
        start = get_coord(LIST_LINE[index][0])
        end = get_coord(LIST_LINE[index][1])
        return shapes.Line(start, end)

def use_curve(code : int, index : int) -> str:
    if code & (1 << index):
        start = get_coord(LIST_LINE[index][0])
        if code & (1 << index) & 0b11111:
            if (code & 0b111111) & (0b111110 << (index)):
                mid = VERTEX[8]
                if code == 18:
                    mid = (mid[0] + 5, mid[1])
                return "{start[0]} {start[1]} Q {mid[0]} {mid[1]} ".format(start=start, mid=mid)
            else:
                return f"{start[0]} {start[1]} "
        elif code & (1 << index) & 0b100000:
            return f"{start[0]} {start[1]} "
        else:
            end = get_coord(LIST_LINE[index][1])
            control = get_coord(LIST_LINE[index][2])
            return "M {start[0]} {start[1]} Q {control[0]} {control[1]} {end[0]} {end[1]} ".format(start=start, control=control, end=end)
    else:
        return ""

def generate_curve_char(coordonate : tuple[int, int], code : int, use_mid_sec : bool) -> container.SVG:
    if code == 0:
        return None
    char = container.SVG(size=(60, 120), insert=coordonate)
    char.stroke(color="black", width=5, linecap="round", linejoin="round")
    char.fill(opacity=0)
    mask = ""
    if use_mid_sec:
        mask = "url(#mask)"
        char.add(shapes.Line(start=(5, 55), end=(55, 55)))
    path_d = ""
    if code & 0b111111:
        path_d = "M "
    for i in range(11):
        path_d += use_curve(code, i)
    char.add(path.Path(d=path_d, mask=mask))
    if code & 1 << 11:
        char.add(shapes.Circle(center=(VERTEX[4][0], VERTEX[4][1] + 5), r=5, fill="white"))
    return char


def generate_char(coordonate : tuple[int, int], code : int, use_mid_sec : bool = False) -> container.SVG:
    if code == 0:
        return None
    char = container.SVG(size=(60, 120), insert=coordonate)
    char.stroke(color="black", width=5, linecap="round", linejoin="round")
    char.fill(opacity=0)
    for i in range(11):
        line = use_line(code, i)
        if line is not None:
            char.add(line)
    if code & 1 << 11:
        char.add(shapes.Circle(center=(VERTEX[4][0], VERTEX[4][1] + 5), r=5, fill="white"))
    if use_mid_sec:
        char.add(shapes.Line(start=(5, 55), end=(55, 55)))
    if code & (0b111 << 3) and code & 0b111:
        char.add(shapes.Line(VERTEX[6], VERTEX[8]))
        if not use_mid_sec:
            char.add(shapes.Line(VERTEX[7], VERTEX[8]))
    return char

def size_script(ipa_text : list[int], max_width : int) -> tuple[int, int, list[list[int]]]:
    if max_width <= 0:
        return (50 * len(ipa_text) + 10, 120, [ipa_text])
    word_list = split_list(ipa_text, 0)
    max_character = (max_width - 10) / 50
    count_line = 1
    character_left = max_character
    for word in word_list:
        if len(word) + 1 > character_left:
            count_line += 1
            character_left = max_character - len(word)
        else:
            character_left -= len(word) + 1
    return (max_width, count_line * 130, word_list)

def generate_text(ipa_text : list[int], filename : str, use_mid_sec : bool = False, max_width : int = 0, use_curve : bool = False):
    width, height, word_list = size_script(ipa_text, max_width)
    dwg = Drawing(filename=filename, profile="full", size=(width, height))
    mask : masking.Mask = dwg.defs.add(masking.Mask(id="mask"))
    mask.add(shapes.Rect((0,0), (60, 120), fill="white"))
    mask.add(shapes.Rect((0,55), (60, 10), fill="black"))
    x, y = (0, 0)
    max_character = (width - 10) / 50
    character_left = max_character
    for word in word_list:
        if len(word) + 1 > character_left:
            y += 130
            x = 0
            character_left = max_character - len(word)
        else:
            character_left -= len(word) + 1
        for character in word:
            el : container.SVG
            if use_curve:
                el = generate_curve_char((x, y), character, use_mid_sec)
            else:
                el = generate_char((x, y), character, use_mid_sec)
            dwg.add(el)
            x += 50
        x += 50
    dwg.save()

