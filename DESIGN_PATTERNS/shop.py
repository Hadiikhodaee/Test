from notification import EmailNotification, SMSNotification, PushNotification
from decorators import notify_observers

class Product:
    pass


class Payment:
    observers = [PushNotification, SMSNotification]
    @notify_observers(message="Purchase Paid")
    def checkout(self):
        pass


class Purchase:
    observers = [EmailNotification, SMSNotification, PushNotification]

    def __init__(self, product_list):
        self.product = product_list
        self.payment = Payment()

    def checkout(self):
        self.payment.checkout()
    @notify_observers(message="purchase canceld")
    def cancel(self):
        pass