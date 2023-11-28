import sys
import cv2
import mediapipe as mp
import pyautogui as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QSizePolicy, QGridLayout
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt
import pyttsx3

class EyeControlUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAutoFillBackground(True)

        self.setWindowTitle("EyeNav : Your Eye-Controlled Assistance")
        self.setWindowIcon(QIcon("final_project_implementation\images_for_UI\app_logo.png"))

        # Maximize the window
        self.showMaximized()

        # Set the window background color to sky blue
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(135, 206, 250))  # Sky blue color
        self.setPalette(palette)

        layout = QVBoxLayout()
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(layout)

        header_label = QLabel("EyeNav : Navigate with Your Head or Eye Movements, Blink to Select")
        header_label.setStyleSheet("font-size: 28px; color: #0074D9;")

        # Create a container widget to center the buttons
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_container.setLayout(button_layout)

        # Increase the button size
        button_size = 150
        button_style = "font-size: 16px; background-color: rgb(152, 228, 255);"  # RGB(152, 228, 255)

        self.food_button = QPushButton("Food")
        food_icon = QIcon("final_project_implementation\images_for_UI\food.png")
        food_pixmap = food_icon.pixmap(button_size // 2, button_size // 2)  # Increase image size
        self.food_button.setIcon(food_icon)
        self.food_button.setIconSize(food_pixmap.size())
        self.food_button.setFixedSize(button_size, button_size)
        self.food_button.setStyleSheet(button_style)


        self.water_button = QPushButton("Water")
        water_icon = QIcon("final_project_implementation\images_for_UI\water_bottle.png")
        water_pixmap = water_icon.pixmap(button_size // 2, button_size // 2)  # Increase image size
        self.water_button.setIcon(water_icon)
        self.water_button.setIconSize(water_pixmap.size())
        self.water_button.setFixedSize(button_size, button_size)
        self.water_button.setStyleSheet(button_style)


        self.medicines_button = QPushButton("Medicines")
        medicines_icon = QIcon("final_project_implementation\images_for_UI\medicines.png")
        medicines_pixmap = medicines_icon.pixmap(button_size // 2, button_size // 2)  # Increase image size
        self.medicines_button.setIcon(medicines_icon)
        self.medicines_button.setIconSize(medicines_pixmap.size())
        self.medicines_button.setFixedSize(button_size, button_size)
        self.medicines_button.setStyleSheet(button_style)


        self.help_button = QPushButton("Help")
        help_icon = QIcon("final_project_implementation\images_for_UI\help.png")
        help_pixmap = help_icon.pixmap(button_size // 2, button_size // 2)  # Increase image size
        self.help_button.setIcon(help_icon)
        self.help_button.setIconSize(help_pixmap.size())
        self.help_button.setFixedSize(button_size, button_size)
        self.help_button.setStyleSheet(button_style)


        self.food_button.clicked.connect(self.say_button_name)
        self.water_button.clicked.connect(self.say_button_name)
        self.medicines_button.clicked.connect(self.say_button_name)
        self.help_button.clicked.connect(self.say_button_name)


        # Add buttons to the button layout within the container
        button_layout.addWidget(self.food_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.water_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.medicines_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.help_button, alignment=Qt.AlignCenter)

        # Add the button container to the main layout, making it the topmost element
        layout.addWidget(header_label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(button_container, alignment=Qt.AlignTop | Qt.AlignHCenter)

    def say_button_name(self):
        sender = self.sender()
        button_text = sender.text()
        engine = pyttsx3.init()
        engine.say(f"Patient needs {button_text}.")
        engine.runAndWait()

# Initialize the FaceMesh model
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pg.size()

# Create a custom window for OpenCV and minimize it
cv2.namedWindow("Eye Controlled Mouse", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Eye Controlled Mouse", cv2.WINDOW_NORMAL, cv2.WINDOW_GUI_NORMAL)

app = QApplication(sys.argv)
eye_control_ui = EyeControlUI()
eye_control_ui.showMaximized()  # Maximize the PyQt5 window

cam = cv2.VideoCapture(0)

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_h, frame_w, _ = frame.shape
    output = face_mesh.process(frame)

    landmark_points = output.multi_face_landmarks

    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)

            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            if id == 1:
                screen_x = screen_w / frame_w * x
                screen_y = screen_h / frame_h * y
                pg.moveTo(screen_x, screen_y)

        left = [landmarks[145], landmarks[159]]

        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)

            cv2.circle(frame, (x, y), 3, (0, 255, 0))

        if (left[0].y - left[1].y) < 0.015:
            pg.click()
            pg.sleep(1)

    cv2.imshow("Eye Controlled Mouse", frame)
    keyCode = cv2.waitKey(1)

    if keyCode == ord('q'):
        break

cv2.destroyAllWindows()

sys.exit(app.exec_())
