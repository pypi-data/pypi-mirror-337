import re

RE_LTCC = re.sub(r"\s+", '|', ('('+
'''
เy?cีt?ยะ?p?f?

เy?cืt?อะ?p?f?

เy?cิt?cf?

ก็
y?c็t?อcf?

[เแ]cc็t?cf?
[เแ]c็t?cf?

[เ-โ]หltf?
[เ-โ]mbtf?
[เ-โ]y?ct?ะ?p?f?

[เ-ไ]หltf?
[เ-ไ]mbtf?
[เ-ไ]y?ct?p?f?

y?ct?[ะาำ]p?f?

yc[ิ-ู]t?p?f?
c[ิ-ฺํ๎]t?f?

y?cืt?cf?

y?cัt?cf?

ycัt?วะ
cัt?วะ

บ่
y?ctc

y?ฤๅ
y?ฦๅ

cรรc์
y?ccf
y?c?p?
'''.replace('f', '(?:cc?[อุอิ]?[อ์])'.replace('อ', ''))
    .replace('y', '(?:cฺ|c๎)')
    .replace('p', '(?:cฺ)')
    .replace('c', '[ก-ฮ]')
    .replace('t', '[่-๋]')
    .replace('m', '[กจฏฎดตบปอ]')
    .replace('l', '[งญณนมย-วฬ]')
    .replace('b', '[ร-ว]')
    .strip()
+')'))

PATTERN = re.compile(RE_LTCC)

def segment(text: str) -> str:
    '''
    Segments text into Large Thai Character Clusters (LTCCs)
    '''
    return [token for token in PATTERN.split(text) if token]