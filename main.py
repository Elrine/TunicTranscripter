import src.SvgGenerator as sg
import src.PhonicConverter as pc
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Tunic Transcriptor",
        description="Create text in a Tunic script")
    parser.add_argument('filename', help="filename of the script")
    parser.add_argument("-v", "--verbose", action='count', default=0)
    parser.add_argument("-l", "--lang", default="fra", help="Define the language of the translator to IPA")
    parser.add_argument("-m", "--median-line", action="store_true", default=False)
    parser.add_argument("-w", "--width", type=int, help="max width of the result")
    parser.add_argument("-c", "--curve", action="store_true", default=False)
    args = parser.parse_args()
    text_finish = False
    text = ""
    while not text_finish:
        buffer = input("Enter your text: ")
        text += buffer + " "
        if buffer == "":
            text_finish = True
    text = pc.convert_to_ipa(text, lang=args.lang)
    if args.verbose > 0:
        print(text)
    text_array = pc.uni_str_to_array_char(text)
    code_array = pc.char_to_char_code(text_array)
    if args.verbose > 1:
        print(code_array)
    sg.generate_text(code_array, "test1.svg", args.median_line, args.width, args.curve)
