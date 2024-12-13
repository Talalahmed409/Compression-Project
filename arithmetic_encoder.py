import math

def arithmetic_encode(sequence, probabilities):
    # Calculate cumulative probabilities
    cumulative_probs = {}
    cumulative = 0.0
    for char, prob in probabilities.items():
        cumulative_probs[char] = (cumulative, cumulative + prob)
        cumulative += prob

    # Encoding process
    low, high = 0.0, 1.0
    for char in sequence:
        if char not in cumulative_probs:
            raise ValueError(f"Character '{char}' not found in the probability dictionary.")
        
        char_low, char_high = cumulative_probs[char]
        range_width = high - low
        high = low + range_width * char_high
        low = low + range_width * char_low

    # Final encoded value
    encoded_value = (low + high) / 2

    # Calculate compression ratio
    # Number of bits required to encode the value
    num_bits_encoded = -math.log2(high - low)
    # Original size in bits (assuming 8 bits per character)
    original_size = len(sequence) * 8
    # Compression ratio
    compression_ratio = original_size / num_bits_encoded

    return encoded_value, compression_ratio


# Example Usage
sequence = "ACBA"
probabilities = {
    "A": 0.8,
    "B": 0.02,
    "C": 0.18
}

try:
    encoded_value, compression_ratio = arithmetic_encode(sequence, probabilities)
    print(f"Encoded value: {encoded_value}")
    print(f"Compression ratio: {compression_ratio:.2f}")
except ValueError as e:
    print(e)
