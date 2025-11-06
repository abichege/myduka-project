import psycopg2
# connect to postgres database
connect = psycopg2.connect(
    host='localhost',
    user='postgres',
    port=5432,
    dbname='myduka_db',
    password='blossomabigael'
)
# declare cursor to perform database operations
curr = connect.cursor()
# fetch products
# curr.execute('select * from products;')
# product = curr.fetchall()
# print(f'my products:{product}')
# fetch sales
# curr.execute('select * from sales;')
# sales = curr.fetchall()
# print(f'my sales:{sales}')
# fetch stock
# curr.execute('select * from stock;')
# stock = curr.fetchall()
# print(f'my stock:{stock}')
# fetch all products


# def fetch_products():
#     curr.execute('SELECT * FROM products;')
#     prods = curr.fetchall()
#     return prods


# products = fetch_products()
# print(products)

# fetch sale
# def fetch_sales():
#     curr.execute('select * from sales')
#     sale=curr.fetchall()
#     return sale
# my_sales=fetch_sales()
# print(my_sales)
# fetch stock
# def fetch_stock():
#     curr.execute('select * from stock')
#     stockk=curr.fetchall()
#     return stockk
# my_stock=fetch_stock()
# print(my_stock)

# fetch data
def fetch_data(table_name):
    curr.execute(f'select * from {table_name}')
    data=curr.fetchall()
    return data
# products=fetch_data('products')
# print(products)
# sales=fetch_data('sales')
# print(sales)
# stock=fetch_data('stock')
# print(stock)
# insert
# product
def insert_products(values):
    query='insert into products(name,buying_price,selling_price)values(%s,%s,%s);'
    curr.execute(query,values)
    connect.commit()

# new_product=('salt',10,25)
# # insert_products(new_product)
# product=fetch_data('products')
# print(product)

# sales
def insert_sales(values):
    query='insert into sales(product_id,quantity,created_at)values(%s,%s,now());'
    curr.execute(query,values)
    connect.commit()

# new_sale=(4,25)
# insert_sales(new_sale)
# my_sale=fetch_data('sales')
# print(my_sale)

# stock
def insert_stock(values):
    query='insert into stock(product_id,stock_quantity)values(%s,%s);'
    curr.execute(query,values)
    connect.commit()

# new_stock=(4,30)
# insert_stock(new_sale)
# my_stock=fetch_data('stock')
# print(my_stock)
# profit per product
def get_profit():
    query='select p.name,p.product_id,sum((p.selling_price-p.buying_price)*s.quantity) as profit from products as p inner join sales as s on p.product_id=s.product_id group by p.name,p.product_id;'
    curr.execute(query)
    profit=curr.fetchall()
    return profit
# my_profit=get_profit()
# print(my_profit)
# sales per product
def get_sales():
    query='select p.name,p.product_id,sum(p.selling_price*s.quantity) as sales from products as p join sales as s on p.product_id=s.product_id group by p.name,p.product_id;'
    curr.execute(query)
    getsales=curr.fetchall()
    return getsales
# my_sales=get_sales()
# print(my_sales)
# profit per day
def profit_per_day():
    query='select date(s.created_at), sum((p.selling_price-p.buying_price)*s.quantity) as profit from products as p join sales as s on p.product_id=s.product_id group by date(s.created_at);'
    curr.execute(query)
    getprofit=curr.fetchall()
    return getprofit
# sales per day
def sales_per_day():
    query='select date(s.created_at), sum((p.selling_price)*s.quantity) as sales from products as p join sales as s on p.product_id=s.product_id group by date(s.created_at) order by date(s.created_at);'
    curr.execute(query)
    getsales=curr.fetchall()
    return getsales