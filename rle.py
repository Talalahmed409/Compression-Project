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

#   original_string = input("Enter the string: ")
# encoded_string = RLE(original_string)
# print(RLE(original_string))
# print(f"Original string: {original_string}")
# print(f"Encoded string: {encoded_string}")
# print(f"Length of encoded string: {len(encoded_string)}")