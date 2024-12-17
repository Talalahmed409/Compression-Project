def RLE(input_string):
    if not input_string:
        return ""

    encoded_string = ""
    count = 1
    prev_char = input_string[0]

    for char in input_string[1:]:
        if char == prev_char:
            count += 1
        else:
            encoded_string += str(count) + prev_char
            count = 1
            prev_char = char

    encoded_string += str(count) + prev_char
    return encoded_string
def RLE_decode(encoded_string):
    if not encoded_string:
        return ""

    decoded_string = ""
    count = ""

    for char in encoded_string:
        if char.isdigit():
            count += char
        else:
            decoded_string += char * int(count)
            count = ""

    return decoded_string
