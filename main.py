from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, QAction, QTableWidget, QTableWidgetItem, \
     QDialog, QComboBox
from PyQt5.QtCore import Qt
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Managment System")

        # Adding Menu Bar:
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        
        search_action = QAction("Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)
        

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number,
                                   QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()
        
    def search(self):
        dialog = SearchDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        # Add Student Name Widget:
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        # Add Combo Box Of Courses:
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)
        
        # Add Mobile Number Widget:
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)
        
        # Add A Submit Button:
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)
        
        self.setLayout(layout)
        
    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        # Set Window Title And Size:
        self.setWindowTitle("Search For A Student")
        self.setFixedHeight(300)
        self.setFixedWidth(300)
        
        # Create Layout And Input Widgets:
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_student)
        layout.addWidget(search_button)
        
        self.setLayout(layout)
        
    def search_student(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        row = list(result)[0]
        print(row)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        print(items)
        for item in items:
            print(item)
            # It Shadows the name cells that match the searched name, table.item is a method that takes 2 arguments
            # 1st is the row index, 2nd is the column index
            main_window.table.item(item.row(), 1).setSelected(True)
        
        
        cursor.close()
        connection.close()
        

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec_())
