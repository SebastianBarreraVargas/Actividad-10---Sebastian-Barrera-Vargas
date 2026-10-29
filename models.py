from abc import ABC, abstractmethod


class Book:
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.available = True

    def __str__(self):
        status = "disponible" if self.available else "prestado"
        return f"{self.title} ({status})"


class User(ABC):
    def __init__(self, name, email, user_type):
        self.name = name
        self.email = email
        self.user_type = user_type

    @abstractmethod
    def max_loans(self):
        pass

    @abstractmethod
    def loan_days(self):
        pass

    def __str__(self):
        return f"{self.name} ({self.user_type})"


class Student(User):
    def __init__(self, name, email):
        super().__init__(name, email, "estudiante")

    def max_loans(self):
        return 2

    def loan_days(self):
        return 7


class Teacher(User):
    def __init__(self, name, email):
        super().__init__(name, email, "docente")

    def max_loans(self):
        return 5

    def loan_days(self):
        return 14
