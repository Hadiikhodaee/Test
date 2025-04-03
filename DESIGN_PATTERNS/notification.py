from abc import ABC, abstractmethod

class Observer(ABC):
    @staticmethod
    @abstractmethod
    def send(message):
        pass

class EmailNotification(Observer):
    @staticmethod
    def send(message):
        print(f"Sending Email message {message}")

class SMSNotification(Observer):
    @staticmethod
    def send(message):
        print(f"Sending SMS message {message}")

class PushNotification(Observer):
    @staticmethod
    def send(message):
        print(f"Sending Push message {message}")