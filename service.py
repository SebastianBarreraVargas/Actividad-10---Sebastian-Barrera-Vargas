class LibraryService:
    def __init__(self, loans, notifier):
        self._loans = loans
        self._notifier = notifier
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def borrow(self, user, book):
        if not book.available:
            self._notifier.send(user, f"'{book.title}' no esta disponible.")
            return False
        if len(self._loans.books_of(user)) >= user.max_loans():
            self._notifier.send(user, f"Limite de {user.max_loans()} prestamos alcanzado.")
            return False
        book.available = False
        self._loans.add(user, book)
        self._notifier.send(user, f"Prestado: '{book.title}' (max {user.loan_days()} dias).")
        return True

    def give_back(self, user, book):
        if book not in self._loans.books_of(user):
            self._notifier.send(user, f"No tiene prestado '{book.title}'.")
            return False
        book.available = True
        self._loans.remove(user, book)
        self._notifier.send(user, f"Devuelto: '{book.title}'.")
        for obs in self._observers:
            obs.on_book_returned(book)
        return True
