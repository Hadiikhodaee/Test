from user import User
from estate import Apartment, House, Store
from region import Region
from advertisment import ApartmentRent, ApartmentSell, HouseRent, HouseSell, StoreRent, StoreSell
from random import choice

first_name = ['first_name1', 'first_name2', 'first_name3']
last_name = ['last_name1', 'last_name2', 'last_name3']
mobiles = ["0999999", '088888', "0777777"]



def create_samples():
    for mobile in mobiles:
        User(choice(first_name), choice(last_name), mobile)
        
    reg1 = Region(name = "regoin1")
    reg2 = Region(name = "regoin2")
    
    apartment1 = Apartment(has_elevator=True, 
                           has_parking=True, 
                           floor=2, 
                           user=User.object_list[0],
                           build_year = 1403,
                           area = 100,
                           region = reg1,
                           rooms_count = 2,
                           address = "tehran ....."
                        )
    
    apartment_sell1 = ApartmentSell(
                            has_elevator= True, 
                            has_parking=True, 
                            floor = 3, 
                            user=User.object_list[0],
                            built_year = 1402,
                            region = reg1,
                            rooms_count = 2,
                            address = "tehran .....",
                            price_per_meter = 100,
                            discountable = True,
                            convertable = True,
                            build_year = 1403,
                            area = 100
                        )
    
    store1 = Store(user=User.object_list[2],
                       area=300,
                       rooms_count=5,
                       build_year=1400,
                       region=reg1,
                       address="tehran..."
                       )
    apartment_sell1 = ApartmentSell(
                        has_elevator=True,
                        has_parking=True,
                        floor=3,
                        user=User.object_list[0],
                        build_year=1402,
                        region=reg1,
                        rooms_count=2,
                        address="Tehran...",
                        price_per_meter=100,
                        discountable=False,
                        convertable=True,
                        area=300,
    )
    apartment_sell2 = ApartmentSell(
                        has_elevator=True,
                        has_parking=True,
                        floor=3,
                        user=User.object_list[0],
                        build_year=1402,
                        region=reg1,
                        rooms_count=2,
                        address="Tehran...",
                        price_per_meter=100,
                        discountable=True,
                        convertable=True,
                        area=300,
    )
    apartment_rent1 = ApartmentRent(
                        has_elevator=True,
                        has_parking=True,
                        floor=3,
                        user=User.object_list[0],
                        build_year=1402,
                        region=reg1,
                        rooms_count=2,
                        address="Tehran...",
                        initial_price=250,
                        monthly_price=50,
                        convertable=True,
                        area=300,
    )
    house_sell1 = HouseSell(
                        has_yard=True,
                        floors_count=5,
                        user=User.object_list[0],
                        build_year=1402,
                        region=reg1,
                        rooms_count=2,
                        address="Tehran...",
                        price_per_meter=100,
                        discountable=True,
                        convertable=True,
                        area=300,
            )
    house_rent1 = HouseRent(
                        has_yard=True,
                        floors_count=5,
                        user=User.object_list[0],
                        build_year=1402,
                        region=reg1,
                        rooms_count=2,
                        address="Tehran...",
                        initial_price=250,
                        monthly_price=50,
                        convertable=True,
                        discountable=False,
                        area=300,
            )
        
     