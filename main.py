# requirements: PyQt5
# run: python todo_qtpy.py

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QScrollArea,
                             QLineEdit, QCheckBox, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5 import uic


class TaskWidget(QWidget):
    PRIORITY_COLORS = {
        'Low': '#10b981',
        'Medium': '#f59e0b',
        'High': '#ef4444'
    }

    def __init__(self, task_text, priority):
        super().__init__()
        self.task_text = task_text
        self.priority = priority
        self.is_completed = False

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)

        self.checkbox = QCheckBox()
        self.checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """)

        self.priority_label = QLabel(self.priority)
        self.priority_label.setFixedWidth(65)
        self.priority_label.setAlignment(Qt.AlignCenter)
        self.update_priority_style()

        self.task_label = QLabel(self.task_text)
        self.task_label.setWordWrap(True)
        self.task_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #1f2937;
            }
        """)

        self.delete_btn = QPushButton("✕")
        self.delete_btn.setFixedSize(30, 30)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                border: 0;
                border-radius: 15px;
                background-color: #ef4444;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover { background-color: #dc2626; }
            QPushButton:pressed { background-color: #b91c1c; }
        """)

        layout.addWidget(self.checkbox)
        layout.addWidget(self.priority_label)
        layout.addWidget(self.task_label, 1)
        layout.addWidget(self.delete_btn)

    def connect_signals(self):
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)

    def update_priority_style(self):
        color = self.PRIORITY_COLORS.get(self.priority)
        self.priority_label.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                font-size: 11px;
                font-weight: bold;
                border-radius: 4px;
                padding: 4px 8px;
            }}
        """)

    def on_checkbox_changed(self, state):
        self.is_completed = (state == Qt.Checked)

        if self.is_completed:
            self.task_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #9ca3af;
                    text-decoration: line-through;
                }
            """)
        else:
            self.task_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #1f2937;
                }
            """)

    def get_delete_button(self):
        return self.delete_btn


class TodoManager:

    def __init__(self, task_layout):
        self.task_layout = task_layout
        self.tasks = []

    def add_task(self, task_text, priority):
        task_widget = TaskWidget(task_text, priority)

        task_widget.get_delete_button().clicked.connect(
            lambda: self.delete_task(task_widget)
        )

        idx_before_spacer = self.task_layout.count() - 1
        self.task_layout.insertWidget(idx_before_spacer, task_widget)

        self.tasks.append(task_widget)
        return task_widget

    def delete_task(self, task_widget):
        if task_widget in self.tasks:
            self.tasks.remove(task_widget)
        self.task_layout.removeWidget(task_widget)
        task_widget.deleteLater()



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_task_area()
        self.connect_signals()
        self.show()

    def setup_ui(self):
        uic.loadUi('todo.ui', self)
        self.setWindowTitle("To Do List")

        self.addButton = self.findChild(QPushButton, "pushButton")
        self.lineEdit = self.findChild(QLineEdit, "lineEdit")
        self.scrollArea = self.findChild(QScrollArea, "scrollArea")
        self.priority_combo = self.findChild(QComboBox, "comboBox")

    def setup_task_area(self):
        self.task_host = QWidget()
        self.task_layout = QVBoxLayout(self.task_host)
        self.task_layout.setContentsMargins(0, 0, 0, 0)
        self.task_layout.setSpacing(5)



        self.task_layout.addStretch()

        self.scrollArea.setWidget(self.task_host)

        self.task_host.setStyleSheet("background-color: #f9fafb;")

        self.todo_manager = TodoManager(self.task_layout)


    def connect_signals(self):
        self.addButton.clicked.connect(self.on_add_task)
        self.lineEdit.returnPressed.connect(self.on_add_task)

    def on_add_task(self):
        task_text = self.lineEdit.text().strip()

        if not task_text:
            return

        priority = self.priority_combo.currentText()

        self.todo_manager.add_task(task_text, priority)

        self.lineEdit.clear()
        self.lineEdit.setFocus()





app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())