from abc import ABC, abstractmethod
from datetime import datetime


class Notifier(ABC):
    @abstractmethod
    def send(self, user, message):
        pass


class ConsoleNotifier(Notifier):
    def send(self, user, message):
        print(f"  [Consola] {user.name}: {message}")


class EmailNotifier(Notifier):
    def send(self, user, message):
        print(f"  [Email -> {user.email}] {message}")
