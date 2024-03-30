from ipa2 import IPA2

CONSONNES :  dict[str, int] = {
    "b": 50,
    "d": 26,
    "f": 17,
    "k": 51,
    "l": 18,
    "m": 56,
    "n": 40,
    "p": 19,
    "s": 27,
    "t": 21,
    "v": 5,
    "z": 54,
    "g": 22,
    "ɲ": 24,
    "ʁ": 42,
    "ʃ": 10,
    "ʒ": 34,
    "dʒ": 58,
    "tʃ": 23,
    "ŋ": 48,
    "j": 30,
    "w": 7,
    "ɥ": 39
}


VOYELLE : dict[str, int] = {
    "a": 3,
    "e": 1,
    "i": 4,
    "o": 31,
    "u": 24,
    "y": 28,
    "ø": 21,
    "œ": 30,
    "ɔ": 17,
    "ə": 16,
    "ɛ": 2,
    "ɑ̃": 15,
    "ɔ̃": 19,
    "ɛ̃": 14,
}


def convert_to_ipa(src : str, lang : str = "fra") -> str:
    IPAConverter = IPA2(lang)
    converted_text = IPAConverter.convert_sent(src.lower().replace("’", "'"))
    return converted_text[0]


def uni_str_to_array_char(src : str) -> list[str]:
    character_array = []
    i = 0
    while i < len(src):
        char = src[i]
        if i + 1 < len(src) and (
            (ord(src[i + 1]) in [771, 774]) or
            (char == "d" and src[i + 1] == "ʒ") or
            (char == "t" and src[i + 1] == "ʃ")):
            combine_char = char + src[i + 1]
            character_array.append(combine_char)
            i += 2
        else:
            character_array.append(char)
            i += 1
    return character_array


def char_to_char_code(src : list[str]) -> list[int]:
    i = 0
    code_array : list[int] = []
    while i < len(src):
        code : int = 0
        voyelle_first = src[i] in VOYELLE.keys()
        if src[i] == " ":
            code = 0
        else:
            if voyelle_first:
                code |= VOYELLE[src[i]] << 6
            else:
                code |= CONSONNES[src[i]]
            if i + 1 < len(src) and src[i + 1] != " ":
                code |= voyelle_first << 11
                consonne_second = src[i + 1] in CONSONNES.keys()
                if voyelle_first and consonne_second:
                    code |= CONSONNES[src[i + 1]]
                    i += 1
                elif not voyelle_first and not consonne_second:
                    code |= VOYELLE[src[i + 1]] << 6
                    i += 1
        i += 1
        code_array.append(code)
    return code_array


def split_list(list : list[int], separator : int) -> list[list[int]]:
    result = []
    temp_list = []
    for i in list:
            if i == separator:
                    result.append(temp_list)
                    temp_list = []
            else:
                    temp_list.append(i)
    result.append(temp_list)
    return result
