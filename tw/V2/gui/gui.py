from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from bots.recruiter import Recruiter
from safeScheduler import SafeScheduler
from time import sleep

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.error_window = None
        self.recruiter_window = None
        self.login_thread = None
        self.driver = None
        
        self.setWindowTitle("TW Bots")
        self.setGeometry(1000, 100, 10, 10)

        self.schedule = SafeScheduler(minutes_after_failure=30)
        
        self.recruiter = Recruiter(self.schedule)

        self.run_pending_thread = QThread()
        self.run_pending_work = Run_Pending_Work(self.schedule)

        self.run_pending_work.moveToThread(self.run_pending_thread)

        self.run_pending_thread.started.connect(self.run_pending_work.run)

        self.run_pending_work.finished.connect(self.run_pending_thread.quit)
        self.run_pending_work.finished.connect(self.run_pending_work.deleteLater)

        self.run_pending_thread.finished.connect(self.run_pending_thread.deleteLater)

        self.run_pending_thread.start()

        self.menu_bar = QMenuBar()

        self.central_widget = QWidget()
        self.open_browser_button = QPushButton('OPEN BROWSER')
        self.user_label = QLabel('USER:')
        self.user_input = QLineEdit()
        self.password_label = QLabel('PASSWORD:')
        self.password_input = QLineEdit()
        self.show_password_checkbox = QCheckBox()
        self.show_password_label = QLabel('SHOW')
        self.login_button = QPushButton('LOGIN')
        self.open_new_tab_button = QPushButton('NEW TAB')
        self.close_tab_button = QPushButton('CLOSE TAB')
        self.next_tab_button = QPushButton('NEXT TAB')
        self.previous_tab_button = QPushButton('PREVIOUS TAB')
        
        self.recruiter_action = QAction('Recruiter')

        self.main_layout = QVBoxLayout()
        self.sub_layout_1 = QGridLayout()
        self.sub_layout_2 = QGridLayout()

        self.menu_bar.addAction(self.recruiter_action)
        
        self.sub_layout_1.addWidget(self.user_label, 0, 0)
        self.sub_layout_1.addWidget(self.user_input, 0, 1)
        self.sub_layout_1.addWidget(self.password_label, 1, 0)
        self.sub_layout_1.addWidget(self.password_input, 1, 1)
        self.sub_layout_1.addWidget(self.show_password_checkbox, 1, 2)
        self.sub_layout_1.addWidget(self.show_password_label, 1, 3)

        self.sub_layout_2.addWidget(self.open_new_tab_button, 0, 0)
        self.sub_layout_2.addWidget(self.close_tab_button, 0, 1)
        self.sub_layout_2.addWidget(self.next_tab_button, 1, 0)
        self.sub_layout_2.addWidget(self.previous_tab_button, 1, 1)

        self.main_layout.addWidget(self.open_browser_button)
        self.main_layout.addLayout(self.sub_layout_1)
        self.main_layout.addWidget(self.login_button)
        self.main_layout.addLayout(self.sub_layout_2)
        
        self.central_widget.setLayout(self.main_layout)

        self.setMenuBar(self.menu_bar)
        self.setCentralWidget(self.central_widget)
        
        self.user_input.setText('BradleyLedermann')
        self.password_input.setText('oLAAa100')

        self.user_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.password_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.password_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)

        self.open_browser_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )
        self.user_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )
        self.user_input.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, 
            QSizePolicy.Policy.Expanding
        )
        self.password_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )
        self.password_input.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, 
            QSizePolicy.Policy.Expanding
        )
        self.login_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )
        self.open_new_tab_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )
        self.close_tab_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )
        self.next_tab_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )
        self.previous_tab_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )
        
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.recruiter_action.triggered.connect(self.open_recruiter_window)
        
        self.open_browser_button.clicked.connect(self.open_browser)
        self.login_button.clicked.connect(self.login)
        self.open_new_tab_button.clicked.connect(self.open_new_tab)
        self.close_tab_button.clicked.connect(self.close_tab)
        self.next_tab_button.clicked.connect(self.next_tab)
        self.previous_tab_button.clicked.connect(self.previous_tab)
        
        self.show_password_checkbox.stateChanged.connect \
            (self.show_password_checkbox_state_changed)

    def open_recruiter_window(self):
        if self.recruiter_window is None:
            self.recruiter_window = Recruiter_Window(self.recruiter)
        self.recruiter_window.show()
    
    def open_browser(self):
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        self.driver = webdriver.Chrome('D:\chromedriver.exe', options=options)

        self.recruiter.set_driver(self.driver)

    def show_password_checkbox_state_changed(self):
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
    
    def login(self):
        try:
            self.login_thread = QThread()
            
            self.login_work = Login_Work(self)
            self.login_work.moveToThread(self.login_thread)

            self.login_thread.started.connect(self.login_work.run)

            self.login_work.finished.connect(self.login_thread.quit)
            self.login_work.finished.connect(self.login_work.deleteLater)

            self.login_thread.finished.connect(self.login_thread.deleteLater)

            self.login_thread.start()

        except AttributeError as error:
            if self.recruiter_window is None:
                self.recruiter_window = Error_Window()
            self.recruiter_window.set_message(str(error))
            self.recruiter_window.show()

    def open_new_tab(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
    
    def close_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])
    
    def next_tab(self):
        current_tab = self.driver.window_handles.index \
            (self.driver.current_window_handle)

        try:
            self.driver.switch_to.window \
                (self.driver.window_handles[current_tab+1])
        except IndexError:
            self.driver.switch_to.window(self.driver.window_handles[0])
    
    def previous_tab(self):
        current_tab = self.driver.window_handles.index \
            (self.driver.current_window_handle)

        self.driver.switch_to.window(self.driver.window_handles[current_tab-1])

