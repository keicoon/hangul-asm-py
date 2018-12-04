FIRST_KORAEN_CHAR = "\uac00"
LAST_KOREAN_CHAR = "\ud7af"
KOREAN_UNICODE_DEFAULT_INDEX = 0xac00

DEFAULT_IMT_ARR = (19, 21, 28)
USING_CHARCODE = False
DEFAULT_ASCII_INDEX = 128

import re
REGEX = re.compile('([{}-{}]+)'.format(hex(DEFAULT_ASCII_INDEX), hex(DEFAULT_ASCII_INDEX+sum(DEFAULT_IMT_ARR))))
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
h2Ascii = {}, ascii2H = {}
_init()

CONV_FUNC_TABLE = {
    'conv_i_a2b': lambda c: int(((ord(c) - KOREAN_UNICODE_DEFAULT_INDEX) / 28) / 21),
    'conv_m_a2b': lambda c: int(((ord(c) - KOREAN_UNICODE_DEFAULT_INDEX) / 28) % 21),
    'conv_t_a2b': lambda c: int((ord(c) - KOREAN_UNICODE_DEFAULT_INDEX) % 28) - 1,

    'conv_i_adv': lambda c: c + int('0x1100', 16),
    'conv_m_adv': lambda c: c + int('0x1161', 16),
    'conv_t_adv': lambda c: c + int('0x11A8', 16),

    'conv_i_b2a': lambda i: (i - int('0x1100', 16)) * 588,
    'conv_m_b2a': lambda i: (i - int('0x1161', 16)) * 28,
    'conv_t_b2a': lambda i: (i - int('0x11A8', 16)) + 1,
}

def encode(lines):
    def split_korean_char(char):
        return list((CONV_FUNC_TABLE.conv_i_a2b(char), CONV_FUNC_TABLE.conv_m_a2b(char), CONV_FUNC_TABLE.conv_t_a2b(char))
            .filter(lambda c: c > -1, first))
            .map(lambda (idx, c): (CONV_FUNC_TABLE.conv_i_adv, CONV_FUNC_TABLE.conv_m_adv, CONV_FUNC_TABLE.conv_t_adv)[idx](c))
            .map(lambda c: h2Ascii[c])
            .map(lambda c: chr(c)))
    encoded_list = [split_korean_char(char) if LAST_KOREAN_CHAR >= char and char >= FIRST_KORAEN_CHAR else char for c in lines]
    return str(encoded_list)

def decode(lines):
    def merge_korean_char(chars):
        code_korean_char = KOREAN_UNICODE_DEFAULT_INDEX
        code_korean_char += (CONV_FUNC_TABLE.conv_i_b2a, CONV_FUNC_TABLE.conv_m_b2a, CONV_FUNC_TABLE.conv_t_b2a)
            .filter(lambda (idx, f): chars[idx])
            .map(lambda (idx, f): f(ord(ascii2H[chars[idx]])))
            .sum()
        return chr(code_korean_char)

    def replace_func(p1):
        new_str = []
        l = len(p1)
        i = 0
        while i < l:
            t_idx = (i + 2)
            if t_idx < l and ord(p1[t_idx]) >= T_INDEX:
                new_str.append(merge_korean_char(p1[i:i+3]))
                i += 3
            else:
                new_str.append(merge_korean_char(p1[i:i+2]))
                i += 2
        return new_str
    return REGEX.sub(replace_func, lines)