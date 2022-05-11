import sys
from sqlalchemy import Column, TEXT, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from PyQt6.QtWidgets import QWidget, QApplication
from Main import *

engine = create_engine("sqlite:///Drugs.db")
session = Session(engine)
class MyMainWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        Base = declarative_base()
        Base.metadata.reflect(engine)
        tables = Base.metadata.tables
        for tablename in list(tables.keys()):
            self.covid_med.addItem(tablename)
        self.item_update()
        self.covid_med.currentIndexChanged.connect(self.item_update)
        self.comedication.currentIndexChanged.connect(self.plainTextEdit.clear)
        self.pushButton.clicked.connect(self.inquiry)
    
    def item_update(self):
        self.plainTextEdit.clear()
        tablename = self.covid_med.currentText()
        Base = declarative_base()
        class Table(Base):
            __tablename__ = tablename
            Name = Column(TEXT, primary_key=True)
            Interaction = Column(TEXT)

        self.comedication.clear()
        obj = session.query(Table).all()
        for item in obj:
            self.comedication.addItem(item.Name)

    def inquiry(self):
        tablename = self.covid_med.currentText()
        comedi_name = self.comedication.currentText()
        Base = declarative_base()
        class Table(Base):
            __tablename__ = tablename
            Name = Column(TEXT, primary_key=True)
            Interaction = Column(TEXT)

        obj = session.get(Table, {'Name':comedi_name})
        if obj.Interaction:
            self.plainTextEdit.setPlainText(obj.Interaction)
        else:
            self.plainTextEdit.setPlainText('無')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyMainWindow()
    win.show()
    sys.exit(app.exec())
    