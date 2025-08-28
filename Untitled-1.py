import os
import csv
import time


cwd = os.getcwd()

def FileExists(path: str) -> bool:
    try:
        with open(path, "r") as f:
            f.close()
        return True
    except:
        return False

class Stack: 
    def __init__(self):
        self.stack = []
    
    def append(self, item):
        self.stack.append(item)

    def top(self):
        if len(self.stack) <= 0:
            return None
        return self.stack[-1]
    
    def pop(self):
        self.stack.pop()

    def empty(self):
        return not bool(len(self.stack))

class User:
    def __init__(self):
        self.name: str = None
        self.borrowed: int = 0

class Book:
    def __init__(self):
        self.title: str = None
        self.borrowed: int = 0

class Loan:
    def __init__(self):
        self.user_id : int = None
        self.user_name : str = None
        self.book_id : str = None
        self.book_title : str = None
        self.loan_date : str = None
        self.deadline : str = None
        self.loan_date_timestamp : float = None

    def __str__(self):
        deadline = self.deadline if None else "No devuelto"
        return str(self.user_id) + ", " + self.user_name + ", " + self.book_id + ", " + self.book_title + ", " + self.loan_date + ", " + deadline

users = {}
books = {}
loans = []
history = Stack()

def LoadUsers(path: str) -> None:
    with open(path, "r") as f:
        reader = csv.reader(f)
        for line in reader:
            user: User = User()
            user.name = line[1]
            users[int(line[0])] = user
        f.close()

def LoadBooks(path: str) -> None:
    with open(path, "r") as f:
        reader = csv.reader(f)
        for line in reader:
            book: Book = Book()
            book.title = line[1]
            books[line[0]] = book
        f.close()

def ReadLoans(path: str) -> None:
    unsorted_loans = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        for line in reader:
            loan: Loan = Loan()
            loan.user_id = int(line[0])
            if users.get(loan.user_id) == None:
                print("El id de usuario " + str(loan.user_id)+ " no ha sido registrado")
                break
            loan.user_name = line[1]
            loan.book_id = line[2]
            if books.get(loan.book_id) != None:
                users[loan.user_id].borrowed = users[loan.user_id].borrowed + 1
                books[loan.book_id].borrowed = books[loan.book_id].borrowed + 1
            else:
                print("Libro con id " + loan.book_id + " no encontrado")
                break

            loan.book_title = line[3]
            loan.loan_date = line[4]
            loan.loan_date_timestamp = time.mktime(time.strptime(loan.loan_date,"%Y-%d-%m"))
            if len(line) == 6:
                loan.deadline = line[5]
            unsorted_loans.append(loan)
        loans.extend(sorted(unsorted_loans, key= lambda x: x.loan_date_timestamp, reverse= True))
        f.close()

def GenerateHistoryReport(path: str, items: list[Loan]) -> None:
    with open(path, "a", newline="\n") as f:
        f.write("<table>")
        if len(items) != 0:
            f.write("<caption><h3>")
            f.write("Historial de prestamos")
            f.write("</h3></caption>")
            f.write("<tr>")
            f.write("<th>ID usuario</th>")
            f.write("<th>Usuario</th>")
            f.write("<th>ID del libro</th>")
            f.write("<th>Titulo del libro</th>")
            f.write("<th>Fecha del prestamo</th>")
            f.write("<th>Fecha de devolucion</th>")
            f.write("</tr>")

        for loan in items:
            f.write("<tr>")
            for value in loan.__dict__.values():
                f.write("<td>")
                if value == None:
                    f.write("No entregado")
                else:
                    if value == loan.loan_date_timestamp:
                        continue
                    else:
                        f.write(str(value))
                f.write("</td>")
            f.write("</tr>")

        f.write("</table>")
        f.close()

def GenerateUserReport(path: str, items: dict[User]) -> None:
    with open(path, "a", newline="\n") as f:
        f.write("<table>")
        if len(items) != 0:
            f.write("<caption><h3>")
            f.write("Listado de usuarios")
            f.write("</h3></caption>")
            f.write("<tr>")
            f.write("<th>ID usuario</th>")
            f.write("<th>Usuario</th>")
            f.write("<th>Cantidad de prestamos</th>")
            f.write("</tr>")

        for user_id in items:
            f.write("<tr>")
            user: User = users[user_id]
            f.write("<td>")
            f.write(str(user_id))
            f.write("</td>")
            for value in user.__dict__.values():
                f.write("<td>")
                f.write(str(value))
                f.write("</td>")
            f.write("</tr>")

        f.write("</table>")
        f.close()

def GenerateBookReport(path: str, items: dict[Book]) -> None:
    with open(path, "a", newline="\n") as f:
        f.write("<table>")
        if len(items) != 0:
            f.write("<caption><h3>")
            f.write("Libros prestados")
            f.write("</h3></caption>")
            f.write("<tr>")
            f.write("<th>ID del libro</th>")
            f.write("<th>Titulo del libro</th>")
            f.write("</tr>")
            for book_id in items:
                book = items[book_id]
                if book.borrowed > 0:
                    f.write("<tr>")
                    f.write("<td>")
                    f.write(book_id)
                    f.write("</td>")
                    f.write("<td>")
                    f.write(book.title)
                    f.write("</td>")
                    f.write("</tr>")
                        
        f.write("</table>")
        f.close()

