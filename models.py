import peewee
from datetime import date

db = peewee.SqliteDatabase("Betsy.db")



#class for product information
class Product(peewee.Model):
    product_name = peewee.CharField()
    product_id = peewee.IntegerField(unique=True)
    description = peewee.CharField()
    price_per_unit = peewee.DecimalField(decimal_places = 10)
    quantity_in_stock = peewee.IntegerField()

    class Meta:
        database = db

#class to link tags with products
class Tags_per_Product(peewee.Model):
    product_id = peewee.ForeignKeyField(Product, backref='tags_product')
    tag_id =  peewee.IntegerField()
    
    class Meta:
        database = db
#class with description of tag_ids

class Tag_id (peewee.Model):
    tag_name = peewee.CharField()
    tag_id = peewee.ForeignKeyField(Tags_per_Product, backref='tag_name')

    class Meta:
        database = db

#class with products per seller

class Seller_per_product (peewee.Model):
    user_id = peewee.IntegerField(unique=True)
    product = peewee.ForeignKeyField(Product, backref='seller_product')
  
    class Meta:
        database = db
        indexes = ((('user_id','product'),True),)

#class with user information

class User(peewee.Model):
    user_id = peewee.ForeignKeyField(Seller_per_product, backref='user') 
    user_name = peewee.CharField()
    address_line1 = peewee.CharField()
    address_line2 = peewee.CharField()
    postal_code = peewee.CharField()
    city = peewee.CharField()
 
    class Meta:
        database = db

#class with transaction information

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