from levels_none_use.level0 import world_data
import pickle

woring = input("did you chooice number of level? => ").lower()

if not woring.startswith("n"):
    with open("levels/level0_data.py", "wb") as f:
        pickle.dump(world_data, f)

    with open("levels/level0_data.py", "rb") as f:
        d = pickle.load(f)

def make_chart(row, col):
    main_list = []
    tile_list = []

    for i in range(row):
        i = 0
        tile_list.append(i)
        for j in range(col):
            j = 0
            tile_list.append(j)

        main_list.append(tile_list)

        tile_list = []

    print('[')
    for i in range(len(main_list)):
        print(f"    {main_list[i]}", end="\n")
    print(']')