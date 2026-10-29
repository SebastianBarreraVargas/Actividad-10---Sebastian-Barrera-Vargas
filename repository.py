from abc import ABC, abstractmethod


class LoanRepository(ABC):
    @abstractmethod
    def add(self, user, book):
        pass

    @abstractmethod
    def remove(self, user, book):
        pass

    @abstractmethod
    def books_of(self, user):
        pass


class InMemoryLoanRepository(LoanRepository):
    def __init__(self):
        self._loans = []

    def add(self, user, book):
        self._loans.append((user, book))

    def remove(self, user, book):
        self._loans.remove((user, book))

    def books_of(self, user):
        return [b for u, b in self._loans if u is user]
