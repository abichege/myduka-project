from flask import Flask, render_template,request,redirect,url_for
from database import fetch_data, insert_products,insert_sales,insert_stock
app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products():
    prods=fetch_data('products')
    # print(prods)
    return render_template('products.html', product=prods)

@app.route('/add_products',methods=['GET','POST'])
def add_products():
    if request.method=='POST':
        # productid=request.form['pid']
        pname=request.form['name']
        bp=request.form['bp']
        sp=request.form['sp']

        new_product=(pname,bp,sp)
        insert_products(new_product)
        return redirect(url_for('products'))
    return redirect(url_for('products'))

@app.route('/sales')
def sales():
    my_sales=fetch_data('sales')
    # print(my_sales)
    product=fetch_data('products')
    return render_template('/sales.html', sale=my_sales,prods=product)

@app.route('/add_sales',methods=['GET','POST'])
def add_sales():
    if request.method=='POST':
        # sid=request.form['sid']
        spid=request.form['spid']
        quantity=request.form['quantity']
        

        new_sales=(spid,quantity)
        insert_sales(new_sales)
        return redirect(url_for('sales'))
    return redirect(url_for('sales'))

@app.route('/stock')
def stock():
    my_stock=fetch_data('stock')
    # print(my_stock)
    my_prod=fetch_data('products')
    return render_template('/stock.html', mystock=my_stock, my_prods=my_prod)

@app.route('/add_stock',methods=['GET','POST'])
def add_stock():
    if request.method=='POST':
        # stid=request.form['stid']
        pid=request.form['stpid']
        stockquantity=request.form['stockquantity']

        new_stock=(pid,stockquantity)
        insert_stock(new_stock)
        return redirect(url_for('stock'))
    return redirect(url_for('stock'))





app.run(debug=True)
