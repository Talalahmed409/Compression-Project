import numpy as np


def lbg_algorithm(data, num_levels):
    """
    Implements the Linde-Buzo-Gray (LBG) algorithm for non-uniform scalar quantization.

    Parameters:
    data (list): The input data to quantize.
    num_levels (int): The desired number of quantization levels.

    Returns:
    tuple: Quantization levels and decision boundaries.
    """
    data = np.array(data)
    epsilon = 1e-6  # Small value to prevent infinite loop

    # Step 1: Initialize the first quantization level as the mean of the data
    levels = [np.mean(data)]

    # Step 2: Iteratively split levels until the desired number is reached
    while len(levels) < num_levels:
        # Split each level into two by adding/subtracting a small value
        levels = [level + epsilon for level in levels] + \
            [level - epsilon for level in levels]

        while True:
            # Step 3: Assign data points to the nearest quantization level
            clusters = {level: [] for level in levels}
            for point in data:
                nearest_level = min(levels, key=lambda x: abs(point - x))
                clusters[nearest_level].append(point)

            # Step 4: Update levels to the mean of each cluster
            new_levels = [
                np.mean(clusters[level]) if clusters[level] else level for level in levels]

            # Check for convergence
            if np.allclose(new_levels, levels, atol=epsilon):
                break

            levels = new_levels

    # Step 5: Determine decision boundaries
    boundaries = []
    for i in range(len(levels) - 1):
        boundaries.append((levels[i] + levels[i + 1]) / 2)

    return levels, boundaries


def lbg_compression(data, num_levels):
    levels, boundaries = lbg_algorithm(data, num_levels)
    compressed_data = []
    ranges = []

    # Define ranges using boundaries and levels
    ranges.append(f"(-∞, {boundaries[0]}]")  # First group
    for i in range(1, len(boundaries)):
        ranges.append(f"[{boundaries[i-1]}, {boundaries[i]}]")
    ranges.append(f"[{boundaries[-1]}, ∞)")  # Last group

    # Assign data points to quantized levels
    for point in data:
        for i, boundary in enumerate(boundaries):
            if point <= boundary:
                compressed_data.append(levels[i])
                break
        else:
            compressed_data.append(levels[-1])

    return compressed_data, levels, ranges

    """
    Compresses the data using the LBG algorithm.

    Parameters:
    data (list): The input data to compress.
    num_levels (int): The desired number of quantization levels.

    Returns:
    tuple: Compressed data and the quantization levels.
    """
    levels, boundaries = lbg_algorithm(data, num_levels)
    compressed_data = []

    for point in data:
        for i, boundary in enumerate(boundaries):
            if point <= boundary:
                compressed_data.append(levels[i])
                break
        else:
            compressed_data.append(levels[-1])

    return compressed_data, levels


# # Example usage
# data = [1.0, 2.1, 2.0, 3.5, 3.6, 5.0, 8.0, 13.0]
# num_levels = 4

# compressed_data, quantization_levels = lbg_compression(data, num_levels)
# print("Original Data:", data)
# print("Compressed Data:", compressed_data)
# print("Quantization Levels:", quantization_levels)
