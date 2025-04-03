from abc import abstractmethod, ABC

class EstateAbstract(ABC):
    def __init__(self, user, area, rooms_count, build_year, region, address, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.area = area
        self.rooms_count = rooms_count
        self.build_year = build_year
        self.region = region
        self.address = address
        
    @abstractmethod
    def show_description(self):
        pass
    
class Apartment(EstateAbstract):
    def __init__(self, has_elevator, has_parking, floor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_elevator = has_elevator
        self.has_parking = has_parking
        self.floor = floor
    def show_description(self):
        print(f"Apartment  area : {self.area}")
        
    
    
class House(EstateAbstract):
    def __init__(self, has_yard, floors_count, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_yard = has_yard
        self.floors_count = floors_count
    def show_description(self):
        print(f"House  ")
        
    
class Store(EstateAbstract):
    def show_description(self):
        print(f"House  ")
    