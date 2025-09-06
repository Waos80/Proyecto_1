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
        deadline = self.deadline
        if deadline == None:
            deadline = "No devuelto"
        return str(self.user_id) + ", " + self.user_name + ", " + self.book_id + ", " + self.book_title + ", " + self.loan_date + ", " + deadline

Letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÁÉÍÓÚáéíóúÑñ' "
Book_Letters = "ÁÉÍÓÚáéíóúÑñ ".join(chr(i) for i in range(128))

def is_ID(token: str) -> bool:
    return len(token) == 4 and all(c.isdigit() for c in token)

def is_username(token: str) -> bool:
    return all(c in Letters for c in token) > 0

def is_bookname(token: str) -> bool:
    return all(c in Book_Letters for c in token) > 0

def is_IDLib(token: str) -> bool:
    return token.startswith("LIB") and len(token) == 6 and token[3:].isdigit()

def is_Date(token: str) -> bool:
    if len(token) != 10:
        return False
    if token[4] != "-" or token[7] != "-":
        return False
    year = token[:4]
    month = token[5:7]
    day = token[8:]
    if not(year.isdigit() and month.isdigit() and day.isdigit()):
        return False
    year = int(year)
    month = int(month)
    day = int(day)
    if year < 1970 or year > 2027:
        return False
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    if month in [4, 6, 9, 11] and day > 30:
        return False
    if month == 2:
        leap = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
        if day > (29 if leap else 28):
            return False
    return True

def token_Identifier(token: str, Tidentiflag: str) -> bool:
    if is_ID(token) and Tidentiflag == "0":
        return True
    elif is_username(token) and Tidentiflag == "1":
        return True
    elif is_IDLib(token) and Tidentiflag == "2":
        return True
    elif is_bookname(token) and Tidentiflag == "3":
        return True
    elif is_Date(token) and (Tidentiflag == "4" or Tidentiflag == "5"):
        return True
    else:
        return False
    
