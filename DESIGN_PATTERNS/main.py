from shop import Product, Purchase

if __name__ == "__main__":
    p1 = Product()

    purchase = Purchase([p1])
    purchase.checkout()