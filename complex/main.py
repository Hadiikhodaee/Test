from samples import create_samples
from advertisment import ApartmentRent, ApartmentSell, HouseRent,HouseSell, StoreRent, StoreSell
class Handler:
    ADVERTISEMENT_TYPES = {
        1 : ApartmentSell,
        2 : ApartmentRent,
        3 : HouseSell,
        4 : HouseRent
    }
    SWITCHES = {
        'r':'get_reports',
        's':'show_all',
        'g' : 'search'
    }
    def get_reports(self):
        for adv in self.ADVERTISEMENT_TYPES.values():
            print(adv, adv.manager.count())
            
    def show_all(self):
        for adv in self.ADVERTISEMENT_TYPES.values():
            for obj in adv.object_list:
                print(obj.show_detail())
                
    def search(self):
        for key in self.ADVERTISEMENT_TYPES:
            print(f'press {key} for {self.ADVERTISEMENT_TYPES[key]}')
        user_input = int(input('Enter your choice: '))
        switch = self.ADVERTISEMENT_TYPES.get(user_input, None)
        
        if switch is None:
            print("iNvalid input")
            self.run()
            
        for item in switch.manager.get(floor = 3, price_per_meter=100):
            item.show_detail()
        self.run()
    
    def run(self):
        for key in self.SWITCHES:
            print(f'press {key} for {self.SWITCHES[key]}')
        user_input = input('Enter your choice: ')
        switch = self.SWITCHES.get(user_input, None)
        
        if switch is None:
            print("iNvalid input")
            self.run()
            
        choice = getattr(self, switch, None)
        choice()
        self.run()
        
            


if __name__ == "__main__":
    create_samples()
    Handler().run()