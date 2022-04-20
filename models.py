__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import helper

def main():
    print(helper.search('Necklace'))
    print(helper.list_user_products(256123))   
    print(helper.list_products_per_tag(50003))
    print(helper.add_product_to_catalog(256123,'Necklace','Double Heart Necklace',12,3,50003,10003))
    print(helper.remove_product(20220000036))
    print(helper.update_stock(20220000040,23))
    print(helper.purchase_product(20220000039,216516,10))



if __name__ == '__main__':
    main()
