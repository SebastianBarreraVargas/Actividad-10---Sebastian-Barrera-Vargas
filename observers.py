from abc import ABC, abstractmethod


class BookReturnObserver(ABC):
    @abstractmethod
    def on_book_returned(self, book):
        pass


class WaitList(BookReturnObserver):
    def __init__(self, notifier):
        self._notifier = notifier
        self._waiting = {}

    def add(self, user, book):
        if book.isbn not in self._waiting:
            self._waiting[book.isbn] = []
        if user not in self._waiting[book.isbn]:
            self._waiting[book.isbn].append(user)
            self._notifier.send(user, f"Agregado a lista de espera: '{book.title}'.")

    def on_book_returned(self, book):
        waiting = self._waiting.get(book.isbn, [])
        for user in waiting:
            self._notifier.send(user, f"'{book.title}' ya esta disponible.")
        self._waiting[book.isbn] = []