class Error_Window(QMainWindow):

    def __init__(self, *args, **kwargs) -> None:
        super(Error_Window, self).__init__(*args, **kwargs)

        self.setWindowTitle("Error")
        self.setGeometry(1100, 200, 10, 10)

        self.centralWidget = QWidget()

        self.layout = QVBoxLayout()
        
        self.error_message_label = QLabel()

        self.layout.addWidget(self.error_message_label)

        self.centralWidget.setLayout(self.layout)

        self.setCentralWidget(self.centralWidget)

    def set_message(self, message):
        self.error_message_label.setText(message)

class Recruiter_Window(QMainWindow):

    def __init__(self, recruiter, *args, **kwargs) -> None:
        super(Recruiter_Window, self).__init__(*args, **kwargs)

        self.recruiter = recruiter

        self.setWindowTitle("Recruiter")
        self.setGeometry(1100, 200, 250, 100)

        self.centralWidget = QWidget()

        self.on_label = QLabel('ON')
        self.on_radio_button = QRadioButton()
        self.off_label = QLabel('OFF')
        self.off_radio_button = QRadioButton()
        self.blank_label = QLabel()
        self.village_label = QLabel('VILLAGE')
        self.village_combo_box = QComboBox()
        self.attack_radio_button = QRadioButton()
        self.defense_radio_button = QRadioButton()
        self.attack_label = QLabel('ATTACK')
        self.defense_label = QLabel('DEFENSE')

        self.on_off_group = QButtonGroup()
        self.attack_defense_group = QButtonGroup()

        self.main_layout = QVBoxLayout()
        self.sub_layout_1 = QHBoxLayout()
        self.sub_layout_2 = QHBoxLayout()
        self.sub_layout_3 = QHBoxLayout()

        self.on_off_group.addButton(self.on_radio_button)
        self.on_off_group.addButton(self.off_radio_button)

        self.attack_defense_group.addButton(self.attack_radio_button)
        self.attack_defense_group.addButton(self.defense_radio_button)

        self.sub_layout_1.addWidget(self.on_label)
        self.sub_layout_1.addWidget(self.on_radio_button)
        self.sub_layout_1.addWidget(self.off_label)
        self.sub_layout_1.addWidget(self.off_radio_button)

        self.sub_layout_2.addWidget(self.village_label)
        self.sub_layout_2.addWidget(self.village_combo_box)

        self.sub_layout_3.addWidget(self.attack_label)
        self.sub_layout_3.addWidget(self.attack_radio_button)
        self.sub_layout_3.addWidget(self.defense_label)
        self.sub_layout_3.addWidget(self.defense_radio_button)

        self.main_layout.addLayout(self.sub_layout_1)
        self.main_layout.addWidget(self.blank_label)
        self.main_layout.addLayout(self.sub_layout_2)
        self.main_layout.addLayout(self.sub_layout_3)

        self.centralWidget.setLayout(self.main_layout)

        self.setCentralWidget(self.centralWidget)

        self.on_radio_button.setChecked(True)

        self.on_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.off_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.village_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.attack_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.defense_label.setAlignment(Qt.AlignRight | Qt.AlignCenter)

        self.on_radio_button.clicked.connect(self.recruiter.turn_on)
        self.off_radio_button.clicked.connect(self.recruiter.turn_off)

class Login_Work(QObject):
    finished = pyqtSignal()

    def __init__(self, parent):
        super(Login_Work, self).__init__()

        self.driver = parent.driver
        self.user_input = parent.user_input
        self.password_input = parent.password_input

    def run(self):
        self.driver.get("https://www.tribalwars.com.br/")

        wait = WebDriverWait(self.driver, 1)
        try:
            wait.until(EC.visibility_of_element_located((By.ID, 'user'))) \
                .send_keys(self.user_input.text())
            wait.until(EC.visibility_of_element_located((By.ID, 'password'))) \
                .send_keys(self.password_input.text(), Keys.RETURN)
        except TimeoutException:
            pass
        
        self.finished.emit()

class Run_Pending_Work(QObject):
    finished = pyqtSignal()

    def __init__(self, schedule):
        super(Run_Pending_Work, self).__init__()

        self.schedule = schedule

    def run(self):
        while True:
            self.schedule.run_pending()
            sleep(1)
