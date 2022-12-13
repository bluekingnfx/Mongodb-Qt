from PyQt6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QMessageBox,QDialog,QWidget,QApplication
from PyQt6.QtGui import QFont,QMovie
from PyQt6.QtCore import QSize,Qt

from functools import partial as pars
import typing as ty


class HelperClass():

    @classmethod
    def ExitFunc(cls,self):
        self.close()

    @classmethod
    def HeadingNDes(cls,HeadingText,Description,HeightDes=0,DesWidth=300,HeadingW=400,HeadingH=50) -> ty.Tuple[QWidget,QLabel]:
        widget = QWidget()
        vLay = QVBoxLayout()
        labelHeading = QLabel()
        labelText = QLabel()
        labelHeading.setText(HeadingText)
        labelHeading.setStyleSheet("color:#333")
        labelHeading.setFixedWidth(HeadingW)
        labelHeading.setFixedHeight(HeadingH)
        labelHeading.setFont(QFont("Sanserif",20,400,False))
        labelText.setText(Description)
        labelText.setStyleSheet("color:#555")
        labelWarn = QLabel()
        labelWarn.setStyleSheet("color:#e83815")
        labelText.setWordWrap(True)
        labelHeading.setWordWrap(True)
        labelText.setFixedWidth(DesWidth)
        if HeightDes > 0 : widget.setFixedHeight(HeightDes)
        labelText.setFont(QFont("Sanserif",16,200,False))
        vLay.addWidget(labelHeading)
        vLay.addWidget(labelText)
        widget.setLayout(vLay)
        return [widget,labelWarn]

    @classmethod
    def ProducePushBut(cls,self,butText:str,connectFunc:ty.Callable[[],None],height=30,argsConnectFunc = []) -> QPushButton:
        but = QPushButton(butText,self)
        but.clicked.connect(pars(connectFunc,but,*argsConnectFunc))
        but.setMinimumHeight(height)
        return but

    @classmethod 
    def ProduceMessageBox(cls,self,boxType:ty.Literal["about","question"],title:str,des:str,okButFunc:ty.Union[ty.Callable[[],None],None] = None,cancel:ty.Union[ty.Callable[[],None],None] = None,OkArgs:ty.List=[],cancelArgs:ty.List = [],sendMessageBox:bool = False) -> QMessageBox:
        if boxType == "about":
            if okButFunc != None:
                okButFunc(*OkArgs)
            QMessageBox.about(self,title,des)
        else:
            question = QMessageBox.question(self,title,des,QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel) 
            if question == QMessageBox.StandardButton.Ok:
                if sendMessageBox == False: okButFunc(*OkArgs)
                else: okButFunc(*OkArgs,question)
            else:
                if cancel != None: cancel(*cancelArgs)
                QMessageBox.close(self)
    
    @classmethod
    def graphicSpinner(cls,mainThread):
        dialogue = QDialog(mainThread)
        dialogue.setMinimumSize(QSize(200,200))
        dialogue.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        label = QLabel(dialogue)
        Fullpath = mainThread.rootFol+"/data/200w.gif"
        movie = QMovie(Fullpath)
        movie.start()
        label.setMovie(movie)
        dialogue.open()
        dialogue.hide()
        return dialogue

    @classmethod
    def setButDisabled(cls,text:str,but:QPushButton):
        but.setText(text)
        but.setDisabled(True)
        QApplication.processEvents()

    @classmethod
    def setButEnabled(cls,text:str,but:QPushButton):
        but.setText(text)
        but.setEnabled(True)
    

if __name__ == "__main__":
    HelperClass()