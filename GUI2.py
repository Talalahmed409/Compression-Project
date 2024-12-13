import sys
import math
import PyQt5

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QComboBox, QTextEdit,
    QPushButton, QWidget, QTableWidget, QTableWidgetItem, QGridLayout, QHeaderView,
    QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# Importing compression functions
from arithmetic_encoder import arithmetic_encode
from huffman import build_frequency_dict, build_huffman_tree, generate_huffman_codes, encode_text as huffman_encode
from rle import RLE


def simplify_ratio(original_size, encoded_size):
        # Simplify a size ratio by dividing both sizes by their GCD.
        gcd_value = math.gcd(original_size, encoded_size)
        simplified_original = original_size // gcd_value
        simplified_encoded = encoded_size // gcd_value
        return f"{simplified_original}:{simplified_encoded}"

class CompressionGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Compression Techniques (Final Project)')
        self.resize(800, 600)
        self.setWindowIcon(QIcon("D:\Study\Fall 2024-2025\Data Compression\Final Project\icon.ico"))

        self.layout = QGridLayout()

        # Compression Method Selection
        self.method_label = QLabel("Select Compression Method:")
        self.method_label.setAlignment(Qt.AlignCenter)
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Arithmetic Encoding", "Huffman Encoding", "Run-Length Encoding"])
        self.method_combo.currentIndexChanged.connect(self.switch_method)

        # Input Text
        self.input_label = QLabel("Input Text:")    
        self.input_label.setAlignment(Qt.AlignCenter)
        self.input_text = QTextEdit()
        self.input_text.setAlignment(Qt.AlignCenter)

        # Probability Table for Arithmetic Encoding
        self.table_label = QLabel("Character Probabilities:")
        self.table_label.setAlignment(Qt.AlignCenter)
        self.prob_table = QTableWidget(0, 2)
        self.prob_table.setHorizontalHeaderLabels(["Character", "Probability"])
        self.prob_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.prob_table.verticalHeader().setVisible(False)  # Hide row numbering
        self.prob_table.setStyleSheet("QTableWidget::item { text-align: center; }")

        # Button to Generate Probability Table
        self.generate_table_button = QPushButton("Generate Probability Table")
        self.generate_table_button.clicked.connect(self.generate_table)
        self.generate_table_button.setEnabled(False)

        # Compressed Output
        self.output_label = QLabel("Outputs:")
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setAlignment(Qt.AlignCenter)

        # Encode Button
        self.encode_button = QPushButton("Encode")
        self.encode_button.clicked.connect(self.encode_text)

        # Adding Widgets to Layout
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

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.switch_method()  # Initialize method-specific UI components

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
            QMessageBox.warning(self, "Error", "Please enter a sequence first.")
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

        original_size = len(input_text) * 8  # Original size in bits
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
                    QMessageBox.warning(self, "Error", f"Invalid probability for character '{char}'.")
                    return
                probabilities[char] = prob
                total_prob += prob

            if abs(total_prob - 1.0) > 1e-6:
                QMessageBox.warning(self, "Error", "The total probability must equal 1.")
                return

            try:
                encoded_result = arithmetic_encode(input_text, probabilities)
                code_word = encoded_result[0]  # Extract the first element of the tuple
                result = str(code_word)  # Convert to string for display
            except Exception as e:
                QMessageBox.critical(self, "Encoding Error", str(e))
                return

            self.output_text.setText(f"Encoded Result:\n{result}")


        elif method == "Huffman Encoding":
            frequency = build_frequency_dict(input_text)
            huffman_tree = build_huffman_tree(frequency)
            huffman_codes = generate_huffman_codes(huffman_tree)
            try:
                result = huffman_encode(input_text, huffman_codes)
                encoded_size = len(result)  # Encoded size in bits
            except Exception as e:
                QMessageBox.critical(self, "Encoding Error", str(e))
                return
                        # Simplify the ratio and display the result
            simplified_ratio = simplify_ratio(original_size, encoded_size)

            

        elif method == "Run-Length Encoding":
            try:
                result = RLE(input_text)
                import re

                def calculate_encoded_size(text):
                    # Regular expression to find all numbers in the text
                    numbers = re.findall(r'\d+', text)
                    
                    # Calculate size for non-number characters (8 bits each)
                    non_number_size = len([char for char in text if not char.isdigit()]) * 8
                    
                    if numbers:
                        # Convert all found numbers to integers and find the largest number
                        max_number = max(map(int, numbers))
                        # Get the number of bits required to represent the largest number
                        number_bit_length = max_number.bit_length()  # This gives the number of bits needed to represent the largest number
                        number_size = len(numbers) * number_bit_length  # Total size for numbers
                    else:
                        number_size = 0  # No numbers in the text

                    total_size = non_number_size + number_size
                    return total_size

                # Example usage in your encode_text method
                encoded_size = calculate_encoded_size(result) # Approximate size in bits for simplicity
            except Exception as e:
                QMessageBox.critical(self, "Encoding Error", str(e))
                return
            simplified_ratio = simplify_ratio(original_size, encoded_size)

        if method == "Arithmetic Encoding":
            self.output_text.setText(f"Encoded Result:\n{result}")
        elif method == "Huffman Encoding":

            self.output_text.setText(f"Encoded Result:\n{result}\n\nHuffman Codes: {huffman_codes}\n\nOriginal Size: {original_size} bits\nEncoded Size: {encoded_size} bits\n\nCompression Ratio:\n {simplified_ratio}")
        else:
            self.output_text.setText(f"Encoded Result:\n{result}\n\nOriginal Size: {original_size} bits\nEncoded Size: {encoded_size}\n\nCompression Ratio: {simplified_ratio}")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set the style for the application
    app.setStyle('Fusion')

    # Create and show the main window
    window = CompressionGUI()
    window.show()

    sys.exit(app.exec_())

