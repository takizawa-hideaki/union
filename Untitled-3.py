number = 12
str_number = str(number)

text = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

# 変換
text1 = str_number.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(len(str_number))}))
text2 = str_number.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(2)}))
prin
}".format(str_number))