# PyServeLab - simple GUI based local web server
# 
#

import sys
import os
import multiprocessing
from flask import Flask, send_from_directory
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, 
    QPushButton, QLabel, QLineEdit, QHBoxLayout, QMessageBox
)

def run_server(port, directory, default_document):

    app = Flask(__name__)
    
    @app.route("/", defaults={"filename": None})
    @app.route("/<path:filename>")
    def serve_file(filename):
        if filename is None:
            index_path = os.path.join(directory, default_document)
            if os.path.exists(index_path):
                return send_from_directory(directory, default_document)
            return f"Serving directory: {directory} (No default document found)"
        return send_from_directory(directory, filename)
    
    from werkzeug.serving import make_server
    server = make_server("0.0.0.0", port, app)
    server.serve_forever()


class WebServerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyServeLab - Simple Web Server")
        self.setGeometry(100, 100, 500, 250)
        self.server_process = None
        self.selected_directory = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Directory selection
        dir_layout = QHBoxLayout()
        self.dir_label = QLabel("Selected Directory: None")
        dir_button = QPushButton("Select Directory")
        dir_button.clicked.connect(self.select_directory)
        dir_layout.addWidget(self.dir_label)
        dir_layout.addWidget(dir_button)

        # Port selection
        port_layout = QHBoxLayout()
        port_label = QLabel("Port:")
        self.port_input = QLineEdit("5000")
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_input)

        # Default document selection
        default_doc_layout = QHBoxLayout()
        default_doc_label = QLabel("Default Document:")
        self.default_doc_input = QLineEdit("index.html")
        default_doc_layout.addWidget(default_doc_label)
        default_doc_layout.addWidget(self.default_doc_input)

        # Start/Stop buttons
        self.start_button = QPushButton("Start Server")
        self.start_button.clicked.connect(self.start_server)
        self.stop_button = QPushButton("Stop Server")
        self.stop_button.clicked.connect(self.stop_server)
        self.stop_button.setEnabled(False)

        layout.addLayout(dir_layout)
        layout.addLayout(port_layout)
        layout.addLayout(default_doc_layout)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.selected_directory = directory
            self.dir_label.setText(f"Selected Directory: {directory}")

    def start_server(self):
        if not self.selected_directory:
            QMessageBox.warning(self, "Error", "Please select a directory to serve.")
            return

        port_text = self.port_input.text()
        if not port_text.isdigit():
            QMessageBox.warning(self, "Error", "Please enter a valid numeric port.")
            return

        port = int(port_text)
        default_document = self.default_doc_input.text().strip()

        if self.server_process is not None:
            QMessageBox.warning(self, "Error", "Server is already running!")
            return

        # Start the Flask server in a separate process
        self.server_process = multiprocessing.Process(
            target=run_server, 
            args=(port, self.selected_directory, default_document)
        )
        self.server_process.start()

        QMessageBox.information(self, "Server Started", f"Server running on port {port}")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_server(self):
        if self.server_process:
            # Terminate the process forcefully and wait for it to exit
            self.server_process.terminate()
            self.server_process.join()
            self.server_process = None

            QMessageBox.information(self, "Server Stopped", "The server has been stopped.")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)


if __name__ == "__main__":
    qt_app = QApplication(sys.argv)
    main_window = WebServerGUI()
    main_window.show()
    sys.exit(qt_app.exec_())
