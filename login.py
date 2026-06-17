import bcrypt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
from PyQt5.QtCore import Qt
import database

class Session:
    user_id = None
    username = None
    full_name = None
    
    @classmethod
    def clear(cls):
        cls.user_id = None
        cls.username = None
        cls.full_name = None
        
    @classmethod
    def set_user(cls, user_id, username, full_name):
        cls.user_id = user_id
        cls.username = username
        cls.full_name = full_name
        
    @classmethod
    def is_logged_in(cls):
        return cls.user_id is not None


class LoginWidget(QWidget):
    def __init__(self, main_app, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        
        card = QFrame()
        card.setFixedWidth(480)
        card.setStyleSheet("background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px;")
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(35, 40, 35, 40)
        card_layout.setSpacing(15)
        
        title_lbl = QLabel("Retail Price\nOptimization Dashboard")
        title_lbl.setStyleSheet("font-size: 16pt; font-weight: bold; color: #4F46E5; border: none; line-height: 1.2;")
        title_lbl.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_lbl)
        
        sub_lbl = QLabel("Sign in to continue")
        sub_lbl.setStyleSheet("color: #64748B; font-size: 10pt; border: none;")
        sub_lbl.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(sub_lbl)
        card_layout.addSpacing(5)
        
        self.un_input = QLineEdit()
        self.un_input.setPlaceholderText("Username")
        self.un_input.setMinimumHeight(40)
        self.un_input.setStyleSheet("border: 1px solid #CBD5E1; border-radius: 6px; padding: 8px; font-size: 10pt; color: #1E293B; background-color: #FFFFFF;")
        card_layout.addWidget(self.un_input)
        
        self.pw_input = QLineEdit()
        self.pw_input.setPlaceholderText("Password")
        self.pw_input.setEchoMode(QLineEdit.Password)
        self.pw_input.setMinimumHeight(40)
        self.pw_input.setStyleSheet("border: 1px solid #CBD5E1; border-radius: 6px; padding: 8px; font-size: 10pt; color: #1E293B; background-color: #FFFFFF;")
        self.pw_input.returnPressed.connect(self.run_login)
        card_layout.addWidget(self.pw_input)
        card_layout.addSpacing(5)
        
        login_btn = QPushButton("Sign In")
        login_btn.setMinimumHeight(40)
        login_btn.setStyleSheet("background-color: #4F46E5; color: white; font-weight: bold; border-radius: 6px; font-size: 10pt; border: none;")
        login_btn.clicked.connect(self.run_login)
        card_layout.addWidget(login_btn)
        card_layout.addSpacing(5)
        
        signup_layout = QHBoxLayout()
        signup_layout.setContentsMargins(0, 0, 0, 0)
        signup_layout.setAlignment(Qt.AlignCenter)
        
        signup_msg = QLabel("Don't have an account?")
        signup_msg.setStyleSheet("border: none; color: #475569;")
        signup_layout.addWidget(signup_msg)
        
        signup_btn = QPushButton("Sign Up")
        signup_btn.setStyleSheet("background-color: transparent; color: #4F46E5; border: none; font-weight: bold; text-decoration: underline;")
        signup_btn.clicked.connect(lambda: self.main_app.switch_screen("signup"))
        signup_layout.addWidget(signup_btn)
        
        card_layout.addLayout(signup_layout)
        layout.addWidget(card)
        
    def run_login(self):
        username = self.un_input.text().strip()
        password = self.pw_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Required Fields", "Please enter username and password.")
            return
            
        try:
            rows = database.execute_query(
                "SELECT UserID, FullName, PasswordHash FROM Users WHERE Username = ?", 
                (username,), fetch=True
            )
            
            if not rows:
                QMessageBox.critical(self, "Failed", "Invalid username or password.")
                return
                
            user_id, fullname, pw_hash = rows[0]
            
            if bcrypt.checkpw(password.encode('utf-8'), pw_hash.encode('utf-8')):
                Session.set_user(user_id, username, fullname)
                self.un_input.clear()
                self.pw_input.clear()
                self.main_app.start_dashboard()
            else:
                QMessageBox.critical(self, "Failed", "Invalid username or password.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to authenticate: {e}")
