import bcrypt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
from PyQt5.QtCore import Qt
import database

class SignupWidget(QWidget):
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
        
        title_lbl = QLabel("Create Account")
        title_lbl.setStyleSheet("font-size: 16pt; font-weight: bold; color: #4F46E5; border: none;")
        title_lbl.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_lbl)
        
        sub_lbl = QLabel("Join the Pricing Platform")
        sub_lbl.setStyleSheet("color: #64748B; font-size: 10pt; border: none;")
        sub_lbl.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(sub_lbl)
        card_layout.addSpacing(5)
        
        self.fn_input = QLineEdit()
        self.fn_input.setPlaceholderText("Full Name")
        self.fn_input.setMinimumHeight(40)
        self.fn_input.setStyleSheet("border: 1px solid #CBD5E1; border-radius: 6px; padding: 8px; font-size: 10pt; color: #1E293B; background-color: #FFFFFF;")
        card_layout.addWidget(self.fn_input)
        
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
        card_layout.addWidget(self.pw_input)
        card_layout.addSpacing(5)
        
        register_btn = QPushButton("Register Account")
        register_btn.setMinimumHeight(40)
        register_btn.setStyleSheet("background-color: #4F46E5; color: white; font-weight: bold; border-radius: 6px; font-size: 10pt; border: none;")
        register_btn.clicked.connect(self.run_signup)
        card_layout.addWidget(register_btn)
        card_layout.addSpacing(5)
        
        back_btn = QPushButton("Back to Sign In")
        back_btn.setStyleSheet("background-color: transparent; color: #64748B; border: none; font-weight: bold; text-decoration: underline;")
        back_btn.clicked.connect(lambda: self.main_app.switch_screen("login"))
        card_layout.addWidget(back_btn)
        
        layout.addWidget(card)
        
    def run_signup(self):
        fullname = self.fn_input.text().strip()
        username = self.un_input.text().strip()
        password = self.pw_input.text().strip()
        
        if not fullname or not username or not password:
            QMessageBox.warning(self, "Required Fields", "All fields are required.")
            return
            
        try:
            # Check unique username
            rows = database.execute_query("SELECT COUNT(*) FROM Users WHERE Username = ?", (username,), fetch=True)
            if rows[0][0] > 0:
                QMessageBox.warning(self, "Username Taken", "Username already exists. Please choose a different one.")
                return
                
            # Hash password
            salt = bcrypt.gensalt()
            pw_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
            
            # Register user
            database.execute_query(
                "INSERT INTO Users (FullName, Username, PasswordHash) VALUES (?, ?, ?)",
                (fullname, username, pw_hash)
            )
            
            QMessageBox.information(self, "Signup Successful", "Account created successfully! You can now log in.")
            self.fn_input.clear()
            self.un_input.clear()
            self.pw_input.clear()
            self.main_app.switch_screen("login")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to register account: {e}")
