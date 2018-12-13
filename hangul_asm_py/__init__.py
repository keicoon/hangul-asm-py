FIRST_KORAEN_CHAR = "\uac00"
LAST_KOREAN_CHAR = "\ud7af"
KOREAN_UNICODE_DEFAULT_INDEX = int('0xac00', 16)

DEFAULT_IMT_ARR = (19, 21, 28)
USING_CHARCODE = False
DEFAULT_ASCII_INDEX = 128

import re
REGEX = re.compile('([\\x{:x}-\\x{:x}]+)'.format(DEFAULT_ASCII_INDEX, (DEFAULT_ASCII_INDEX + sum(DEFAULT_IMT_ARR))))
T_INDEX = (DEFAULT_ASCII_INDEX + DEFAULT_IMT_ARR[0] + DEFAULT_IMT_ARR[1])
def _init():
    ascii_idx = DEFAULT_ASCII_INDEX
    def mapping(s, d):
        h2Ascii[s] = d
        ascii2H[d] = s
    for idx in range(DEFAULT_IMT_ARR[0]):
        mapping((int('0x1100', 16) + idx), ascii_idx)
        ascii_idx += 1
    for idx in range(DEFAULT_IMT_ARR[1]):
        mapping((int('0x1161', 16) + idx), ascii_idx)
        ascii_idx += 1
    for idx in range(DEFAULT_IMT_ARR[2]):
        mapping((int('0x11A8', 16) + idx), ascii_idx)
        ascii_idx += 1
h2Ascii = dict()
ascii2H = dict()
_init()

CONV_A2B_LIST = [
    lambda c: int(((ord(c) - KOREAN_UNICODE_DEFAULT_INDEX) / 28) / 21),
    lambda c: int(((ord(c) - KOREAN_UNICODE_DEFAULT_INDEX) / 28) % 21),
    lambda c: int((ord(c) - KOREAN_UNICODE_DEFAULT_INDEX) % 28) - 1,
]
CONV_ADV_LIST = [
    lambda c: c + int('0x1100', 16),
    lambda c: c + int('0x1161', 16),
    lambda c: c + int('0x11A8', 16),
]
CONV_B2A_LIST = [
    lambda i: (i - int('0x1100', 16)) * 588,
    lambda i: (i - int('0x1161', 16)) * 28,
    lambda i: (i - int('0x11A8', 16)) + 1,
]
from functional import seq
def encode(lines, mode_type='char'):
    def split_korean_char(char):
        chars = list(seq(CONV_A2B_LIST)\
            .map(lambda f: f(char))\
            .filter(lambda c: c > -1))
        return list(seq([CONV_ADV_LIST[idx](c) for idx, c in enumerate(chars)])\
            .map(lambda c: h2Ascii[c])\
            .map(lambda c: chr(c)))

    encoded_list = [split_korean_char(char) if LAST_KOREAN_CHAR >= char and char >= FIRST_KORAEN_CHAR else char for char in lines]
    flattened = [val for sublist in encoded_list for val in sublist]
    flatten_encoded_list = "".join(flattened)
    if mode_type is 'charcode':
        flatten_encoded_list = [ord(c) for c in flatten_encoded_list]
    return flatten_encoded_list

def decode(lines, mode_type='char'):
    def merge_korean_char(chars):
        code_korean_char = KOREAN_UNICODE_DEFAULT_INDEX
        for idx, c in enumerate(chars):
            code_korean_char += CONV_B2A_LIST[idx](ascii2H[ord(c)])
        return chr(code_korean_char)

    def replace_func(m):
        p1 = m.group()
        new_str = []
        i = 0 
        l = len(p1)
        while i < l:
            t_idx = (i + 2)
            if t_idx < l and ord(p1[t_idx]) >= T_INDEX:
                new_str.append(merge_korean_char(p1[i:i+3]))
                i += 3
            else:
                new_str.append(merge_korean_char(p1[i:i+2]))
                i += 2
        return "".join(new_str)
    if mode_type is 'charcode':
        lines = "".join([chr(c) for c in lines])
    return REGEX.sub(replace_func, lines)