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

user1 = User(username="ajaffal", password="Jansport9-")

session.add(user1)
session.commit()

user2 = User(username="nano", password="password")

session.add(user2)
session.commit()

# Catalog for Adidas shoes
category1 = Category(name="Adidas")

session.add(category1)
session.commit()

item2 = Item(name="Yeezy Boost", description="Without doubt the most celebrated sneaker of the year (thus far), the adidas Yeezy Boost acts as a shinning achievement for adidas. Often times a hyped album, movie or shoe disappoints when it finally makes its was to consumers. Not the Yeezy Boost. Aesthetically, the progressive shoe is a hit",
                     category=category1)

session.add(item2)
session.commit()


item1 = Item(name="Ultra Boost", description="Deemed the best running shoe ever, the adidas Ultra Boost may also be one of the best looking running shoes, too. Highlighting many of the brand's latest technical advancements, this sleek and sartorially pleasing running shoe is as multifaceted as it is dominate on the track, trail or treadmill. And with an all-white pair being all the buzz right now, expect the Three Stripes to feed the beast with more new colorways of the Ultra Boost.",
                     category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Tubular Runner", description="Drawing design inspiration from adidas affiliate label, Y-3, the Tubular Runner may be the best generally accessible new adidas silhouette of 2015. Uniquely crafted for performance and comfort while equally alluring in terms of style, a pair of two of the Tubular Runner is a must this year. And with a moderate price of $110, this purchase is pretty easy to stomach.",
                     category=category1)

session.add(item2)
session.commit()

item3 = Item(name="Superstar Supercolor Pack", description="Pharrell Williams is a colorful character that sees sounds like you and I see things. Thus, when he lends his thoughts to sneaker design, you can expect the outcome to be as vibrant as his personality and accenting wardrobe. That's exactly what the adidas Supercolor Pack represents - a vivid, youthful imagination with no limitations. And with 50 pairs in circulation, no ones tonal needs should go unmet.",
                     category=category1)

session.add(item3)
session.commit()

item4 = Item(name="Stan Smith", description="Although the Stan Smith was much more of a fixture during its initial retro run last year, its fuel still burns in 2015. We choose not to mark a particular model here, we simply hold the Stan up as a staple item this season. Few shoes are better for the warm weather months than this one, and that's as true this year as it was last. There is a reason why the Stan Smith is adidas' best selling shoe of all-time - timelessness never fails.",
                     category=category1)

session.add(item4)
session.commit()


# Catalog for Puma shoes
category2 = Category(name="Puma")

session.add(category2)
session.commit()


item1 = Item(name="BioWeb Elite", description="The PUMA BioWeb Elite men's running shoes are ideal for cross training regimens. The shoes offer plenty of support for weightlifting and other gym activities, but also have the cushioning and durability to work as a running shoe. The webbed design on the exterior is a stylish plus.",
                      category=category2)

session.add(item1)
session.commit()

item2 = Item(
    name="Mobium Elite Speed", description="For a dedicated running shoe, the PUMA Mobium Elite Speed men's running shoes are a great option. The name comes from a band that runs in a figure eight shape around the outsole of the shoe and provides unique resistance that can add more speed to the user's run.",
    category=category2)

session.add(item2)
session.commit()

item3 = Item(name="Suede Classic", description="Not every pair of sneakers is for wearing on the court or on the track. The PUMA Suede Classic shoes, while at the height of athletic technology when they first appeared, are now simply stylish street shoes. The PUMA logo is prominent as is the unmistakable swoop. The shoes are available in a wide range of colors in sizes for both men and women.",
                     category=category2)

session.add(item3)
session.commit()

item4 = Item(name="Titantour", description="The PUMA TITANTOUR golf shoes use cutting-edge technology to create shoes that stay comfortable for an entire round on the links. While Shapelock memory foam creates a cushion that molds to any individual foot, cooling technology keeps feet cool and dry for hours.",
                     category=category2)

session.add(item4)
session.commit()

item5 = Item(name="Soleil FS", description="Women's feet often call for shoes that are a bit different than men's. The PUMA Soleil FS women's sneakers are dance-friendly athletic shoes that are ideal for vigorous classes, including Zumba, and specifically sized for women's feet. The sole features a pivot point that makes dance turns and spins easier as well.",
                     category=category2)

session.add(item5)
session.commit()

item6 = Item(name="Match 74", description="Drawing comparisons to classic sneakers, like the Nike Wimbledon, the PUMA Match 74 is a sleek leather shoe with retro appeal. With colors as varied as black with a white sole and a deep, rich burgundy, there is a pair of PUMA Match 74 sneakers to match virtually any personal style.",
                     category=category2)

session.add(item6)
session.commit()


# Catalog for Nike shoes
category1 = Category(name="Nike")

session.add(category1)
session.commit()


item1 = Item(name="Kobe XI Elite Premium ASG iD", description="The Kobe XI Elite Premium ASG iD Basketball Shoe celebrates one of basketball's most exciting weekends and brightest stars. New, exclusive, customizable graphics let you represent your favorite player while setting yourself apart.",
                     category=category1)

session.add(item1)
session.commit()

item2 = Item(name="Air Icarus", description="The Nike Air Icarus Men's Shoe recalls a classic running shoe with an updated nylon upper and synthetic suede for durable, lightweight comfort. Nike Air cushioning offers soft, lightweight impact protection.",
                     category=category1)

session.add(item2)
session.commit()

item3 = Item(name="SB50 Nike Ultra XT", description="The SB50 Nike Ultra XT Men's Shoe offers a premium look off the field with a sleek leather upper and engraved hardware that pays homage to the big game. A midfoot strap locks your foot in place, and a foam midsole delivers a plush ride. ",
                     category=category1)

session.add(item3)
session.commit()

item4 = Item(name="Roshe Cortez", description="The Nike Roshe Cortez Women's Shoe combines the cushioning of the Nike Roshe with the iconic lines of the original Nike Cortez running shoe for a new take on two favorites. A supple suede upper delivers durability while a flexible midsole/outsole promotes natural motion.",
                     category=category1)

session.add(item4)
session.commit()

item2 = Item(name="Juvenate SM", description="The Nike Juvenate SM Women's Shoe delivers minimalist design cues from the classic Roshe in a stretchy, lightweight package. The collapsible upper makes for easy packing when you're on the go.",
                     category=category1)

session.add(item2)
session.commit()



print "added menu items!"
