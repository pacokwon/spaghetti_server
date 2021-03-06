from pymongo import MongoClient
from random import randint

def insert_ratings():
    client = MongoClient('mongodb://localhost')
    db = client['newb']
    db.ratings.drop()

    pipeline = [
        {'$unwind': '$menus'},
        {
            '$project': {
                '_id': 1,
                'name': 1,
                'menu': '$menus'
            }
        }
    ]

    res = list(db.categories.aggregate(pipeline))

    col = db['ratings']
    for obj in res:
        salty = True if randint(0, 1) == 0 else False
        for i in range(10):
            if i == 0:
                col.insert_one({'name': obj['name'],
                                'menu': obj['menu'],
                                'rating': [{
                                    'taste': randint(1, 3) if salty else randint(3, 5),
                                    'portion': randint(1, 3) if salty else randint(3, 5),
                                    'price': randint(1, 3) if salty else randint(3, 5)
                                }]})
            else:
                col.update_one(
                    {
                        'name': obj['name'],
                        'menu': obj['menu']
                    },
                    {
                        '$push': {
                            'rating': {
                                'taste': randint(1, 3) if salty else randint(3, 5),
                                'portion': randint(1, 3) if salty else randint(3, 5),
                                'price': randint(1, 3) if salty else randint(3, 5)
                            }
                        }
                    }
                )

def insert_one_rating(name, menu, rating):
    client = MongoClient('mongodb://localhost')
    db = client['newb']

    pipeline = [
        {'$unwind': '$menus'},
        {
            '$project': {
                '_id': 1,
                'name': 1,
                'menu': '$menus'
            }
        }
    ]
    col = db['ratings']

    col.update_one(
        {
            'name': name,
            'menu': menu
        },
        {
            '$push': {
                'rating': rating
            }
        }
    )

if __name__ == "__main__":
    insert_ratings()