def TTErrors(token: str, flag: str) -> None:
    if flag == "0": #Error en el ID
        if len(token) > 4:
            TTError = f"EL digito '{token[5]}' en la posición 5 excede la longitud máxima para el ID {token}"
            return TTError
        elif len(token) < 4:
            TTError = f"El ID: {token} no cumple con la cantidad mínima de digitos para un ID"
            return TTError
        else:
            for i, c in enumerate(token):
                if not(c.isdigit()):
                    TTError = f"El caracter '{token[i]}', en la posición {i + 1}, del token {token} no es un digito."
                    return TTError
    elif flag == "1": #Error en el nombre de usuario
        for i, c in enumerate(token):
            if not(c in Letters):
                TTError = f"El caracter en la posición {i + 1}: '{c}' no es válido para el token {token}."
                return TTError
    elif flag == "2": #Error en el ID de libro
        LibLetters = "LIB"
        LibDigits = token[3:]
        for i, c in enumerate(token[:3]):
            if not(c in LibLetters):
                TTError = f"El caracter en la posición {i + 1}: '{c}' no es válido para el token {token}."
                return TTError
        if len(LibDigits) > 3:
            TTError = f"EL ID de libro {token} excede la cantidad máxima de digitos."   
            return TTError
        elif len(LibDigits) < 3:
            TTError = f"El ID del libro {token} no cumple con la cantidad mínima de digitos."
            return TTError
        for i, c in enumerate(token[3:]):
            if not(c.isdigit()):
                TTError = f"El caracter '{c}', en la posición {i + 4} del token {token} no es un digito."
                return TTError
    elif flag == "3": #Error en el nombre del libro
        for i, c in enumerate(token):
            if not(c in Book_Letters):
                TTError = f"El caracter número {i + 1}: '{c}' no es válido para el token {token}"
                return TTError 
    elif flag == "4": #Error en la fecha del préstamo
        if len(token) > 10:
            TTError = f"El caracter '{token[10]}' en la posición 11, excede la cantidad máxima de caracteres para el token"
            return TTError
        elif len(token) < 10:
            TTError = f"el token {token} no cumple con la cantidad mínima de caracteres para una fecha\nCaracter {token[len(token) - 1]} en la posición {len(token) + 1}."
            return TTError
        if token[4] != "-":
            TTError = f"El caracter '{token[4]}' en la posición 5 no es válido para una fecha."
            return TTError
        elif token[7] != "-":
            TTError = f"El caracter '{token[7]}' en la posición 8 no es válido para una fecha."
        deadline = list(map(lambda x : int(x), token.split("-")))
        year = deadline[0]
        month = deadline[1]
        day = deadline[2]
        for i, c in enumerate(str(deadline[0])):
            if not(c.isdigit()):
                TTError = f"El caracter '{c}', en la posición {i} no es un digito."
                if year < 2020:
                    TTError = TTError + f"\nLa fecha {token} es menor a la permitida"
                elif year > 2025:
                    TTError = f"\nLa fecha {token} es mayor a la permitida"
                return TTError
        for i, c in enumerate(str(deadline[1])):
            if not(c.isdigit()):
                TTError = f"El caracter '{c}', en la posición {i} no es un digito."
                return TTError
            elif month < 1 or month > 12:
                TTError = f"{month} no es un mes válido."
                return TTError
            elif month in [4, 6, 9, 11] and day > 30:
                TTError = f"El mes {month} no puede tener {day} días."
                return TTError
            elif month == 2:
                leap = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
                if day > (29 if leap else 28):
                    TTError = f"El mes de febrero de año {year} es bisciesto, no puede tener {day} días."
                    return TTError
        for i, c in enumerate(str(deadline[2])):
            if not(c.isdigit()):
                TTError = f"El caracter '{c}', en la posición {i} no es un digito."
                return TTError
    elif flag == "5": #Error en la fecha de devolución del libro
        if len(token) > 10:
            TTError = f"El caracter '{token[10]}' en la posición 11, excede la cantidad máxima de caracteres para el token"
            return TTError
        elif len(token) < 10:
            TTError = f"el token {token} no cumple con la cantidad mínima de caracteres para una fecha\nCaracter {token[len(token)]} en la posición {len(token) + 1}."
            return TTError
        if token[4] != "-":
            TTError = f"El caracter '{token[4]}' en la posición 5 no es válido para una fecha."
            return TTError
        elif token[7] != "-":
            TTError = f"El caracter '{token[7]}' en la posición 8 no es válido para una fecha."
        deadline = list(map(lambda x : int(x), token.split("-")))
        year = deadline[0]
        month = deadline[1]
        day = deadline[2]
        for i, c in enumerate(str(deadline[0])):
            if not(c.isdigit()):
                TTError = f"El caracter '{c}', en la posición {i} no es un digito."
                if year < 2020:
                    TTError = TTError + f"\nLa fecha {token} es menor a la permitida"
                elif year > 2025:
                    TTError = f"\nLa fecha {token} es mayor a la permitida"
                return TTError
        for i, c in enumerate(str(deadline[1])):
            if not(c.isdigit()):
                TTError = f"El caracter '{c}', en la posición {i} no es un digito."
                return TTError
            elif month < 1 or month > 12:
                TTError = f"{month} no es un mes válido."
                return TTError
            elif month in [4, 6, 9, 11] and day > 30:
                TTError = f"El mes {month} no puede tener {day} días."
                return TTError
            elif month == 2:
                leap = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
                if day > (29 if leap else 28):
                    TTError = f"El mes de febrero de año {year} es bisciesto, no puede tener {day} días."
                    return TTError
        for i, c in enumerate(str(deadline[2])):
            if not(c.isdigit()):
                TTError = f"El caracter '{c}', en la posición {i} no es un digito."
                return TTError

users = {}
books = {}
loans = []
history = Stack()

def LoadUsers(path: str) -> None:
    flag = "0"
    with open(path, "r",encoding="utf-8") as f:
        reader = csv.reader(f)
        for line_numer, line in enumerate(reader):
            user: User = User()
            for i, token in enumerate(line):
                reconocido = False
                Tidentiflag = str(i)
                for tipo in range(2):
                    if token_Identifier(token, Tidentiflag):
                        reconocido = True
                        if i == 0:
                            users[int(line[0])] = user
                            flag = "1"
                            Tidentiflag = "1"
                        elif i == 1:
                            user.name = token
                            flag = "2"
                            Tidentiflag = "2"
                if not reconocido:
                    print(f"Error en el archivo 'users.txt', el token: {token}, en la línea: {line} es inválido. Se descartará el usuario.")
                    print(TTErrors(token, flag))
                    break     
        f.close()

def LoadBooks(path: str) -> None:
    flag = "2"
    with open(path, "r",encoding="utf-8") as f:
        reader = csv.reader(f)
        for line_numer, line in enumerate(reader):
            book: Book = Book()
            for i, token in enumerate(line):
                reconocido = False
                Tidentiflag = str(i + 2)
                for tipo in range(2):
                    if token_Identifier(token, Tidentiflag):
                        reconocido = True
                        if i == 0:
                            books[line[0]] = book
                            flag = "3"
                            Tidentiflag = "3"
                        elif i == 1:
                            book.title = token
                            flag = "4"
                            Tidentiflag = "4"
                if not reconocido:
                    print(f"Error en el archivo 'books.txt', el token: {token}, en la línea: {line} es inválido. Se descartará el libro.") 
                    print(TTErrors(token, flag))
                    break   
        f.close()

