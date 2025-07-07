import sys
import os
import threading
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QProgressBar, QMessageBox)
from PyQt6.QtCore import pyqtSignal, QObject
import app_logic

APP_VERSION = "2.3.0"

# Classe para comunicação entre a thread de trabalho e a interface
class WorkerSignals(QObject):
    update_status = pyqtSignal(str, str)
    finished = pyqtSignal()

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.caminho_pdf_entrada = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f"Separador de PDF v{APP_VERSION}")
        self.setGeometry(0, 0, 600, 400)
        self.center_window()
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #555555;
            }
            QLabel {
                padding: 5px;
            }
        """)
        
        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Widgets
        self.label_instrucao = QLabel("Siga os passos para processar seu arquivo")
        self.label_instrucao.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        self.select_button = QPushButton("📁  1. Selecionar Arquivo PDF")
        self.file_label = QLabel("Nenhum arquivo selecionado.")
        self.file_label.setStyleSheet("color: #999999;")
        
        self.process_button = QPushButton("⚙️  2. Processar e Salvar em...")
        self.process_button.setDisabled(True)
        
        self.status_label = QLabel("Aguardando ação...")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0) # Estilo de "ocupado"
        self.progress_bar.hide()

        # Adicionando widgets ao layout
        layout.addWidget(self.label_instrucao)
        layout.addWidget(self.select_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.process_button)
        layout.addStretch() # Espaçador
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)

        # Conectando sinais (eventos)
        self.select_button.clicked.connect(self.selecionar_arquivo)
        self.process_button.clicked.connect(self.processar_arquivo)

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def update_status_slot(self, message, color):
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color};")

    def on_processing_finished(self):
        self.progress_bar.hide()
        self.select_button.setDisabled(False)
        self.process_button.setDisabled(True)
        self.file_label.setText("Nenhum arquivo selecionado.")
        self.file_label.setStyleSheet("color: #999999;")
        self.caminho_pdf_entrada = None

    def selecionar_arquivo(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecione o arquivo PDF", "", "Arquivos PDF (*.pdf);;Todos os arquivos (*)")
        if caminho:
            self.caminho_pdf_entrada = caminho
            self.file_label.setText(os.path.basename(caminho))
            self.file_label.setStyleSheet("color: white;")
            self.process_button.setDisabled(False)
            self.update_status_slot("Arquivo pronto para processar.", "cyan")

    def processar_arquivo(self):
        if not self.caminho_pdf_entrada:
            return

        nome_base_zip, _ = os.path.splitext(os.path.basename(self.caminho_pdf_entrada))
        caminho_zip, _ = QFileDialog.getSaveFileName(self, "Salvar arquivo .zip como...", f"{nome_base_zip}.zip", "Arquivos Zip (*.zip)")

        if not caminho_zip:
            self.update_status_slot("Processo cancelado.", "yellow")
            return

        self.select_button.setDisabled(True)
        self.process_button.setDisabled(True)
        self.progress_bar.show()

        # Threading com PyQt
        self.worker = threading.Thread(target=self.run_processing_logic, args=(self.caminho_pdf_entrada, caminho_zip))
        self.worker.start()

    def run_processing_logic(self, input_path, output_path):
        signals = WorkerSignals()
        signals.update_status.connect(self.update_status_slot)
        signals.finished.connect(self.on_processing_finished)
        
        # Função de callback para a lógica de processamento
        def callback_from_thread(message, color="white"):
            signals.update_status.emit(message, color)

        app_logic.processar_e_zipar_pdf(input_path, output_path, callback_from_thread)
        signals.finished.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
