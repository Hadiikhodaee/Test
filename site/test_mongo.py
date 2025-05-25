import pymongo

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = my_client["test_database"]
mycol = db["customers"]
# print(my_client.list_database_names())
# mycol.insert_one({"name": "John", "address": "Highway 37"})
# print(my_client.list_database_names())

# records = [
#      { "name": "Amy", "address": "Apple st 652"},
#   { "name": "Hannah", "address": "Mountain 21"},
#   { "name": "Michael", "address": "Valley 345"},
#   { "name": "Sandy", "address": "Ocean blvd 2"},
#   { "name": "Betty", "address": "Green Grass 1"},
#   { "name": "Richard", "address": "Sky st 331"},
#   { "name": "Susan", "address": "One way 98"},
#   { "name": "Vicky", "address": "Yellow Garden 2"},
#   { "name": "Ben", "address": "Park Lane 38"},
#   { "name": "William", "address": "Central st 954"},
#   { "name": "Chuck", "address": "Main Road 989"},
#   { "name": "Viola", "address": "Sideway 1633"},
#   { "name": "sadeghi", "address": "tehran", "phone":989390096929},
# ]

# mycol.insert_many(records)

# print(mycol.find_one({'name':'sadeghi', 'phone':989390096929}).get('address'))
# print(mycol.find_one({'name': 'sadeghi'})["phone"])

# all_customers = mycol.find({'name': 'sadeghi'})
# for customer in all_customers:
#     print(customer["name"])
#     print(customer["address"])
#     if "phone" in customer:
#         print(customer["phone"])
#     else:
#         print("No phone number available")
#     print(customer)

customers = mycol.find({
    # 'address': {'$gt':'S'},
    'address': {'$regex':'^S'},
})

for customer in customers:
    print(customer["name"])
#TODO work with regex