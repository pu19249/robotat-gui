import PyQt5.QtWidgets as qtw

class mainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.show()


app = qtw.QApplication([])
mw = mainWindow()

# run the app
app.exec_()
