from pathlib import Path
import sys

# Optional project-local dependency installation; never modifies system Python.
sys.path.insert(0, str(Path(__file__).resolve().parent / 'deps'))
from PySide6.QtWidgets import QApplication
from config.loader import load_config
from services.fpga_controller import FpgaController
from gui.vision_window import VisionWindow

def main():
    app = QApplication(sys.argv)
    config = load_config(Path(__file__).resolve().parent / 'config/algorithms.json')
    controller = FpgaController(config)
    window = VisionWindow(controller, config)
    window.show()
    return app.exec()

if __name__ == '__main__':
    sys.exit(main())
