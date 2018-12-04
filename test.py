if __name__ == '__main__':
    from hangul_asm_py import (encode, decode)
    txt = """이번 강추위는 북극 주변의 찬 공기를 가둬놓던 제트기류가 지구 온난화로 인해 약화하면서 '북극 한기'가 남쪽으로 이동한 것이 근본 원인이다.
북극 상공의 찬 기류를 '폴라 보텍스'(polar vortex)라고 부른다. 강한 바람대인 제트기류는 평소 북극 주변을 빠르게 돌면서 이 찬 기류를 막아두는 역할을 한다. 
그런데 최근 온난화로 인해 북극 해빙이 녹아 북극 상층의 온도가 올라가고 제트기류가 약해지자 북극 한기가 남하해 중위도 지역인 한반도까지 영향을 준 것이다.
<최강한파> 제주 '섬 속의 섬' 우도도 '눈세상' (제주=연합뉴스) 전지혜 기자 = 1월 24일 제주 전역에 기록적인 폭설이 내린 가운데 관광객들이 많이 찾는 제주 '섬 속의 섬' 우도에도 눈이 하얗게 쌓여 있다. << 우도면사무소 제공 >> atoz@yna.co.kr
온난화로 인해 '한파 울타리'가 느슨해져 오히려 혹독한 추위가 엄습하는 '온난화의 역설'인 셈이다. 
대설의 경우 중국 북부지방에서 찬 대륙고기압이 확장하면서 상대적으로 따뜻한 서해상을 중심으로 눈구름이 만들어져 바람을 타고 육상으로 유입돼 발생했다."""
    print(txt)
    enc = encode(txt)
    print(enc)
    dec = decode(enc)
    print(dec)

    print("""result info
    source len: {}
    encoded text len: {}
    decoded text len: {}
    equality: {}
    loss: {}""".format(len(txt), len(enc), len(dec), txt == dec, len(enc) / len(txt) * 100))