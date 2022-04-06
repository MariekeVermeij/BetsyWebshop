__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"
from numpy import outer
from datetime import datetime
from models import User,Product,Tags_per_Product,Seller_per_product,Tag_id,Transaction_history
 
#function to search in name and description for a certain term and return the products with information
def search(term):
    query = Product.select(Product.product_id,Product.product_name,Product.description,Product.price_per_unit,Product.quantity_in_stock).where((Product.product_name.contains(term)) | (Product.description.contains(term)))
    for product in query:
        print(product.product_id,product.product_name,product.description,product.price_per_unit,product.quantity_in_stock)
    return""
#print(search('Necklace'))


#function to return seller with products
def list_user_products(user_id):
    query = Product.select(Seller_per_product.user_id,Seller_per_product.product,User.user_id,User.user_name,Product.product_id,Product.product_name,Product.description)\
            .join(Seller_per_product, on= ((Seller_per_product.product == Product.product_id) & (Seller_per_product.user_id == user_id)), attr='seller')\
            .join(User,on=Seller_per_product.user_id == User.user_id, attr='user')
    for user in query:
        print(user.seller.user_id,user.seller.user.user_name,user.product_id,user.product_name,user.description)
    return""
#print(list_user_products(256123))   


#function to show withs products have a certain tag. 
def list_products_per_tag(tag_id):
    query = Tags_per_Product.select(Tags_per_Product.tag_id,Tag_id.tag_name,Product.product_id,Product.product_name,Product.description)\
            .join(Tag_id, on= Tag_id.tag_id == Tags_per_Product.tag_id, attr='tags')\
            .switch(Tags_per_Product)\
            .join(Product, on=Tags_per_Product.product_id == Product.product_id, attr='product_id')\
            .where(tag_id==Tags_per_Product.tag_id)
    for product in query: 
        print(product.tag_id, product.tags.tag_name, product.product_id.product_id, product.product_id.product_name, product.product_id.description)
    return""
#print(list_products_per_tag(50003))
#print(list_products_per_tag(10003))


#function 
def return_last_product_id():
    query = Product.select(Product.product_id).order_by(Product.product_id.desc())
    for product in query:
        return product.product_id
#print(return_last_product_id())


#funcion to add new product with information to the products, seller per product and tag per product table.
def add_product_to_catalog(user_id,product_name,product_description,price,quantity,tag1,tag2):
    a = Product.insert(product_id=(return_last_product_id()+1),product_name=product_name,description=product_description,price_per_unit=price,quantity_in_stock=quantity)
    a.execute()
    b = Seller_per_product.insert(user_id = user_id,product = (return_last_product_id()))
    b.execute()
    c = Tags_per_Product.insert(product_id=(return_last_product_id()),tag_id=tag1)
    c.execute()
    d = Tags_per_Product.insert(product_id=(return_last_product_id()),tag_id=tag2)
    d.execute()
#add_product_to_catalog(256123,'Necklace','Double Heart Necklace',12,3,50003,10003)
#print(search('Necklace'))

#function to remove a product from the database
def remove_product(product_id):
    a =Product.delete().where(Product.product_id == product_id)
    a.execute()
    b=Tags_per_Product.delete().where(Tags_per_Product.product_id == product_id)
    b.execute()
    c=Seller_per_product.delete().where(Seller_per_product.product == product_id)
    c.execute()
#remove_product(20220000036)
#print(search('Necklace'))


#function to change the stock quantity for a certain product
def update_stock(product_id, new_quantity):
    update = Product.update(quantity_in_stock = new_quantity).where(Product.product_id == product_id)
    update.execute()
#update_stock(20220000039,99)


# function to return the quantity of a certain product.
def return_last_product_quantity(product_id):
    query = Product.select(Product.product_id,Product.quantity_in_stock).where(Product.product_id == product_id)
    for product in query:
        return product.quantity_in_stock
#print(return_last_product_quantity(20220000039))


#funtion to return the highest transaction id
def return_last_transaction_id():
    query = Transaction_history.select(Transaction_history.transaction_id).order_by(Transaction_history.transaction_id.desc())
    for transaction in query:
        return transaction.transaction_id
#print(return_last_transaction_id())

#funtion to return the highest product id
def return_user_id(product_id):
    query = Seller_per_product.select(Seller_per_product.user_id,Seller_per_product.product).where(Seller_per_product.product_id == product_id)
    for user in query:
        return(user.user_id)
#print(return_user_id(20220000039))


#function to add information about a new purchase to transaction history and update the quantity in stock
def purchase_product(product_id, buyer_id, quantity):
    new_quantity = (return_last_product_quantity(product_id))-quantity 
    update_stock(product_id,new_quantity)
    today= datetime.today().strftime('%Y-%m-%d')
    a = Transaction_history.insert(transaction_id=(return_last_transaction_id()+1),customer_id=buyer_id,seller_id= return_user_id(product_id),\
        purchase_date = today, purchase_product= product_id, purchase_quantity=quantity, customer_invoice_sent= 'FALSE', customer_invoice_payed= 'FALSE')
    a.execute()
#purchase_product(20220000039,221513,10)
#print(return_last_transaction_id())
#print(search('Necklace'))

