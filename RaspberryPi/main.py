import sys
import logging
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainForm

if __name__ == "__main__":
    print('hello pi')
    # config logging
    # filename='running.log',filemode='a',
    logging.basicConfig(level=logging.ERROR,
                        format="%(asctime)s %(filename)s %(funcName)s %(lineno)d %(levelname)s: %(message)s",
                        datefmt = '%Y-%m-%d %H:%M:%S')

    # start app
    app = QApplication(sys.argv)
    mainWindow = MainForm()
    mainWindow.show()
    sys.exit(app.exec_())
    

