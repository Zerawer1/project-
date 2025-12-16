import struct

def sha1(data: bytes) -> str:
    # Инициализация констант
    h0 = 0x67452301б
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # Предварительная обработка данных
    bit_length = len(data) * 8
    data += b'\x80'
    while (len(data) * 8) % 512 != 448:
        data += b'\x00'
    data += struct.pack('>Q', bit_length)

    # Разбиение на блоки по 512 бит (64 байта)
    chunks = [data[i:i+64] for i in range(0, len(data), 64)]

    for chunk in chunks:
        # Развертывание блока в 80 слов
        words = list(struct.unpack('>16I', chunk)) + [0] * 64
        for i in range(16, 80):
            words[i] = left_rotate(words[i-3] ^ words[i-8] ^ words[i-14] ^ words[i-16], 1)

        # Инициализация хеш-значений для этого блока
        a, b, c, d, e = h0, h1, h2, h3, h4

        # Основной цикл SHA-1
        for i in range(80):
            if 0 <= i <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = left_rotate(a, 5) + f + e + k + words[i] & 0xFFFFFFFF
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp

        # Обновление хеш-значений
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    # Формирование итогового хеша
    return '%08x%08x%08x%08x%08x' % (h0, h1, h2, h3, h4)

def left_rotate(n: int, b: int) -> int:
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF
