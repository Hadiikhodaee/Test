class User:
    pass

class Address:
    def __init__(self, country):
        self.country = country

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Purchase:
    def __init__(self, user, address):
        self.user = user
        self.address = address
        self.product_list = []

    def add_products(self, product_list):
        if not isinstance(product_list, list):
            product_list = [product_list]
        self.product_list.extend(product_list)

    def total_price(self):
        s = 0
        for product in self.product_list:
            s += product.price