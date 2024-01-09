from PyQt6 import QtWidgets, uic, QtGui, QtCore
import sys

class UI(QtWidgets.QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi('library.ui',self)
        self.show()
        
        self.authors = []
        
        #buttons
        self.addauthor.clicked.connect(self.addAuthor)
        self.okay.clicked.connect(self.submitform)
        self.close_form.clicked.connect(self.close)
        self.issued_input.stateChanged.connect(self.issued)
        
        #subcategories
        self.subcategories = {
            "Database Systems": ["ERD", "SQL", "OLAP", "Data Mining"],
            "OOP": ["C++", "Java"],
            "Artificial Intelligence": ["Machine Learning", "Robotics", "Computer Vision"]
        }
        self.categories()
        self.category_input.currentIndexChanged.connect(self.sub_categories)
        
        
    def addAuthor(self):
        author_name = self.authorname_input.text()
        if author_name:
            self.authors.append(author_name)
            self.listofauthors.addItem(author_name)
            self.authorname_input.clear()
        
    def categories(self):
        categories = ["Database Systems","OOP","Artificial Intelligence"]
        self.category_input.addItems(categories)
        
    def sub_categories(self):
        subcategory = self.subcategories.get(self.category_input.currentText(), [])
        self.subcategory_input.clear()
        self.subcategory_input.addItems(subcategory)
        
        
    def issued(self,state):
        self.issuedby_input.setEnabled(state)
        self.issuedon_input.setEnabled(state)    
        
    def submitform(self):
        errorlist = []
        
        
        name = self.name_input.text()
        if len(name) == 0:
            errorlist.append("Please add your name")
        
        
        isbn = self.isbn_input.text()
        if len(isbn)>12:
            errorlist.append("The Length of ISBN is greater than 12")
        
        
        purchase_date = self.purchasedon_input.date().toPyDate()
        today = QtCore.QDate.currentDate().toPyDate()
        if purchase_date >= today:
            errorlist.append("Purchased On Date is greater than today")
            
        
        if self.reference.isChecked():
            self.book_type = "Reference Book"
        elif self.textbook.isChecked():
            self.book_type = "Text Book" 
        elif self.journal.isChecked():
            self.book_type = "Journal"
        else:
            errorlist.append("Please select a book type")
        
        if self.book_type == "Journal":
            if len(self.authors) > 0:
                errorlist.append("Book of Journal Type should have no authors")
        else:
            if len(self.authors) == 0:
                errorlist.append("Reference Books or Text Books should have atleast one author")
        
        issued_box = self.issued_input.isChecked()
        issued_by = self.issuedby_input.text()
        issued_on = self.issuedon_input.date().toPyDate()
        
        if self.issued_input.isChecked():
            if not (issued_by):
                errorlist.append("Issued to is empty")
            if not (today > issued_on > purchase_date):
                errorlist.append("Issued Date is not between Purchased on and Today's Date")
        
        # self.checkerrors()
        if len(errorlist)>0:
            error =  "\n".join(errorlist)
            QtWidgets.QMessageBox.warning(self,"Verification Failed", error)
        else:
            QtWidgets.QMessageBox.information(self,"Confirmation", "Book Added Successfully")
        
    # def checkerrors(self, errorlist):
    #     if len(errorlist)>0:
    #         error =  "\n".join(errorlist)
    #         QtWidgets.QMessageBox.warning(self,"Verification Failed", error)
    #     else:
    #         QtWidgets.QMessageBox.information(self,"Confirmation", "Book Added Successfully")







if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec())