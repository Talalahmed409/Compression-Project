import sys
import math
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QComboBox, QTextEdit,
    QPushButton, QWidget, QTableWidget, QTableWidgetItem, QGridLayout, QHeaderView,
    QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# Importing other compression functions
from arithmetic_encoder import arithmetic_encode, arithmetic_decode
from huffman import build_frequency_dict, build_huffman_tree, generate_huffman_codes, encode_text as huffman_encode
from huffman import decode_huffman

from rle import RLE, RLE_decode  # RLE module


def simplify_ratio(original_size, encoded_size):
    gcd_value = math.gcd(original_size, encoded_size)
    return f"{original_size // gcd_value}:{encoded_size // gcd_value}"


def lbg_algorithm(data, num_levels):
    data = np.array(data)
    epsilon = 1e-6
    levels = [np.mean(data)]
    while len(levels) < num_levels:
        levels = [level + epsilon for level in levels] + \
            [level - epsilon for level in levels]
        while True:
            clusters = {level: [] for level in levels}
            for point in data:
                nearest_level = min(levels, key=lambda x: abs(point - x))
                clusters[nearest_level].append(point)
            new_levels = [
                np.mean(clusters[level]) if clusters[level] else level for level in levels]
            if np.allclose(new_levels, levels, atol=epsilon):
                break
            levels = new_levels
    boundaries = [(levels[i] + levels[i + 1]) /
                  2 for i in range(len(levels) - 1)]
    return levels, boundaries


def lbg_compression(data, num_levels):
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


def decode_nu_scalar(compressed_data, levels):
    # Decompress by mapping each value back to its closest level
    decompressed_data = []
    for value in compressed_data:
        # Find the closest quantization level
        closest_level = min(levels, key=lambda level: abs(value - level))
        decompressed_data.append(closest_level)
    return decompressed_data


class CompressionGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.huffman_tree = None  # To store the Huffman tree for decoding

    def initUI(self):
        self.setWindowTitle('Compression Techniques (Final Project)')
        self.resize(800, 600)
        self.setWindowIcon(QIcon("icon.ico"))

        self.layout = QGridLayout()

        self.method_label = QLabel("Select Compression Method:")
        self.method_label.setAlignment(Qt.AlignCenter)
        self.method_combo = QComboBox()
        self.method_combo.addItems(
            ["Arithmetic Encoding", "Huffman Encoding", "Run-Length Encoding", "NU Scalar"])
        self.method_combo.currentIndexChanged.connect(self.switch_method)

        self.input_label = QLabel("Input Text or Data:")
        self.input_label.setAlignment(Qt.AlignCenter)
        self.input_text = QTextEdit()
        self.input_text.setAlignment(Qt.AlignCenter)

        self.table_label = QLabel("Character Probabilities:")
        self.table_label.setAlignment(Qt.AlignCenter)
        self.prob_table = QTableWidget(0, 2)
        self.prob_table.setHorizontalHeaderLabels(["Character", "Probability"])
        self.prob_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.prob_table.verticalHeader().setVisible(False)

        self.generate_table_button = QPushButton("Generate Probability Table")
        self.generate_table_button.clicked.connect(self.generate_table)
        self.generate_table_button.setEnabled(False)

        self.output_label = QLabel("Outputs:")
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setAlignment(Qt.AlignCenter)

        self.encode_button = QPushButton("Encode")
        self.encode_button.clicked.connect(self.encode_text)

        self.decode_button = QPushButton("Decode")
        self.decode_button.clicked.connect(self.decode_text)

        self.layout.addWidget(self.method_label, 0, 0)
        self.layout.addWidget(self.method_combo, 0, 1, 1, 2)
        self.layout.addWidget(self.input_label, 1, 0)
        self.layout.addWidget(self.input_text, 1, 1, 1, 2)
        self.layout.addWidget(self.table_label, 2, 0)
        self.layout.addWidget(self.prob_table, 2, 1, 1, 2)
        self.layout.addWidget(self.generate_table_button, 3, 0, 1, 3)
        self.layout.addWidget(self.output_label, 4, 0)
        self.layout.addWidget(self.output_text, 4, 1, 1, 2)
        self.layout.addWidget(self.encode_button, 5, 0, 1, 3)
        self.layout.addWidget(self.decode_button, 6, 0, 1, 3)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
        self.switch_method()

        self.setStyleSheet("""
        QMainWindow {
            background-color: #2b2b2b;
        }
        QLabel {
            font-size: 14px;
            color: #ffffff;
            text-align: center;
        }
        QComboBox {
            font-size: 13px;
            background-color: #3c3f41;
            color: #ffffff;
            border: 2px solid #5c5f61;
            padding: 0px;
            border-radius: 4px;
            text-align: center;
        }
        QComboBox QAbstractItemView {
            font-size: 13px;
            background-color: #3c3f41;
            color: #f0f0f0;
            selection-color: #ffffff;
            border: 1px solid #5c5f61;
        }
        QTextEdit {
            font-size: 13px;
            background-color: #3c3f41;
            color: #f0f0f0;
            border: 1px solid #5c5f61;
            border-radius: 4px;
            text-align: center;
        }
        QPushButton {
            font-size: 13px;
            color: #ffffff;
            background-color: #ff0048;
            border: none;
            border-radius: 4px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #b3003f;
        }
        QPushButton:disabled {
            background-color: #555555;
        }
        QTableWidget {
            font-size: 13px;
            background-color: #3c3f41;
            color: #f0f0f0;
            border: 1px solid #5c5f61;
            border-radius: 4px;
            gridline-color: #5c5f61;
            text-align: center;
        }
        QTableWidget::item {
            text-align: center;
            padding: 4px;
            border: none;
            background-color: #3c3f41;
            color: #f0f0f0;
        }
        QTableWidget::item:selected {
            background-color: #ff0048;
            color: #ffffff;
        }
        QHeaderView {
            background-color: #3c3f41;
        }

        QHeaderView::section {
            text-align: center;
            background-color: #3c3f41;
            color: #ffffff;
            border: 1px solid #5c5f61;
            padding: 4px;
        }
        QScrollBar:vertical {
            width: 8px;
            background: #3c3f41;
        }
        QScrollBar::handle:vertical {
            background: #ff0048;
            border-radius: 4px;
        }
        QMessageBox {
            background: #3c3f41;
        }
    """)

    def switch_method(self):
        method = self.method_combo.currentText()
        if method == "Arithmetic Encoding":
            self.generate_table_button.setEnabled(True)
            self.prob_table.setEnabled(True)
            self.table_label.setVisible(True)
            self.prob_table.setVisible(True)
        else:
            self.generate_table_button.setEnabled(False)
            self.prob_table.setEnabled(False)
            self.table_label.setVisible(False)
            self.prob_table.setVisible(False)

    def generate_table(self):
        sequence = self.input_text.toPlainText()
        if not sequence.strip():
            QMessageBox.warning(
                self, "Error", "Please enter a sequence first.")
            return

        unique_chars = sorted(set(sequence))
        self.prob_table.setRowCount(len(unique_chars))
        for i, char in enumerate(unique_chars):
            char_display = char if char != ' ' else 'Space'
            char_item = QTableWidgetItem(char_display)
            char_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            prob_item = QTableWidgetItem()
            prob_item.setTextAlignment(Qt.AlignCenter)
            self.prob_table.setItem(i, 0, char_item)
            self.prob_table.setItem(i, 1, prob_item)

    def encode_text(self):
        method = self.method_combo.currentText()
        input_text = self.input_text.toPlainText()

        if not input_text.strip():
            QMessageBox.warning(self, "Error", "Input text cannot be empty.")
            return

        original_size = len(input_text) * 8
        encoded_size = 0
        result = ""

        if method == "Arithmetic Encoding":
            probabilities = {}
            total_prob = 0.0
            for row in range(self.prob_table.rowCount()):
                char = self.prob_table.item(row, 0).text()
                prob_item = self.prob_table.item(row, 1)
                try:
                    prob = float(prob_item.text())
                except (ValueError, AttributeError):
                    QMessageBox.warning(
                        self, "Error", f"Invalid probability for character '{char}'.")
                    return
                probabilities[char] = prob
                total_prob += prob

            if abs(total_prob - 1.0) > 1e-6:
                QMessageBox.warning(
                    self, "Error", "The total probability must equal 1.")
                return
            # Store the sequence length and probabilities
            self.sequence_length = len(input_text)  # Store the sequence length
            self.probabilities = probabilities  # Store probabilities for decoding

            try:
                encoded_result = arithmetic_encode(input_text, probabilities)
                code_word = encoded_result[0]
                result = str(code_word)
            except Exception as e:
                QMessageBox.critical(self, "Encoding Error", str(e))
                return

            self.output_text.setText(f"Encoded Result:\n{result}")

        elif method == "Huffman Encoding":
            frequency = build_frequency_dict(input_text)
            huffman_tree = build_huffman_tree(frequency)
            self.huffman_tree = huffman_tree  # Store the Huffman tree
            huffman_codes = generate_huffman_codes(huffman_tree)
            try:
                result = huffman_encode(input_text, huffman_codes)
                encoded_size = len(result)  # Encoded size in bits
            except Exception as e:
                QMessageBox.critical(self, "Encoding Error", str(e))
                return

            simplified_ratio = simplify_ratio(original_size, encoded_size)
            # Enable decoding after encoding
            self.decode_button.setEnabled(True)

            self.output_text.setText(
                f"Encoded Result:\n{result}\n\nHuffman Codes: {huffman_codes}\n\nOriginal Size: {original_size} bits\nEncoded Size: {encoded_size} bits\n\nCompression Ratio:\n {simplified_ratio}")
            huffman_codes = {}

        elif method == "Run-Length Encoding":
            try:
                input_text = self.input_text.toPlainText()
                if not input_text.strip():
                    QMessageBox.warning(
                        self, "Error", "Please enter text to encode.")
                    return
                result = RLE(input_text)  # Call the RLE function directly
                self.output_text.setText(f"RLE Encoded Result:\n{result}")
            except Exception as e:
                QMessageBox.critical(self, "Encoding Error",
                                     f"RLE Encoding Failed:\n{str(e)}")

        elif method == "NU Scalar":
            try:
                data = list(map(float, input_text.split()))
                num_levels = 4  # For simplicity, using 4 quantization levels
                compressed_data, levels = lbg_compression(data, num_levels)
                # Store compressed data for later decompression
                self.compressed_data = compressed_data
                self.levels = levels  # Store levels for decompression
                result = f"Compressed Data: {compressed_data}\nQuantization Levels: {levels}"
            except ValueError:
                QMessageBox.warning(
                    self, "Error", "Please enter valid comma-separated numbers.")
                return

            self.output_text.setText(result)

    def decode_text(self):
        method = self.method_combo.currentText()

        if method == "Arithmetic Encoding":
            if not hasattr(self, "sequence_length"):
                QMessageBox.warning(
                    self, "Error", "No sequence length available for decoding. Perform encoding first.")
                return

            if not hasattr(self, "probabilities"):
                QMessageBox.warning(
                    self, "Error", "No probabilities available for decoding. Perform encoding first.")
                return

            encoded_value = self.input_text.toPlainText()
            if not encoded_value.strip():
                QMessageBox.warning(
                    self, "Error", "Please provide encoded value to decode.")
                return

            try:
                # Convert to float if necessary
                encoded_value = float(encoded_value)
                decoded_text = arithmetic_decode(
                    encoded_value, self.probabilities, self.sequence_length)
                self.output_text.setText(f"Decoded Result:\n{decoded_text}")
            except Exception as e:
                QMessageBox.critical(self, "Decoding Error", str(e))

        elif method == "Huffman Encoding":
            if self.huffman_tree is None:
                QMessageBox.warning(
                    self, "Error", "No Huffman tree available for decoding.")
                return

            encoded_text = self.input_text.toPlainText()
            if not encoded_text.strip():
                QMessageBox.warning(
                    self, "Error", "Please provide encoded text to decode.")
                return

            try:
                decoded_text = decode_huffman(encoded_text, self.huffman_tree)
                self.output_text.setText(f"Decoded Result:\n{decoded_text}")
            except Exception as e:
                QMessageBox.critical(self, "Decoding Error", str(e))

        elif method == "Run-Length Encoding":
            try:
                encoded_text = self.input_text.toPlainText()
                if not encoded_text.strip():
                    QMessageBox.warning(
                        self, "Error", "Please provide encoded text to decode.")
                    return
                # Call the RLE_decode function directly
                result = RLE_decode(encoded_text)
                self.output_text.setText(f"RLE Decoded Result:\n{result}")
            except Exception as e:
                QMessageBox.critical(self, "Decoding Error",
                                     f"RLE Decoding Failed:\n{str(e)}")

        elif method == "NU Scalar":
            try:
                compressed_data = list(
                    map(float, self.input_text.toPlainText().split()))
                decompressed_data = decode_nu_scalar(
                    compressed_data, self.levels)
                self.output_text.setText(
                    f"Decompressed Data:\n{decompressed_data}")
            except Exception as e:
                QMessageBox.critical(self, "Decoding Error", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CompressionGUI()
    window.show()
    sys.exit(app.exec_())
