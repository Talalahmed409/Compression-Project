# loading the needed libraries
import heapq
from collections import Counter


class HuffmanNode:  # represents the nodes in the huffman tree
    def __init__(self, char, freq):
        self.char = char  # characters stored in the nodes
        self.freq = freq  # frequency of the characters
        self.lo = None  # left child node
        self.hi = None  # right child node

    def __lt__(self, other):
        return self.freq < other.freq  # compares the heap ordering by frequency


def build_frequency_dict(text):
    return Counter(text)  # counts the occurrences of each character in text


def build_huffman_tree(frequency):
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)  # Transforms the list into a min-heap

    while len(heap) > 1:  # Iterates until there’s only one node left, the root
        lo = heapq.heappop(heap)  # Pops out the node with least frequency
        # Pops out the second least frequent character node
        hi = heapq.heappop(heap)
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


def generate_huffman_codes(node, code='', huffman_code=None):
    if huffman_code is None:
        huffman_code = {}

    if node.char is not None:
        # if it is a leaf node it stores the code for the characcter
        huffman_code[node.char] = code
    else:
        # traverses through the left child and updates their code
        generate_huffman_codes(node.lo, code + '0', huffman_code)
    # traverses through the right child and updates their code
        generate_huffman_codes(node.hi, code + '1', huffman_code)

    return huffman_code  # returns dictionary for codes


def encode_text(text, huffman_code):
    # replaces each char with its code
    return ''.join(huffman_code[char] for char in text)


def decode_huffman(encoded_text, root):
    decoded_text = []
    current_node = root

    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.lo
        else:
            current_node = current_node.hi

        if current_node.char is not None:
            decoded_text.append(current_node.char)
            current_node = root  # Reset to the root for the next character

    return ''.join(decoded_text)
