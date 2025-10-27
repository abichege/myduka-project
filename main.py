from flask import Flask, render_template
from database import fetch_data
app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    prods=fetch_data('products')
    # print(prods)
    return render_template('products.html', product=prods)

@app.route('/sales')
def sales():
    my_sales=fetch_data('sales')
    # print(my_sales)
    return render_template('/sales.html', sale=my_sales)

@app.route('/stock')
def stock():
    my_stock=fetch_data('stock')
    print(my_stock)
    return render_template('/stock.html', mystock=my_stock)




app.run()
