# hangul-asm-py
Disassemble and assemble complex char-set of korean letters into/from serialized(disassembled) form. In this way Korean text can be fed into neural network just like English text.

## Install
```
#pip3 install hangul-asm-py
pip3 install git+https://github.com/keicoon/hangul-asm-py.git
```

## Example
```
from hangul_asm_py import (encode, decode)
asm = encode("안녕하세요 한글 테스트입니다")
# ' ¥¥« §
txt = decode(asm)
# 안녕하세요 한글 테스트입니다

asm = encode("안녕하세요 한글 테스트입니다", mode_type='charcode')
# [139, 147, 171, 130, 153, 188, 146, 147, 137, 152, 139, 159, 32, 146, 147, 171, 128, 165, 175, 32, 144, 152, 137, 165, 144, 165, 139, 167, 184, 130, 167, 131, 147]
txt = decode(asm, mode_type='charcode')
# 안녕하세요 한글 테스트입니다
```

## Natural representation for Hangul(Korean letter)
* `않다` --> `ㅇㅏㄴㅎㄷㅏ`
* `아니하다` --> `ㅇㅏㄴㅣㅎㅏㄷㅏ`
* `이걸` --> `ㅇㅣㄱㅓㄹ`
* `이것을` --> `ㅇㅣㄱㅓㅅㅇㅡㄹ`

## Version history
- v0.1.1
    - add mode_type 'charcode'
- v0.1.0
    - release first version

## Dependancy
- [hangul-asm](https://github.com/keicoon/hangul-asm)