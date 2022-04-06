#V A user has a name, address data, and billing information.
#V Each user must be able to own a number of products.
#V The products must have a name, a description, a price per unit, and a quantity describing the amount in stock.
#V The price should be stored in a safe way; rounding errors should be impossible.
#V In order to facilitate search and categorization, a product must have a number of descriptive tags.
#? The tags should not be duplicated. geen overlap?
#V We want to be able to track the purchases made on the marketplace, therefore a transaction model must exist
#V You can assume that only users can purchase goods
#V The transaction model must link a buyer with a purchased product and a quantity of purchased items
#As a bonus requirement, you must consider the various constraints for all fields and incorporate these constraints in the data model.

import peewee
from datetime import date

db = peewee.SqliteDatabase("Betsy.db")




class Product(peewee.Model):
    product_name = peewee.CharField()
    product_id = peewee.IntegerField(unique=True)
    description = peewee.CharField()
    price_per_unit = peewee.DecimalField(decimal_places = 10) #rounding errors should be imposible
    quantity_in_stock = peewee.IntegerField()

    class Meta:
        database = db

class Tags_per_Product(peewee.Model):
    product_id = peewee.ForeignKeyField(Product, backref='tags_product')
    tag_id =  peewee.IntegerField()
    
    class Meta:
        database = db

class Tag_id (peewee.Model):
    tag_name = peewee.CharField()
    tag_id = peewee.ForeignKeyField(Tags_per_Product, backref='tag_name')

    class Meta:
        database = db

class Seller_per_product (peewee.Model):
    user_id = peewee.IntegerField(unique=True)
    product = peewee.ForeignKeyField(Product, backref='seller_product')
  
    class Meta:
        database = db
        indexes = ((('user_id','product'),True),)

class User(peewee.Model):
    user_id = peewee.ForeignKeyField(Seller_per_product, backref='user') 
    user_name = peewee.CharField()
    address_line1 = peewee.CharField()
    address_line2 = peewee.CharField()
    postal_code = peewee.CharField()
    city = peewee.CharField()
 
    class Meta:
        database = db


class Transaction_history(peewee.Model):
    transaction_id = peewee.IntegerField(unique=True)
    customer_id = peewee.ForeignKeyField(User, backref='customer_transactions')
    seller_id = peewee.ForeignKeyField(User, backref='seller_transactions')
    purchase_date = peewee.DateTimeField()
    purchase_product = peewee.ForeignKeyField(Product, backref='transactions')
    purchase_quantity = peewee.IntegerField() 
    customer_invoice_sent = peewee.BooleanField()
    customer_invoice_payed = peewee.BooleanField()
 
    class Meta:
        database = db
        indexes = ((('transaction_id','customer_id','seller_id'),True),)

db.connect()

db.create_tables([Tag_id,Product,Tags_per_Product,User,Seller_per_product,Transaction_history])


db.close