from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from setup_file import *

engine = create_engine('sqlite:///bank_db.db')
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

# Existing Bank_Name delete
session.query(Bank_Name).delete()
# Existing Customer_Details delete
session.query(Customer_Details).delete()
# Existing Customer_Details delete.
session.query(User).delete()

# user data
User1 = User(name="Mahesh", email="sriramanenimahesh@gmail.com",)
session.add(User1)
session.commit()
print ("User added successfully")
# sample data
Bank_1 = Bank_Name(name="SBI", user_id=1)
session.add(Bank_1)
session.commit()

Bank_2 = Bank_Name(name="Andhrabank", user_id=1)
session.add(Bank_2)
session.commit()

Bank_3 = Bank_Name(name="HDFC", user_id=1)
session.add(Bank_3)
session.commit()

Bank_4 = Bank_Name(name="ICICI", user_id=1)
session.add(Bank_4)
session.commit()

Bank_5 = Bank_Name(name="AXIS", user_id=1)
session.add(Bank_5)
session.commit()
# Using different users for details
Customer_1 = Customer_Details(cus_name="Mahesh", acc_number="49235792759",
                              cus_phone_number="8458394578",
                              acc_type="savings",
                              cus_address=("Andhrapradesh"),
                              bank_name_id=1,
                              user_id=1)
session.add(Customer_1)
session.commit()

Customer_2 = Customer_Details(cus_name="Dinesh", acc_number="56235792759",
                              cus_phone_number="7538394578",
                              acc_type="current",
                              cus_address=("Andhrapradesh"),
                              bank_name_id=2,
                              user_id=1)
session.add(Customer_2)
session.commit()

Customer_3 = Customer_Details(cus_name="Venkatesh",
                              acc_number="28374827459",
                              cus_phone_number="9182137045",
                              acc_type="savings",
                              cus_address=("Mumbai"),
                              bank_name_id=3,
                              user_id=1)
session.add(Customer_3)
session.commit()

Customer_4 = Customer_Details(cus_name="Pavan",
                              acc_number="59724957847",
                              cus_phone_number="7297828329",
                              acc_type="savings",
                              cus_address=("karnataka"),
                              bank_name_id=4,
                              user_id=1)
session.add(Customer_4)
session.commit()

Customer_5 = Customer_Details(cus_name="prasanth",
                              acc_number="76575792759",
                              cus_phone_number="9182460125",
                              acc_type="savings",
                              cus_address=("Tamilnadu"),
                              bank_name_id=5, user_id=1)
session.add(Customer_5)
session.commit()
print("Bankdata has been inserted sucessfully ")
