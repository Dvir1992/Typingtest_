"""
Fun typing test that displays the accuracy and words per minute in the end
"""
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
import time

data=[]
space_pressed=False
left_pressed=False
delete_pressed=False
backspace_pressed=False
grade_text=""

class LineEdit(QLineEdit):
    """
    Every time one of the keyboard buttons is pressed, the program enter
    "keyPressEvent" function. the function check if specific buttons have been pressed.
    """
    def keyPressEvent(self, event: QKeyEvent):
        global space_pressed, left_pressed, delete_pressed, backspace_pressed
        super(LineEdit, self).keyPressEvent(event)
        if event.key() == Qt.Key_Space:
            print("Space Key pressed")
            space_pressed= True
        if event.key() == Qt.Key_Left:
            left_pressed = True
        if event.key() == Qt.Key_Delete:
            delete_pressed = True
        if event.key() == Qt.Key_Backspace:
            backspace_pressed = True


class speed_and_accuracy(QThread):
    """
    This is the class that check the speed and accuracy of the user through time.
    At the end of the test, it shows the average speed and accuracy.
    """
    def __init__(self):
        super().__init__()
    def run(self):
        global grade_text, data, space_pressed, left_pressed, delete_pressed, backspace_pressed
        i=0
        j=0
        word=''
        start = time.time()
        words=0
        speed=0
        entry=0
        percent=0
        total_percent = 0
        while i!=len(data):
          if left_pressed | delete_pressed | backspace_pressed:
              text="You can't go back or delete your text. Please start again when the text appears"
              self.wrong_values(text)
              i=0
              window.entry_2.clear()
              time.sleep(5)
              window.label_text_2.hide()
              window.label_text.show()
              left_pressed = False
              delete_pressed = False
              backspace_pressed = False
              start = time.time()
          if space_pressed:
            words=words+1
            word=window.entry_2.text().split(" ")[i]
            print (word)
            print(data[i])
            space_pressed=False
            if word == data[i]:
                print(i)
            if len(word)==len(data[i]):
                for letter in data[i]:
                    if letter== word[j]:
                        percent=percent+100/len(data[i])
                    else:
                        print ("mistake")
                    j=j+1
                j=0
            else:
                for k in range(1,len(data[i])+1):
                    if abs(len(word)-len(data[i]))>=k:
                        percent=((len(data[i])-k)/len(data[i]))*100
            window.entry_3.clear()
            window.entry_3.insert("{}%".format(percent))
            total_percent=total_percent+percent
            total_percent_2=total_percent/len(data)
            percent=0
            if (time.time() - start) > 5:
                entry=entry+1
                speed = (speed +words/5)
                end_speed=speed/entry
                window.entry_4.clear()
                window.entry_4.insert("{}".format(words/5))
                words=0
                start = time.time()

            i = i + 1
        window.entry_4.clear()
        window.entry_3.clear()
        window.entry_4.insert("{}".format(end_speed))
        window.entry_3.insert("{}%".format(total_percent_2))
        if end_speed<0.3 and total_percent_2<33:
            grade_text="keep practice both on speed and accuracy"
        elif 0.3 <=end_speed <= 0.8 and 33<total_percent_2 <75:
            grade_text = "You are good both on speed and accuracy. Try to get better"
        elif 0.8<end_speed  and total_percent_2 >75:
            grade_text = "You are very good both on speed and accuracy. Keep going"
        else:
            grade_text= "Nice! Try to be in the same level in both speed and accuracy"
        window.finish_button.setDisabled(False)


    def wrong_values(self,text):
        window.label_text_2.setText(text)
        window.label_text_2.setStyleSheet("font: bold normal 30px 'Times New Roman'")
        window.label_text_2.setWordWrap(True)
        window.welcome_layout.addWidget(window.label_text_2)
        window.outer_layout.addLayout(window.welcome_layout)
        window.outer_layout.addLayout(window.finish_layout)
        window.setLayout(window.outer_layout)
        window.label_text_2.show()
        window.label_text.hide()



