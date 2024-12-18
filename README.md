# Compression Techniques - Final Project

## Features

- Supports **Lossless Compression**:
  - Run-Length Encoding (RLE)
  - Huffman Encoding
  - Arithmetic Encoding
- Supports **Lossy Compression**:
  - NU Scalar Quantization
- **Interactive GUI** built with PyQt5
- **Real-time encoding and decoding** with detailed outputs
- Clear output of **compression ratios and results**

---

## Algorithms Overview

### **Lossless Compression**

#### Run-Length Encoding (RLE)

- Simplifies repetitive data patterns.
- Encodes consecutive identical elements as a single value and count.
- Example: `AAAABBBCCDAA → 4A3B2C1D2A`.

#### Huffman Encoding

- Constructs a binary tree based on character frequencies.
- Assigns shorter codes to frequent characters.
- Guarantees the shortest average code length for a given set of characters.

#### Arithmetic Encoding

- Represents an entire message as a single fractional value.
- Subdivides the range `[0, 1)` based on character probabilities.

### **Lossy Compression**

#### NU Scalar Quantization

- Utilizes the **LBG algorithm** to quantize data into fewer levels.
- Prioritizes data size reduction at the cost of minor quality loss.

---

## GUI Overview

### Main Features:

- **Select Compression Method**: Choose from the available methods.
- **Input Data**: Enter text or numerical data for processing.
- **Encode and Decode**: Perform compression and decompression operations.
- **Character Probability Table**: Visualize and configure probabilities for Arithmetic Encoding.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Talalahmed409/Compression-Project.git
   cd compression-project
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python compression_gui.py
   ```

---

## Screenshots

![Screenshot](https://github.com/user-attachments/assets/efa62138-7724-4dfe-abfd-864a46a5db3e)
![Screenshot](https://github.com/user-attachments/assets/af7b24d4-fe8b-4664-b8a6-e8532013b0dd)
![Screenshot](https://github.com/user-attachments/assets/fdc6f109-0a76-4004-a09a-db2939f030c2)

---

## Team Members

- **Shrouq Mohammed Rashad**
- **Mennah Allah Yasser Nabil**
- **Eyad Samih Hanafi**
- **Fouad Essam William**
- **Talal Ahmed Mahmoud**

### **Supervisors**

- **Dr. Mahmoud Gamal**
- **Eng. Mariem Nagy**

---

## Acknowledgments

Special thanks to **Alexandria University** and our mentors for their guidance throughout this project.
