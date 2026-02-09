from flask import Flask, render_template,request,redirect,url_for,flash,session
from database import fetch_data, insert_products,insert_sales,insert_stock,get_profit,get_sales,profit_per_day,sales_per_day,insert_users,check_email,total_sales,total_profit,update_product,update_sale,update_stock,delete_product
from flask_bcrypt import Bcrypt
app=Flask(__name__)
bcrypt=Bcrypt(app)
app.secret_key='abcdefghijklmnop'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/products')
def products():
    if 'email' in session:
        prods=fetch_data('products')
    else:
        flash('login to access this page ', 'danger')
        return redirect(url_for('login'))    
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
        flash('Product inserted successfully','success')
        return redirect(url_for('products'))
    return redirect(url_for('products'))
 
@app.route('/update_product', methods=['GET','POST'])
def update_products():
    if request.method=='POST':
        id=request.form['id']
        pname=request.form['name']
        bp=request.form['bp']
        sp=request.form['sp']
        update_product(pname,bp,sp,id)
        flash('Product updated successfully','success')
        return redirect(url_for('products'))
    return redirect(url_for('products'))

@app.route('/delete_products',methods=['GET','POST'])
def del_product():
    if request.method=='POST':
        delete=request.form['del']
        delete_product(delete)
        flash('Product deleted successfully','success')
        return redirect(url_for('products'))
    return redirect(url_for('products'))

@app.route('/sales')
def sales():
    if 'email' in session:
        my_sales=fetch_data('sales')
        # print(my_sales)
        product=fetch_data('products')
    else:
        flash('login to access this page ', 'danger')
        return redirect(url_for('login'))
    return render_template('/sales.html', sale=my_sales,prods=product)

@app.route('/add_sales',methods=['GET','POST'])
def add_sales():
    if request.method=='POST':
        # sid=request.form['sid']
        spid=request.form['spid']
        quantity=request.form['quantity']
        

        new_sales=(spid,quantity)
        insert_sales(new_sales)
        flash('Sale inserted successfully','success')
        return redirect(url_for('sales'))
    return redirect(url_for('sales'))
@app.route('/update_sale', methods=['GET','POST'])
def update_sales():
    if request.method=='POST':
        print('outside')
        quantity=request.form['quantity']
        spid=request.form['id']
        update_sale(quantity,spid)
        flash('Sale updated successfully','success')
        return redirect(url_for('sales'))
    
    return redirect(url_for('sales'))
@app.route('/stock')
def stock():
    if 'email' in session:
        my_stock=fetch_data('stock')
    # print(my_stock)
        my_prod=fetch_data('products')
    else:
        flash('login to access this page ', 'danger')
        return redirect(url_for('login'))
    return render_template('/stock.html', mystock=my_stock, my_prods=my_prod)

@app.route('/add_stock',methods=['GET','POST'])
def add_stock():
    if request.method=='POST':
        # stid=request.form['stid']
        pid=request.form['stpid']
        stockquantity=request.form['stockquantity']

        new_stock=(stockquantity,pid)
        insert_stock(new_stock)
        flash('Stock inserted successfully','success')
        return redirect(url_for('stock'))
    return redirect(url_for('stock'))

@app.route('/update_stock', methods=['GET','POST'])
def edit_stock():
    if request.method=='POST':
        pid=request.form['id']
        stockquantity=request.form['stockquantity']
        update_stock(stockquantity,pid)
        flash('Stock updated successfully','success')
        return redirect(url_for('stock'))
    return redirect(url_for('stock'))

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        print(session.get('email'))
        profits=get_profit()
        # print(profits)
        product_names=[]
        product_profits=[]
        for i in profits:
            product_names.append(i[0])
            product_profits.append(float(i[2]))

        my_sales=get_sales()
        print(my_sales)
        sales_name=[]
        per_product=[]
        for i in my_sales:
            sales_name.append(i[0])
            per_product.append(float(i[2]))

        profit_day=profit_per_day()
        print(profit_day)
        my_profit=[]
        day=[]
        for i in profit_day:
            day.append(str(i[0]))
            my_profit.append(float(i[1]))

        sales_day=sales_per_day()
        print(sales_day)
        mysales=[]
        days=[]
        for i in sales_day:
            days.append(str(i[0]))
            mysales.append(float(i[1]))

        tsales=total_sales()
        print(tsales)
        tprofit=total_profit()
    else:
        flash('login to access this page ', 'danger')
        return redirect(url_for('login'))
    return render_template('dashboard.html', pnames=product_names,pprofits=product_profits,sale=sales_name,per_product=per_product,my_profit=my_profit,day=day,days=days, mysales=mysales,tsales=tsales,tprofit=tprofit)


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        fname=request.form['fname']
        lname=request.form['lname']
        email=request.form['email']
        password=request.form['password']
        h_pass=bcrypt.generate_password_hash(password).decode('UTF-8')

        new_user=(fname,lname,email,h_pass)
        check=check_email(email)
        if check==None:
            insert_users(new_user)
            flash('Registration Successful','success')
            return redirect(url_for('login'))
        else:
            flash('User Exists use a different email','danger')
            return render_template('register.html')
    return render_template('register.html')

@app.route('/login' ,methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        check=check_email(email)
        print(check)
        if check==None:
            flash('user does not exist register','danger')
            return redirect(url_for('register'))
        else:
            if bcrypt.check_password_hash(check[4],password):
                session['email']=email
                flash('login successful','success')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong Password or email','danger')
                return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email')
    flash('Youve been logged out', 'success')
    return redirect(url_for('login'))

app.run(debug=True)
