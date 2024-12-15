import numpy as np


def lbg_algorithm(data, num_levels):
    data = np.array(data)
    epsilon = 1e-6  # Small value to prevent infinite loop

    # Initialize the first quantization level as the mean of the data
    levels = [np.mean(data)]

    # Iteratively split levels until the desired number is reached
    while len(levels) < num_levels:
        # Split each level into two by adding/subtracting a small value
        levels = [level + epsilon for level in levels] + \
            [level - epsilon for level in levels]

        while True:
            # Assign data points to the nearest quantization level
            clusters = {level: [] for level in levels}
            for point in data:
                nearest_level = min(levels, key=lambda x: abs(point - x))
                clusters[nearest_level].append(point)

            # Update levels to the mean of each cluster
            new_levels = [
                np.mean(clusters[level]) if clusters[level] else level for level in levels]

            # Check for convergence
            if np.allclose(new_levels, levels, atol=epsilon):
                break

            levels = new_levels

    # Determine decision boundaries
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
