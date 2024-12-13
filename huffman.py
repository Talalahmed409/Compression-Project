#loading the needed libraries
import heapq
from collections import defaultdict, Counter

class HuffmanNode: #represents the nodes in the huffman tree
    def __init__(self, char, freq):
        self.char = char #characters stored in the nodes
        self.freq = freq #frequency of the characters
        self.lo = None #left child node
        self.hi = None #right child node

    def __lt__(self, other):
        return self.freq < other.freq #compares the heap ordering by frequency
def build_frequency_dict(text):
    return Counter(text) #counts the occurrences of each character in text
def build_huffman_tree(frequency):
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)  # Transforms the list into a min-heap

    while len(heap) > 1:  # Iterates until there’s only one node left, the root
        lo = heapq.heappop(heap)  # Pops out the node with least frequency
        hi = heapq.heappop(heap)  # Pops out the second least frequent character node
        # Create a new merged node with combined frequency
        merged = HuffmanNode(None, lo.freq + hi.freq)
        
        # Assign the higher frequency node to the left (lo), and the lower to the right (hi)
        if lo.freq >= hi.freq:
            merged.lo = lo  # The higher frequency node goes to the left
            merged.hi = hi  # The lower frequency node goes to the right
        else:
            merged.lo = hi  # The higher frequency node goes to the left
            merged.hi = lo  # The lower frequency node goes to the right

        heapq.heappush(heap, merged)  # Push the merged node into the heap

    return heap[0] if heap else None  # In the end, return the root node

def generate_huffman_codes(node, code='', huffman_code={}):
    if node is None:
        return

    if node.char is not None:
        huffman_code[node.char] = code #if it is a leaf node it stores the code for the characcter

    generate_huffman_codes(node.lo, code + '0', huffman_code) #traverses through the left child and updates their code
    generate_huffman_codes(node.hi, code + '1', huffman_code) #traverses through the right child and updates their code

    return huffman_code #returns dictionary for codes
def encode_text(text, huffman_code):
    return ''.join(huffman_code[char] for char in text) #replaces each char with its code




# def main(input_file_path, output_file_path):
#     with open(input_file_path, "r") as file: #reads text from the input file
#             text = file.read()

#     frequency = build_frequency_dict(text) #get frequency of the characters
#     huffman_tree_root = build_huffman_tree(frequency) #builds the tree
#     huffman_code = generate_huffman_codes(huffman_tree_root) #generates the huffman codes
#     encoded_text = encode_text(text, huffman_code) #encodes the text using huffman code
#     original_size = len(text)*8 #calculate the original size in bits
#     encoded_size = len(encoded_text) #calculates size after encoding in bits
#     compression_ratio = (original_size - encoded_size) / original_size * 100 #calculates the compression ratio

#     with open(output_file_path, "w") as file:
#         file.write(encoded_text) #writes the encoded text to an output .txt file

#     print(f"Original Text: {text}")
#     print(f"Encoded Text: {encoded_text}")
#     print(f"Huffman Codes: {huffman_code}")
#     print(f"Original Size: {original_size} bits")
#     print(f"Encoded Size: {encoded_size} bits")
#     print(f"Compression Ratio: {compression_ratio:.2f}%")



# input_file_path = "input.txt" 
# output_file_path = "encoded_output.txt"  
# main(input_file_path, output_file_path) #runs the main function with input text file's path