def ReadLoans(path: str) -> None:
    flag = "0"
    today = time.localtime(time.time())
    unsorted_loans = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for line_number, line in enumerate(reader, start= 1):
            loan: Loan = Loan()
            valid_line = True
            for i, token in enumerate(line):
                reconocido = False
                Tidentiflag = str(i)
                for tipo in range(6):
                    if token_Identifier(token, Tidentiflag):
                        reconocido = True

                        if i == 0:
                            loan.user_id = int(token)
                            flag = "1"
                            Tidentiflag = "1"
                            if users.get(loan.user_id) == None:
                                print(f"El id de usuario {str(loan.user_id)} no ha sido registrado, se omitirá la línea.")
                                valid_line = False
                                break
                        elif i == 1:
                            loan.user_name = token
                            flag = "2"
                            Tidentiflag = "2"
                        elif i == 2:
                            loan.book_id = token
                            flag = "3"
                            Tidentiflag = "3"
                        elif i == 3:
                            loan.book_title = token
                            flag = "4"
                            Tidentiflag = "4"
                        elif i == 4:
                            loan.loan_date = token
                            if int(loan.loan_date[:3]) > today.tm_year:
                                print("La fecha del préstamo no puede ser mayor a hoy.")
                                valid_line = False
                                break
                            flag = "5"
                            Tidentiflag = "5"
                        elif i == 5:
                            loan.deadline = token
                        break
                    if not valid_line:
                        break
                if not reconocido:
                    print(f"Error, el token: {token}, en la línea: {line} es inválido. Se omitirá la línea.")
                    print(TTErrors(token, flag))
                    valid_line = False
            if not valid_line:
                continue
            if books.get(loan.book_id) != None:
                users[loan.user_id].borrowed = users[loan.user_id].borrowed + 1
                books[loan.book_id].borrowed = books[loan.book_id].borrowed + 1
            else:
                print(f"Libro con id {loan.book_id} no encontrado")
                break
            loan.loan_date_timestamp = time.mktime(time.strptime(loan.loan_date,"%Y-%m-%d"))
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
                if (value == None) and (value == loan.deadline) :
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

def GetOverDueLoan(items : list[Loan]) -> None:
    today = time.localtime(time.time())
    for loan in items:        
        if loan.deadline != None:
            overdue = False
            deadline = list(map(lambda x : int(x), loan.deadline.split("-")))
            if deadline[0] < today.tm_year or (deadline[0] <= today.tm_year and deadline[1] < today.tm_mon) or (deadline[0] <= today.tm_year and deadline[1] <= today.tm_mon and deadline[2] < today.tm_mday):
                overdue = True

            if overdue:
                print(loan)

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
                        if value == loan.loan_date_timestamp:
                            continue
                        else:
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

while True:
    opt = input("Que desea realizar?\n1. Cargar usuarios\n2. Cargar libros\n3. Cargar registro de préstamos desde archivo\n4. Mostrar historial de prestamos\n5. Mostrar listados de usuarios unicos\n6. Mostrar listado de libros prestados\n7. Mostrar estadisticas de prestamos\n8. Mostrar prestamos vencidos\n9. Exportar todos los reportes a HTML\n10. Salir\n")
    opt = opt.strip()
    if not opt.isdigit():
        print("Formato ingresado invalido, intentelo de nuevo")
        continue
    
    opt = int(opt)
    if opt == 1:
        LoadUsers(cwd + "/users.txt")
        
    elif opt == 2:
        LoadBooks(cwd + "/books.txt")
        
    elif opt == 3:
        ReadLoans(cwd + "/file.lfa")
        
    elif opt == 4:
        for loan in loans:
            print(loan)
        
    elif opt == 5:
        print("Usuarios unicos:")
        for user_id in users:
            print(str(user_id) + ", " + users[user_id].name)
        
    elif opt == 6:
        print("Libros Prestados:")
        for book_id in books:
            book: Book = books[book_id]
            if book.borrowed > 0:
                print(book_id + ", " + book.title)
                
        
    elif opt == 7:
        print("Total de libros prestados: " + str(len(loans)))
        print("Libro mas prestado: " + GetTopBook().title)
        print("Usuario mas activo: " + GetTopUser().name)
        
    elif opt == 8:
        GetOverDueLoan(loans)
        
    elif opt == 9:
        print("Exportando reportes...")
        GenerateReports(cwd + "/report.html")
        print("Los reportes se han exportado con exito!")
        
    elif opt == 10:
        break
    else:
        print("La opcion ingresada no existe, intentelo de nuevo")
