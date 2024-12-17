Compression Techniques - Final Project

This project demonstrates various data compression techniques through a graphical user interface (GUI) implemented in Python. The application supports both lossless and lossy compression methods, providing users with an interactive way to encode and decode data while understanding the underlying algorithms.
Features

    Supported Compression Methods:
        Lossless Compression:
            Run-Length Encoding (RLE)
            Huffman Encoding
            Arithmetic Encoding
        Lossy Compression:
            NU Scalar Quantization
    Interactive GUI built using PyQt5.
    Real-time Encoding and Decoding with detailed outputs.
    Visual representation of compression ratios and results.

Algorithms Overview
Lossless Compression

    Run-Length Encoding (RLE):
        Simplifies repetitive data patterns.
        Encodes consecutive identical elements as a single value and count.
        Example: AAAABBBCCDAA → 4A3B2C1D2A.

    Huffman Encoding:
        Constructs a binary tree based on character frequencies.
        Assigns shorter codes to frequent characters.
        Guarantees the shortest average code length for a given set of characters.

    Arithmetic Encoding:
        Represents an entire message as a single fractional value.
        Subdivides the range [0, 1) based on character probabilities.

Lossy Compression

    NU Scalar Quantization:
        Utilizes the LBG algorithm to quantize data into fewer levels.
        Prioritizes data size reduction at the cost of minor quality loss.

GUI Overview

    Select Compression Method: Choose from the available methods.
    Input Data: Enter text or numerical data for processing.
    Encode and Decode: Perform compression and decompression operations.
    Character Probability Table: Visualize and configure probabilities for Arithmetic Encoding.

Installation

    Clone the repository:

git clone https://github.com/Talalahmed409/Compression-Project.git
cd compression-project

Install the required dependencies:

pip install -r requirements.txt

Run the application:

    python compression_gui.py

Screenshots

![Screenshot 2024-12-17 200813](https://github.com/user-attachments/assets/fdc6f109-0a76-4004-a09a-db2939f030c2)
![Screenshot 2024-12-17 200745](https://github.com/user-attachments/assets/af7b24d4-fe8b-4664-b8a6-e8532013b0dd)
![Screenshot 2024-12-17 200647](https://github.com/user-attachments/assets/efa62138-7724-4dfe-abfd-864a46a5db3e)


Team Members

    Shrouq Mohammed Rashad
    Mennah Allah Yasser Nabil
    Eyad Samih Hanafi
    Fouad Essam William
    Talal Ahmed Mahmoud

Supervisor: Dr. Mahmoud Gamal
Instructor: Eng. Mariem Nagy
Acknowledgments

Special thanks to Alexandria University and our mentors for their guidance throughout this project.
