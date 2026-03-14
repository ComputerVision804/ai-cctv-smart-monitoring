stats = {
    "people":0,
    "loitering":0,
    "fight":0
}

def update_people(count):
    stats["people"] = count

def add_loiter():
    stats["loitering"] += 1

def add_fight():
    stats["fight"] += 1