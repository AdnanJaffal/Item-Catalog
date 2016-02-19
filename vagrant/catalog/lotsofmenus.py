from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

user1 = User(username="ajaffal")

session.add(user1)
session.commit()

user2 = User(username="nano")

session.add(user2)
session.commit()

# Catalog for 
category1 = Category(name="Urban Burger")

session.add(category1)
session.commit()

item2 = Item(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     category=category1)

session.add(item2)
session.commit()


item1 = Item(name="French Fries", description="with garlic and parmesan",
                     category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Chicken Burger", description="Juicy grilled chicken patty with tomato mayo and lettuce",
                     category=category1)

session.add(item2)
session.commit()

item3 = Item(name="Chocolate Cake", description="fresh baked and served with ice cream",
                     category=category1)

session.add(item3)
session.commit()

item4 = Item(name="Sirloin Burger", description="Made with grade A beef",
                     category=category1)

session.add(item4)
session.commit()

item5 = Item(name="Root Beer", description="16oz of refreshing goodness",
                     category=category1)

session.add(item5)
session.commit()

item6 = Item(name="Iced Tea", description="with Lemon",
                     category=category1)

session.add(item6)
session.commit()

item7 = Item(name="Grilled Cheese Sandwich", description="On texas toast with American Cheese",
                     category=category1)

session.add(item7)
session.commit()

item8 = Item(name="Veggie Burger", description="Made with freshest of ingredients and home grown spices",
                     category=category1)

session.add(item8)
session.commit()


# Menu for Super Stir Fry
category2 = Category(name="Super Stir Fry")

session.add(category2)
session.commit()


item1 = Item(name="Chicken Stir Fry", description="With your choice of noodles vegetables and sauces",
                     category=category2)

session.add(item1)
session.commit()

item2 = Item(
    name="Peking Duck", description=" A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook", category=category2)

session.add(item2)
session.commit()

item3 = Item(name="Spicy Tuna Roll", description="Seared rare ahi, avocado, edamame, cucumber with wasabi soy sauce ",
                     category=category2)

session.add(item3)
session.commit()

item4 = Item(name="Nepali Momo ", description="Steamed dumplings made with vegetables, spices and meat. ",
                     category=category2)

session.add(item4)
session.commit()

item5 = Item(name="Beef Noodle Soup", description="A Chinese noodle soup made of stewed or red braised beef, beef broth, vegetables and Chinese noodles.",
                     category=category2)

session.add(item5)
session.commit()

item6 = Item(name="Ramen", description="a Japanese noodle soup dish. It consists of Chinese-style wheat noodles served in a meat- or (occasionally) fish-based broth, often flavored with soy sauce or miso, and uses toppings such as sliced pork, dried seaweed, kamaboko, and green onions.",
                     category=category2)

session.add(item6)
session.commit()


# Menu for Panda Garden
category1 = Category(name="Panda Garden")

session.add(category1)
session.commit()


item1 = Item(name="Pho", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.",
                     category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Chinese Dumplings", description="a common Chinese dumpling which generally consists of minced meat and finely chopped vegetables wrapped into a piece of dough skin. The skin can be either thin and elastic or thicker.",
                     category=category1)

session.add(item2)
session.commit()

item3 = Item(name="Gyoza", description="The most prominent differences between Japanese-style gyoza and Chinese-style jiaozi are the rich garlic flavor, which is less noticeable in the Chinese version, the light seasoning of Japanese gyoza with salt and soy sauce, and the fact that gyoza wrappers are much thinner",
                     category=category1)

session.add(item3)
session.commit()

item4 = Item(name="Stinky Tofu", description="Taiwanese dish, deep fried fermented tofu served with pickled cabbage.",
                     category=category1)

session.add(item4)
session.commit()

item2 = Item(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     category=category1)

session.add(item2)
session.commit()



print "added menu items!"
