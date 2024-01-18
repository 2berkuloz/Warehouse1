from PyQt6.QtCore import QDateTime

class LogEntry:
    def __init__(self, action, details):
        self.action = action
        self.details = details
        self.timestamp = QDateTime.currentDateTime()

    def __str__(self):
        return f"{self.timestamp.toString()} - {self.action}: {self.details}"
