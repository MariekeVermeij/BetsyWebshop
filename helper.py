from numpy import outer
from datetime import datetime
from models import User,Product,Tags_per_Product,Seller_per_product,Tag_id,Transaction_history
 
#function to search in name and description for a certain term and return the products with information
def search(term):
    query = Product.select(Product.product_id,Product.product_name,Product.description,Product.price_per_unit,Product.quantity_in_stock).where((Product.product_name.contains(term)) | (Product.description.contains(term)))
    l = [] 
    for product in query:
        l.append((product.product_id,product.product_name,product.description))
    return l


#function to return seller with products
def list_user_products(user_id):
    query = Product.select(Seller_per_product.user_id,Seller_per_product.product,User.user_id,User.user_name,Product.product_id,Product.product_name,Product.description)\
            .join(Seller_per_product, on= ((Seller_per_product.product == Product.product_id) & (Seller_per_product.user_id == user_id)), attr='seller')\
            .join(User,on=Seller_per_product.user_id == User.user_id, attr='user')
    l=[]
    for user in query:
        l.append((user.seller.user_id,user.seller.user.user_name,user.product_id,user.product_name,user.description))
    return l



#function to show withs products have a certain tag. 
def list_products_per_tag(tag_id):
    query = Tags_per_Product.select(Tags_per_Product.tag_id,Tag_id.tag_name,Product.product_id,Product.product_name,Product.description)\
            .join(Tag_id, on= Tag_id.tag_id == Tags_per_Product.tag_id, attr='tags')\
            .switch(Tags_per_Product)\
            .join(Product, on=Tags_per_Product.product_id == Product.product_id, attr='product_id')\
            .where(tag_id==Tags_per_Product.tag_id)
    l=[]
    for product in query: 
        l.append((product.tag_id, product.tags.tag_name, product.product_id.product_id, product.product_id.product_name, product.product_id.description))
    return l


#function to only return the last product id
def return_last_product_id():
    query = Product.select(Product.product_id).order_by(Product.product_id.desc())
    for product in query:
        return product.product_id


#funcion to add new product with information to the products, seller per product and tag per product table.
def add_product_to_catalog(user_id,product_name,product_description,price,quantity,tag1,tag2):
    try: 
        return_last_product_id
        Product.create(product_id=(return_last_product_id()+1),product_name=product_name,description=product_description,price_per_unit=price,quantity_in_stock=quantity)
        Seller_per_product.create(user_id = user_id,product = (return_last_product_id()))
        Tags_per_Product.create(product_id=(return_last_product_id()),tag_id=tag1)
        Tags_per_Product.create(product_id=(return_last_product_id()),tag_id=tag2)
        return 'Product added to catalog'
    except: return 'Error, product NOT added to catalog!'


#function to remove a product from the database
def remove_product(product_id):
    try:
        a =Product.delete().where(Product.product_id == product_id)
        a.execute()
        b=Tags_per_Product.delete().where(Tags_per_Product.product_id == product_id)
        b.execute()
        c=Seller_per_product.delete().where(Seller_per_product.product == product_id)
        c.execute()
        return 'Product removed from catalog'
    except: return 'Error, product NOT removed from database'


#function to change the stock quantity for a certain product
def update_stock(product_id, new_quantity):
    try:
        update = Product.update(quantity_in_stock = new_quantity).where(Product.product_id == product_id)
        update.execute()
        return 'Stock is updated'
    except: return 'Error, stock is NOT updated'


# function to return the quantity of a certain product.
def return_last_product_quantity(product_id):
    query = Product.select(Product.product_id,Product.quantity_in_stock).where(Product.product_id == product_id)
    for product in query:
        return product.quantity_in_stock


#funtion to return the highest transaction id
def return_last_transaction_id():
    query = Transaction_history.select(Transaction_history.transaction_id).order_by(Transaction_history.transaction_id.desc())
    for transaction in query:
        return transaction.transaction_id


#funtion to return user Id for product
def return_user_id(product_id):
    query = Seller_per_product.select(Seller_per_product.user_id,Seller_per_product.product).where(Seller_per_product.product_id == product_id)
    for user in query:
        return(user.user_id)


#function to add information about a new purchase to transaction history and update the quantity in stock
def purchase_product(product_id, buyer_id, quantity):
    query = Seller_per_product.select(Seller_per_product.user_id,User.user_id,User.billing_info)\
        .join(User,on=Seller_per_product.user_id == User.user_id, attr='user')
    new_quantity = (return_last_product_quantity(product_id))-quantity 
    if new_quantity >= 0:
            update_stock(product_id,new_quantity)
            today= datetime.today().strftime('%Y-%m-%d')
            Transaction_history.create(transaction_id=(return_last_transaction_id()+1),customer_id=buyer_id,seller_id= return_user_id(product_id),\
                purchase_date = today, purchase_product= product_id, purchase_quantity=quantity, customer_invoice_sent= 'FALSE', customer_invoice_payed= 'FALSE')
            User.update(billing_info = 'Open Invoices').where(buyer_id == User.user_id).execute()
            print (buyer_id,User.user_id)
            return 'Purchase of product is administrated'
    else: return 'Not enough products in stock for this purchase'

