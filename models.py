import peewee
from datetime import date

db = peewee.SqliteDatabase("Betsy.db")


class BaseModel(peewee.Model):
    class Meta:
        database = db

#class for product information
class Product(BaseModel):
    product_name = peewee.CharField()
    product_id = peewee.IntegerField(unique=True)
    description = peewee.CharField()
    price_per_unit = peewee.DecimalField(decimal_places = 2,auto_round=True)
    quantity_in_stock = peewee.IntegerField()



#class to link tags with products
class Tags_per_Product(BaseModel):
    product_id = peewee.ForeignKeyField(Product, backref='tags_product')
    tag_id =  peewee.IntegerField()
    

#class with description of tag_ids

class Tag_id (BaseModel):
    tag_name = peewee.CharField(unique=True)
    tag_id = peewee.ForeignKeyField(Tags_per_Product, backref='tag_name',unique=True)


#class with products per seller 

class Seller_per_product (BaseModel):
    user_id = peewee.IntegerField()
    product = peewee.ForeignKeyField(Product, backref='seller_product',unique=True)
  
    class Meta:
        database = db
        indexes = ((('user_id','product'),True),)

#class with user information

class User(BaseModel):
    user_id = peewee.ForeignKeyField(Seller_per_product, backref='user') 
    user_name = peewee.CharField()
    address_line1 = peewee.CharField()
    address_line2 = peewee.CharField()
    postal_code = peewee.CharField()
    city = peewee.CharField()
    billing_info = peewee.CharField()

#class with transaction information

class Transaction_history(BaseModel):
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