def GetTopBook() -> Book:
    borrowed_books = []
    for book_id in books:
        borrowed_books.append(books[book_id].borrowed)

    top_book = max(borrowed_books)
    for book_id in books:
        book = books[book_id]
        if book.borrowed == top_book:
            return book
    return None

def GetTopUser() -> User:
    borrowed_books = []
    for user_id in users:
        borrowed_books.append(users[user_id].borrowed)

    top_user = max(borrowed_books)
    for user_id in users:
        user = users[user_id]
        if user.borrowed == top_user:
            return user
    return None

def GenerateLoanReport(path: str, items: list[Loan]) -> None:
    with open(path, "a", newline="\n") as f:
        f.write("<table>")
        if len(items) != 0:
            f.write("<caption><h3>")
            f.write("Estadisticas de Prestamos")
            f.write("</h3></caption>")
            f.write("<tr>")
            f.write("<th>Total de libros prestados</th>")
            f.write("<th>Libro mas prestado</th>")
            f.write("<th>Usuario mas activo</th>")
            f.write("<th>Total de usuarios unicos</th>")
            f.write("</tr>")

            total_loans = len(loans)
            top_book = GetTopBook()
            top_user = GetTopUser()

            f.write("<td>")
            f.write(str(total_loans))
            f.write("</td>")
            f.write("<td>")
            f.write(top_book.title)
            f.write("</td>")
            f.write("<td>")
            f.write(top_user.name)
            f.write("</td>")
            f.write("<td>")
            f.write(str(len(users)))
            f.write("</td>")

        f.write("</table>")
        f.close()


def GenerateOverdueReport(path: str, items: list[Loan]) -> None:
    today = time.localtime(time.time())
    with open(path, "a", newline="\n") as f:
        f.write("<table>")
        if len(items) != 0:
            f.write("<caption><h3>")
            f.write("Prestamos vencidos")
            f.write("</h3></caption>")
            f.write("<tr>")
            f.write("<th>ID usuario</th>")
            f.write("<th>Usuario</th>")
            f.write("<th>ID del libro</th>")
            f.write("<th>Titulo del libro</th>")
            f.write("<th>Fecha del prestamo</th>")
            f.write("<th>Fecha de devolucion</th>")
            f.write("</tr>")

        for loan in items:
            f.write("<tr>")
            if loan.deadline != None:
                overdue = False
                deadline = list(map(lambda x : int(x), loan.deadline.split("-")))
                if deadline[0] < today.tm_year or (deadline[0] <= today.tm_year and deadline[1] < today.tm_mon) or (deadline[0] <= today.tm_year and deadline[1] <= today.tm_mon and deadline[2] < today.tm_mday):
                    overdue = True

                if overdue:
                    for value in loan.__dict__.values():
                        f.write("<td>")
                        f.write(str(value))
                        f.write("</td>")
            f.write("</tr>")

        f.write("</table>")
        f.close()

def LoadResources(path_users: str, path_books: str, path_loans: str) -> None:
    LoadUsers(path_users)
    LoadBooks(path_books)
    ReadLoans(path_loans)

def GenerateReports(path: str) -> None:
    with open(path, "w") as f: 
        f.close()
    GenerateHistoryReport(path, loans)
    GenerateUserReport(path, users)
    GenerateBookReport(path, books)
    GenerateLoanReport(path, loans)
    GenerateOverdueReport(path, loans)
    pass


LoadResources(cwd + "/users.txt", cwd + "/books.txt", cwd + "/file.lfa")
GenerateReports(cwd + "/report.html")
'''
while True:
    opt = input("Que desea realizar?\n1. Cargar usuarios\n2. Cargar libros\n3. Cargar registro de préstamos desde archivo\n4. Mostrar historial de prestamos\n5. Mostrar listados de usuarios unicos\n6. Mostrar listado de libros prestados\n7. Mostrar estadisticas de prestamos\n8. Mostrar prestamos vencidos\n9. Exportar todos los reportes a HTML\n10. Salir\n")
    opt = opt.strip()
    if not opt.isdigit():
        print("Formato ingresado invalido, intentelo de nuevo")
        continue
    
    opt = int(opt)
    if opt == 1:
        
        pass
    elif opt == 2:
        pass
    elif opt == 3:
        
        pass
    elif opt == 4:
        for loan in loans:
            print(loan)
        pass
    elif opt == 5:
        print("Usuarios unicos:")
        for user_id in users:
            print(str(user_id) + ", " + users[user_id].name)
        pass
    elif opt == 6:
        print("Libros Prestados:")
        for book_id in books:
            book: Book = books[book_id]
            if book.borrowed > 0:
                print(book_id + ", " + book.title)
                
        pass
    elif opt == 7:
        print("Total de libros prestados: " + str(len(loans)))
        print("Libro mas prestado: " + GetTopBook().title)
        print("Usuario mas activo: " + GetTopUser().name)
        pass
    elif opt == 8:
        pass
    elif opt == 9:
        print("Exportando reportes...")
        GenerateReports()
        print("Los reportes se han exportado con exito!")
        pass
    elif opt == 10:
        break
    else:
        print("La opcion ingresada no existe, intentelo de nuevo")
'''
