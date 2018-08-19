from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Book, Base, BookItem

engine = create_engine('sqlite:///bookitem.db')
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


# Adding a list of books in the book1 category
book1 = Book(name="Motivational Books")

session.add(book1)
session.commit()

bookItem1 = BookItem(name="The Alchemist",
                     description="Paulo Coelho's"
                    "masterpiece tells the magical story of Santiago, an"
                    "Andalusian shepherd boy who yearns to travel in search"
                    "of a worldly treasure as extravagant as any ever found."
                    "The story of the treasures Santiago finds along the way "
                    "teaches us, as only a few stories can, about the essential"
                    "wisdom of listening to our hearts, learning to read the omens"
                    "strewn along life's path, and, above all, following our dreams.",
                     price="$14.50",
                     book=book1)

session.add(bookItem1)
session.commit()


bookItem2 = BookItem(name="Winning",
                     description="The core of Winning is devoted to the real stuff of work."
                     "This main part of the book is split into three sections. The first looks"
                     "inside the company, from leadership to picking winners to making change"
                     "happen. The second section looks outside, at the competition, with chapters"
                     "on strategy, mergers, and Six Sigma, to name just three. The next section of"
                     "the book is about managing your career from finding the right job to achieving"
                     "work-life balance. Welch's optimistic, no excuses, get-it-done mind-set is"
                     "riveting. Packed with personal anecdotes and written in Jack's distinctive"
                     "no b.s. voice, Winning offers deep insights, original thinking, and solutions"
                     "to nuts-and-bolts problems that will change the way people think about work.",
                     price="$18.99",
                     book=book1)

session.add(bookItem2)
session.commit()


# List if novels books category
book2 = Book(name="Top Selling Novels Books")

session.add(book2)
session.commit()


bookItem1 = BookItem(name="The Shakespeare Requirement",
                     description="The slings and arrows of outrageous fortune keep hitting"
                     "beleaguered English professor Jason Fitger right between the eyes in"
                     "this hilarious and eagerly awaited sequel to the cult classic of"
                     "anhedonic academe, the Thurber Prize-winning Dear Committee Members."
                     "Once more into the breach...",
                     price="$24.99",
                     book=book2)

session.add(bookItem1)
session.commit()

bookItem2 = BookItem(name="Grind",
                     description=" Six different people from different walks of life all"
                     "come together in unimaginable ways when they each have a surprising"
                     "connection to one woman. She is Kopper Kandy, a nude dancer in a"
                     "Portland strip club, Exxxotica, and she will change each of their"
                     "lives forever. Meanwhile Kopper Kandy is Allison, the single mother,"
                     "the woman, who must find a way to integrate herself before she loses"
                     "who she is forever. As each person is drawn to the club, the"
                     "reverberations through their relationships are felt in very different"
                     "ways. Sex, love, power, money and the ultimate mystery of men and"
                     "women are explored in this provocative novel that will keep the"
                     "reader craving the next twist of fate before it all coalesces in"
                     "one defining moment-a moment that will determine the rest of their lives.",
                     price="$10.59",
                     book=book2)

session.add(bookItem2)
session.commit()

bookItem3 = BookItem(name="The Address",
                     description="Fiona Davis, author of The Dollhouse, returns with a"
                     "compelling novel about the thin lines between love and loss, success"
                     "and ruin, passion and madness, all hidden behind the walls of The"
                     "Dakota New York City most famous residence.",
                     price="15.00",
                     book=book2)

session.add(bookItem3)
session.commit()



# List of Business Books category
book3 = Book(name="Business Guide Books")

session.add(book3)
session.commit()


bookItem1 = BookItem(name="Business Analytics",
                     description=" Business Analytics, Second Edition teaches the fundamental"
                     "concepts of the emerging field of business analytics and provides vital"
                     "tools in understanding how data analysis works in today organizations."
                     "Students will learn to apply basic business analytics principles,"
                     "communicate with analytics professionals, and effectively use and"
                     "interpret analytic models to make better business decisions. Included"
                     "access to commercial grade analytics software gives students real world"
                     "experience and career-focused value.",
                     price="$39.99",
                     book=book3)

session.add(bookItem1)
session.commit()

bookItem2 = BookItem(name="The Outlier Approach: How to Triumph in your Career as a Nonconformist ",
                     description="From building his last startup to a $15M valuation to selling"
                     "beepers in Compton and making nearly $10K/month after immigrating to the"
                     "US with broken English, Kevin Hong has learned the power of selling vision."
                     "Sell vision to win job interviews, raise money, and recruit superstars"
                     "for your cause. ",
                     price="$15.99",
                     book=book3)

session.add(bookItem2)
session.commit()

# List of Thriller Books category
book4 = Book(name="Thriller and Suspense Books")

session.add(book4)
session.commit()


bookItem1 = BookItem(name="I will Never Leave You",
                     description=" Banking heiress Trish and her husband, James, seem to"
                     "have it all, from a lavish lifestyle to a historic mansion in the"
                     "nation capital. The only thing that is missing to make their family"
                     "complete is a baby, so when Trish holds Anne Elise in her arms for"
                     "the first time, it is no surprise that she falls deeply in love."
                     "There is just one problem: Trish is not the mother.",
                     price="$5.99",
                     book=book4)

session.add(bookItem1)
session.commit()

bookItem2 = BookItem(name="Cyber Storms",
                     description="In the chaos, conspiracy theories rage about a foreign"
                     "cyberattack. Was it the North Koreans? The Russians? The Chinese?"
                     "Might it be the first shockwave of a global shift in power? But"
                     "even these questions become unimportant as Mike and his family"
                     "struggle for survival in the wintry tomb of a doomed New York.",
                     price="$5.99",
                     book=book4)

session.add(bookItem2)
session.commit()

# List of Romance Novels category
book5 = Book(name="Romance and Books")

session.add(book5)
session.commit()


bookItem1 = BookItem(name="Single Dad",
                     description=" My life is going to hell in a handbasket."
                     "My bitter rival just stole the technology I spent millions"
                     "to design and passed it off as his. Now I have less than two"
                     "weeks to come up with a miracle, or lose everything I have"
                     "worked all my life for.",
                     price="$3.99",
                     book=book5)

session.add(bookItem1)
session.commit()

bookItem2 = BookItem(name="Accidental Rival: An Office Romance",
                     description="So there we were. Two people as different as"
                     "fire and ice. There's me. An ambitious, committed,"
                     "head down no nonsense kind of girl who does not need"
                     "distractions in the workplace.Then, there is him: a "
                     "self obsessed, arrogant, flirtatious, entitled, class"
                     "A jerk who wastes time hanging around the water cooler"
                     "flirting with my female colleagues. And I see them batting"
                     "their lashes back at him. Ugh! What they see in him is"
                     "beyond me.",
                     price="$10.99",
                     book=book5)

session.add(bookItem2)
session.commit()


print ("added books lists!")