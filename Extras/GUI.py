import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QComboBox, QTextEdit,
    QPushButton, QWidget, QTableWidget, QTableWidgetItem, QGridLayout, QHeaderView,
    QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt

# Importing compression functions from your modules
try:
    from arithmetic_encoder import arithmetic_encode
except ImportError:
    arithmetic_encode = None
    print("Error: arithmetic_encoder.py not found or does not contain 'arithmetic_encode'.")

try:
    from huffman import build_frequency_dict, build_huffman_tree, generate_huffman_codes, encode_text as huffman_encode
except ImportError:
    build_frequency_dict = build_huffman_tree = generate_huffman_codes = huffman_encode = None
    print("Error: huffman.py not found or missing required functions.")

try:
    from rle import RLE
except ImportError:
    RLE = None
    print("Error: rle.py not found or does not contain 'RLE' function.")

class CompressionGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Compression Techniques')
        self.resize(800, 600)

        self.layout = QGridLayout()

        # Compression Method Selection
        self.method_label = QLabel("Select Compression Method:")
        self.method_combo = QComboBox()
        self.method_combo.addItems(["Arithmetic Encoding", "Huffman Encoding", "Run-Length Encoding"])
        self.method_combo.currentIndexChanged.connect(self.switch_method)

        # Input Text
        self.input_label = QLabel("Input Text:")
        self.input_text = QTextEdit()

        # Probability Table for Arithmetic Encoding
        self.table_label = QLabel("Character Probabilities (Arithmetic Encoding Only):")
        self.prob_table = QTableWidget(0, 2)
        self.prob_table.setHorizontalHeaderLabels(["Character", "Probability"])
        self.prob_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Button to Generate Probability Table
        self.generate_table_button = QPushButton("Generate Probability Table")
        self.generate_table_button.clicked.connect(self.generate_table)
        self.generate_table_button.setEnabled(False)

        # Compressed Output
        self.output_label = QLabel("Compressed Output:")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        # Encode and Save Buttons
        self.encode_button = QPushButton("Encode")
        self.encode_button.clicked.connect(self.encode_text)

        self.save_button = QPushButton("Save Result")
        self.save_button.clicked.connect(self.save_result)
        self.save_button.setEnabled(False)

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
        self.layout.addWidget(self.save_button, 6, 0, 1, 3)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.switch_method()  # Initialize method-specific UI components

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

        if method == "Arithmetic Encoding":
            if arithmetic_encode is None:
                QMessageBox.critical(self, "Error", "Arithmetic Encoder module not found.")
                return

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
                result = str(arithmetic_encode(input_text, probabilities))
            except Exception as e:
                QMessageBox.critical(self, "Encoding Error", str(e))
                return

        elif method == "Huffman Encoding":
            if not all([build_frequency_dict, build_huffman_tree, generate_huffman_codes, huffman_encode]):
                QMessageBox.critical(self, "Error", "Huffman Encoder modules/functions not found.")
                return

            frequency = build_frequency_dict(input_text)
            huffman_tree = build_huffman_tree(frequency)
            huffman_codes = generate_huffman_codes(huffman_tree)
            try:
                result = huffman_encode(input_text, huffman_codes)
            except Exception as e:
                QMessageBox.critical(self, "Encoding Error", str(e))
                return

        elif method == "Run-Length Encoding":
            if RLE is None:
                QMessageBox.critical(self, "Error", "Run-Length Encoder module not found.")
                return

            try:
                result = RLE(input_text)
            except Exception as e:
                QMessageBox.critical(self, "Encoding Error", str(e))
                return

        self.output_text.setText(result)
        self.save_button.setEnabled(True)

    def save_result(self):
        result_text = self.output_text.toPlainText()
        if not result_text:
            QMessageBox.warning(self, "Error", "No result to save.")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write(result_text)
                QMessageBox.information(self, "Success", "File saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"Failed to save file: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CompressionGUI()
    window.show()
    sys.exit(app.exec_())
