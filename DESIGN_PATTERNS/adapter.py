from abstractfactory import Rugs

class PriceAdapter:
    def __init__(self, rate):
        self.rate = rate

    def exchange(self, product):
        return self.rate * product._price
    

if __name__ == "__main__":
    r1 = Rugs("persian rugs, 4000")

    adapter = PriceAdapter(20000)
    for rug in [r1]:
        print(f"{rug._name}: {adapter.exchange(rug)}")