class window_app (QWidget):
    """
    window_app class is the main PyQt Gui class
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Typing speed test")
        self.setGeometry(0, 0, 600, 800)
        self.thread = speed_and_accuracy()

        self.welcome_layout = QVBoxLayout()
        self.label_1 = QLabel(self)
        self.label_1.setStyleSheet("border-radius: 90px; background-image: url(Capture.png); border-image: url(Capture.png) 0 stretch; ")

        self.start_explanation=QLabel("Hello! we are going to test your speed typing.  when you are ready click on the red play button and copy the appeared random text. The accuracy and the speed will be updated as the text is written. When you will finish, the average accuracy and the speed results will appear. Finally, after the finish icon is enabled,click it to get a review (Don't forget to click the space button again after the last word). Good luck.",self)
        self.start_explanation.setStyleSheet("font: bold normal 30px 'Times New Roman'")
        self.start_explanation.setWordWrap(True)

        self.start_button = QPushButton()
        self.start_button.setIcon(QIcon("connect.png"))
        self.start_button.setToolTip('play')
        self.start_button.setStyleSheet("icon-size:100px; border: 10px solid white;")
        self.start_button.clicked.connect(self.show_text)

        self.label_text = QLabel(self)
        self.label_text.hide()
        self.label_text.setText(self.rand_text())
        self.label_text.setStyleSheet("font: bold normal 30px 'Times New Roman'")
        self.label_text.setWordWrap(True)
        self.label_text_2 = QLabel(self)


        self.form_layout = QFormLayout()

        self.label_2= QLabel("copy the text above:",self)
        self.label_2.setStyleSheet("border:3px solid black;font: bold italic 15px 'Times New Roman';padding: 20px")
        self.label_3= QLabel("accuracy[%]:",self)
        self.label_3.setStyleSheet("border:3px solid black;font: bold italic 15px 'Times New Roman';padding: 20px")
        self.label_4= QLabel("speed[words/5-sec]:",self)
        self.label_4.setStyleSheet("border:3px solid black; font: bold italic 15px 'Times New Roman'; padding: 20px" )
        self.entry_2= LineEdit()


        self.entry_3= QLineEdit(self)
        self.entry_4= QLineEdit(self)
        self.entry_2.setStyleSheet("padding:10px;border:3px solid black;font:bold italic 15px 'Times New Roman';")
        self.entry_2.setMaxLength(1000)
        self.entry_3.setStyleSheet("padding:10px;border:3px solid black;")
        self.entry_4.setStyleSheet("padding:10px;border:3px solid black;")

        self.finish_layout = QHBoxLayout()
        self.finish_button = QPushButton()
        self.finish_button.setIcon(QIcon("Finish.png"))
        self.finish_button.setToolTip('play')
        self.finish_button.setStyleSheet("icon-size:100px; border: 10px solid white;")
        self.finish_button.setDisabled(True)
        self.finish_button.clicked.connect(self.output)



        self.welcome_layout.addWidget(self.label_1)
        self.welcome_layout.addWidget(self.start_explanation)
        self.welcome_layout.addWidget(self.start_button,alignment=Qt.AlignCenter)
        self.form_layout.addRow(self.label_2, self.entry_2)
        self.form_layout.addRow(self.label_3,self.entry_3)
        self.form_layout.addRow(self.label_4, self.entry_4)
        self.finish_layout.addLayout(self.form_layout)
        self.finish_layout.addWidget(self.finish_button)
        self.outer_layout= QVBoxLayout()
        self.outer_layout.addLayout(self.welcome_layout)
        self.outer_layout.addLayout(self.finish_layout)
        self.setLayout(self.outer_layout)


    def rand_text(self):
        global data
        lines = open("random_texts.txt").read().splitlines()
        text= random.choice(lines)
        data= text.split(" ")
        return text

    def show_text(self):
        self.welcome_layout.addWidget(self.label_text)
        self.label_text.show()
        self.start_explanation.hide()
        self.start_button.hide()
        self.speed_and_accuracy_check()

    def output(self):
        global grade_text
        self.finish_layout.addWidget(self.grade(grade_text),alignment=Qt.AlignTop)
        self.finish_button.hide()

    def grade(self,text):
        label = QLabel(text, self)
        label.setStyleSheet("border:3px solid black;font: bold italic 30px 'Times New Roman';")
        return label

    def speed_and_accuracy_check(self):
        self.thread.start()


if __name__ == '__main__':
    app = QApplication([])
    window = window_app()
    window.show()
    app.exec()




