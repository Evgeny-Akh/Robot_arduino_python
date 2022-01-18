from PyQt5 import QtWidgets, uic
import pyfirmata # для работы с pyfirmata сначала необходимо в Arduino IDE загрузить программу StandartFirmata
import sys
port="COM3" # порт платы Arduino (можно узнать в Arduino IDE)
try:
    board=pyfirmata.Arduino(port)
    apply=QtWidgets.QApplication([])
    ui=uic.loadUi("arduino.ui")
    ui.setWindowTitle("Работа с роботом через Python")
    class RobotArduino:
        def __init__(self,motor_R1,motor_R2,motor_L1,motor_L2,inDiod):
            self.motor_R1=motor_R1
            self.motor_R2=motor_R2
            self.motor_L1=motor_L1
            self.motor_L2=motor_L2
            self.inDiod=inDiod
        def forward(self): # движение робота вперед
            # вращение правых и левых колес вперед
            board.digital[self.motor_R1].write(1)
            board.digital[self.motor_L1].write(1)
            # блокировка вращения назад правых и левых колес
            board.digital[self.motor_R2].write(0)
            board.digital[self.motor_L2].write(0)
        def backward(self): # движение робота назад
            # блокировка вращения вперед правых и левых колес
            board.digital[self.motor_R1].write(0)
            board.digital[self.motor_L1].write(0)
            # вращение правых и левых колес назад
            board.digital[self.motor_R2].write(1)
            board.digital[self.motor_L2].write(1)
        def forward_left(self): # поворот робота налево с блокировкой левых колес
            # вращение правых колес вперед
            board.digital[self.motor_R1].write(1)
            # блокировка вращения правых колес назад
            board.digital[self.motor_R2].write(0)
            # блокировка вращения вперед и назад левых колес
            board.digital[self.motor_L1].write(0)
            board.digital[self.motor_L2].write(0)
        def forward_right(self): # поворот робота вправо с блокировкой правых колес
            # вращение левых колес вперед
            board.digital[self.motor_L1].write(1)
            # блокировка вращения левых колес назад
            board.digital[self.motor_L2].write(0)
            # блокировка вращения вперед и назад правых колес
            board.digital[self.motor_R1].write(0)
            board.digital[self.motor_R2].write(0)
        def backward_left(self): # задний поворот робота влево с блокировкой левых колес
            # блокировка вращения правых колес вперед
            board.digital[self.motor_R1].write(0)
            # вращение правых колес назад
            board.digital[self.motor_R2].write(1)
            # блокировка вращения вперед и назад левых колес
            board.digital[self.motor_L1].write(0)
            board.digital[self.motor_L2].write(0)
        def backward_right(self): # задний поворот робота вправо с блокировкой правых колес
            # блокировка вращения левых колес вперед
            board.digital[self.motor_L1].write(0)
            # вращение левых колес назад
            board.digital[self.motor_L2].write(1)
            # блокировка вращения вперед и назад правых колес
            board.digital[self.motor_R1].write(0)
            board.digital[self.motor_R2].write(0)
        def left(self): # Поворот налево на месте
            # вращение правых вперед и левых назад
            board.digital[self.motor_R1].write(1)
            board.digital[self.motor_L2].write(1)
            # блокировка вращения правых колес назад и левых вперед
            board.digital[self.motor_R2].write(0)
            board.digital[self.motor_L1].write(0)
        def right(self): # Поворот направо на месте
            # вращение левых вперед и правых назад
            board.digital[self.motor_R2].write(1)
            board.digital[self.motor_L1].write(1)
            # блокировка вращения правых колес вперед и левых назад
            board.digital[self.motor_R1].write(0)
            board.digital[self.motor_L2].write(0)
        def stop_robot(self): # остановка робота
            board.digital[self.motor_R1].write(0)
            board.digital[self.motor_L1].write(0)
            board.digital[self.motor_R2].write(0)
            board.digital[self.motor_L2].write(0)
        def inDiodHigh(self):
            board.digital[self.inDiod].write(1)
        def inDiodLow(self):
            board.digital[self.inDiod].write(0)
        def __del__(self): pass
    robot_arduino=RobotArduino(2,3,4,5,6)
    ui.DiodHigh.clicked.connect(robot_arduino.inDiodHigh)
    ui.DiodLow.clicked.connect(robot_arduino.inDiodLow)
    ui.Forward.clicked.connect(robot_arduino.forward)
    ui.Backward.clicked.connect(robot_arduino.backward)
    ui.ForwardLeft.clicked.connect(robot_arduino.forward_left)
    ui.ForwardRight.clicked.connect(robot_arduino.forward_right)
    ui.BackwardLeft.clicked.connect(robot_arduino.backward_left)
    ui.BackwardRight.clicked.connect(robot_arduino.backward_right)
    ui.Left.clicked.connect(robot_arduino.left)
    ui.Right.clicked.connect(robot_arduino.right)
    ui.Stop.clicked.connect(robot_arduino.stop_robot)
    ui.Close.clicked.connect(apply.quit)
    ui.show(); apply.exec()
except pyfirmata.serial.serialutil.SerialException:
    app=QtWidgets.QApplication(sys.argv)
    window=QtWidgets.QWidget()
    window.setWindowTitle("Ошибка!!!")
    window.resize(400,100)
    label=QtWidgets.QLabel("<center>Порт устройства отсутствует или не верен</center>")
    btnQuit=QtWidgets.QPushButton("&Закрыть")
    vbox=QtWidgets.QVBoxLayout()
    vbox.addWidget(label)
    vbox.addWidget(btnQuit)
    window.setLayout(vbox)
    btnQuit.clicked.connect(app.quit)
    window.show(); sys.exit(app.exec_())