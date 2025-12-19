from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, QAction, QTableWidget, QTableWidgetItem, \
     QDialog, QComboBox, QToolBar, QStatusBar, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Managment System")
        self.setMinimumSize(800, 600)

        # Adding Menu Bar:
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)
        
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ("ID", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        
        # Create Toolbar And Add Toolbar Elements:
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Create Status Bar And Add Status Bar Elements:
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        # Detect A Cell Click:
        self.table.cellClicked.connect(self.cell_clicked)
        
    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)
        
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)
        
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)
                
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)
        
        
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
        
    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
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
        
class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        
        layout = QVBoxLayout()
        
        # Get ID From Selected Row:
        index = main_window.table.currentRow()
        self.student_id = main_window.table.item(index, 0).text()
        
        # Get Student Name From Selected Row:
        name = main_window.table.item(index, 1).text()
        
        # Add Student Name Widget:
        self.student_name = QLineEdit(name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)
        
        # Get Course Name From Selected Row:
        course = main_window.table.item(index, 2).text()
        
        # Add Combo Box Of Courses:
        self.course_name = QComboBox() 
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course)
        layout.addWidget(self.course_name)
        
        # Get Mobile Number From Selected Row:
        mobile = main_window.table.item(index, 3).text()
        
        # Add Mobile Number Widget:
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)
        
        # Add A Submit Button:
        button = QPushButton("Register")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)
        
        self.setLayout(layout)
        
    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile.text(),
                        self.student_id))
        
        connection.commit()
        cursor.close()
        connection.close()
        # Refresh The Table:
        main_window.load_data()
        
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Confirmation")
        
        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete this student?")
        yes = QPushButton("Yes")
        no = QPushButton("No")
        
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)
        
        yes.clicked.connect(self.delete_student)
        
    def delete_student(self):
        # Get Index And Student ID:
        index = main_window.table.currentRow()
        id = main_window.table.item(index, 0).text()
        
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE from students WHERE id = ?", (id, ))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        
        self.close()
        confirmation_message = QMessageBox()
        confirmation_message.setWindowTitle("Success")
        confirmation_message.setText("The Record Was Deleted Successfully")
        confirmation_message.exec_()
  
class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app was created during the course "The python mega course".
        Feel free to modify and reuse this app.
        """
        self.setText(content)
        
        
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec_())
