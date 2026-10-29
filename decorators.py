from notifiers import Notifier
from datetime import datetime


class NotifierDecorator(Notifier):
    def __init__(self, wrapped):
        self._wrapped = wrapped

    def send(self, user, message):
        self._wrapped.send(user, message)


class TimestampNotifier(NotifierDecorator):
    def send(self, user, message):
        ts = datetime.now().strftime("%H:%M:%S")
        super().send(user, f"[{ts}] {message}")


class UrgentNotifier(NotifierDecorator):
    def send(self, user, message):
        super().send(user, f"URGENTE: {message}")
