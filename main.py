import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from skrf.plotting import smith  # Smith Chart
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QIcon  # Import QIcon untuk ikon jendela

# Fungsi Perhitungan
def hitung_koefisien_refleksi(ZL, ZO):
    return (ZL - ZO) / (ZL + ZO)

def hitung_vswr(gamma):
    return (1 + abs(gamma)) / (1 - abs(gamma))

def hitung_daya_diserap(gamma):
    return (1 - abs(gamma)**2)

def hitung_daya_dipantulkan(gamma):
    return abs(gamma)**2

def hitung_return_loss(gamma):
    if abs(gamma) == 0:
        return float('inf')
    return -20 * math.log10(abs(gamma))

# Fungsi Smith Chart
def plot_smith_chart(zl_normalized, gamma):
    # Menggambar Smith Chart kosong
    plt.figure(figsize=(8, 8))
    smith()  
    
    # Menampilkan titik berdasarkan koefisien refleksi
    plt.plot(np.real(gamma), np.imag(gamma), 'ro', markersize=10)  # Titik merah
    
    # Menampilkan judul
    plt.title("Smith Chart - Impedansi Normalisasi", fontsize=12)
    plt.show()

# Fungsi Pie Chart
def plot_pie_chart(daya_serap, daya_pantul):
    labels = ['Daya Diserap', 'Daya Dipantulkan']
    sizes = [daya_serap, daya_pantul]
    colors = ['#4CAF50', '#FF5733']  # Hijau dan merah
    explode = (0.05, 0.1)  # "Meledakkan" irisan daya

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90, textprops={'fontsize': 12})
    plt.title('Distribusi Daya: Diserap vs Dipantulkan', fontsize=14)
    plt.show()

# Kelas Aplikasi GUI
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Perhitungan Impedansi, Smith Chart, dan Pie Chart')
        self.setWindowIcon(QIcon('icon.png'))  # Menambahkan ikon (ganti 'icon.png' dengan nama file ikon Anda)
        main_layout = QVBoxLayout()

        # Input Impedansi
        self.zl_input = QLineEdit(self)
        self.zl_input.setPlaceholderText("Masukkan impedansi beban (ZL) contoh: 3+4j")
        main_layout.addWidget(QLabel("Impedansi Beban (ZL)"))
        main_layout.addWidget(self.zl_input)

        self.zo_input = QLineEdit(self)
        self.zo_input.setPlaceholderText("Masukkan impedansi karakteristik (ZO) contoh: 50")
        main_layout.addWidget(QLabel("Impedansi Karakteristik (ZO)"))
        main_layout.addWidget(self.zo_input)

        # Tombol-Tombol
        self.calc_button = QPushButton('Hitung', self)
        self.calc_button.clicked.connect(self.hitung)
        main_layout.addWidget(self.calc_button)

        self.smith_button = QPushButton('Tampilkan Smith Chart', self)
        self.smith_button.clicked.connect(self.tampilkan_smith_chart)
        main_layout.addWidget(self.smith_button)

        self.pie_button = QPushButton('Tampilkan Pie Chart', self)
        self.pie_button.clicked.connect(self.tampilkan_pie_chart)
        main_layout.addWidget(self.pie_button)

        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset)
        main_layout.addWidget(self.reset_button)

        # Output
        self.result_label = QLabel(self)
        self.result_label.setWordWrap(True)
        main_layout.addWidget(self.result_label)

        self.setLayout(main_layout)

        # Variabel Data
        self.gamma = None
        self.zl_normalized = None
        self.daya_serap = None
        self.daya_pantul = None

    def hitung(self):
        try:
            zl = complex(self.zl_input.text())
            zo = complex(self.zo_input.text())

            if abs(zl) <= 0 or abs(zo) <= 0:
                self.result_label.setText("Impedansi harus bernilai positif.")
                return

            # Perhitungan
            self.gamma = hitung_koefisien_refleksi(zl, zo)
            self.vswr = hitung_vswr(self.gamma)
            self.daya_serap = hitung_daya_diserap(self.gamma) * 100
            self.daya_pantul = hitung_daya_dipantulkan(self.gamma) * 100
            self.return_loss = hitung_return_loss(self.gamma)
            self.zl_normalized = zl / zo

            result = (f"Koefisien Refleksi Gamma = {self.gamma:.4f}\n"
                      f"VSWR = {self.vswr:.4f}\n"
                      f"Persentase daya diserap = {self.daya_serap:.2f}%\n"
                      f"Persentase daya dipantulkan = {self.daya_pantul:.2f}%\n"
                      f"Return Loss = {self.return_loss:.2f} dB\n"
                      f"Impedansi Normalisasi (ZL') = {self.zl_normalized:.4f}")
            self.result_label.setText(result)

        except ValueError:
            self.result_label.setText("Input tidak valid. Harap masukkan impedansi dalam format yang benar (contoh: 3+4j).")

    def tampilkan_smith_chart(self):
        if self.zl_normalized is None or self.gamma is None:
            self.result_label.setText("Belum ada data untuk ditampilkan pada Smith Chart.")
            return
        plot_smith_chart(self.zl_normalized, self.gamma)

    def tampilkan_pie_chart(self):
        if self.daya_serap is None or self.daya_pantul is None:
            self.result_label.setText("Belum ada data untuk ditampilkan pada Pie Chart.")
            return
        plot_pie_chart(self.daya_serap, self.daya_pantul)

    def reset(self):
        self.zl_input.clear()
        self.zo_input.clear()
        self.result_label.clear()
        plt.close('all')  # Menutup semua plot
        self.zl_normalized = None
        self.daya_serap = None
        self.daya_pantul = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
