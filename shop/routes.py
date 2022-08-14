from xml.dom.minidom import Element
from flask import Flask, render_template, url_for, request, redirect, flash, session, json #imports
from shop import app, db #(importing app from __init__ which sets up FLask)
from shop.models import Items, User
from shop.forms import RegistrationForm, LoginForm, CheckoutForm, SortGalleryForm
from flask_login import login_user, logout_user, current_user, login_required
from flask_session import Session


@app.route('/')
@app.route('/loading') #loading page for setting up the specific session to each browser, including the cart list
def loading():
    cart_list = []
    session['cart_list'] = cart_list
    return redirect(url_for('home'))


@app.route('/home', methods = ['GET', 'POST'])
def home():
    sort_form = SortGalleryForm() #form for sorting items on home page
    items = Items.query.all() #get every item in the database for sale
    if sort_form.validate_on_submit(): #when the sorting form is submitted, sort items list depending on choice
        if sort_form.sort_type.data == "price_high":
            items = Items.query.order_by(Items.price.desc())
        elif sort_form.sort_type.data == "price_low":
            items = Items.query.order_by(Items.price.asc())
        elif sort_form.sort_type.data == "ecological":
            items = Items.query.order_by(Items.carbon_footprint.asc())
    # if request.method == "POST": #when the details form is submitted
    #     req = request.form #variable for the form details sent
    #     for item in items: #loop through every item
    #         if item.name in req: #check to see if that item was clicked on
    #             item_list = [item.name, item.description, item.ecological_impact, item.provider, item.origins]
    #             session["item"] = item_list #store details in the session
    #             return redirect(url_for('details')) #show the details of that specific item
                    
                
    return render_template('home.html', title="Home", items=items, form = sort_form)

@app.route('/home/details',methods = ['GET', 'POST']) #shows details of a specific item
def details():
    item_id = request.form.get("itemid")
    if item_id:
        item = Items.query.filter_by(id = item_id).first()
        return render_template('details.html', title = "Details", item = item)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #session['username'] = form.username.data
        if user is not None and user.verify_password(form.password.data):
            cart_temp = session.get('cart_list', None)
            login_user(user)
            session['cart_list'] = cart_temp
            #flash(session.get('cart_list', None))
            flash('You\'ve successfully logged in.')
            return redirect(url_for('home'))
        #errors = json.dumps(form.username.errors)
        #session['errors'] = errors
        return redirect(url_for('login_error'))
    return render_template('login.html', title = 'Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    session.pop('username', None)
    flash('Logout successful. Bye!')
    return redirect(url_for('home'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, password = form.password.data, email = form.email.data)
        db.session.add(user)
        db.session.commit()
        #session["name"] = request.form.get("username")
        #flash('Registration successful!')
        return redirect(url_for('registered'))
    return render_template('register.html', title = 'Register', form=form)

@app.route('/registered')
def registered():
    return render_template('registered.html', title = "Thanks!")

@app.route('/login_error')
def login_error():
    #errors = request.args['errors']
    #errors = session['errors']
    return render_template('login_error.html', title = "Login Error") #errors = json.loads(errors))

@app.route('/cart', methods = ['GET', 'POST'])
def cart():
    cart = Items.query.filter(Items.id.in_(session['cart_list'])).all() #get every item stored in the session cart list
    item_id = request.form.get("itemid") #get the item id of an item from home to be added to the cart
    if request.method == "POST": #for checkout, removing and adding items
        req = request.form
        if "checkout" in req and current_user.is_authenticated: #if checkout clicked and user logged in
            return redirect(url_for('checkout'))
        elif "checkout" in req and not current_user.is_authenticated: #if checkout clicked and user not logged in
            flash('You must be logged in to checkout')
        elif item_id: #if an item is to be added to the cart
            session['cart_list'].append(item_id) #add id of the item to the session cart list
            session.modified = True
            cart = Items.query.filter(Items.id.in_(session['cart_list'])).all() #get every item in the cart
            return redirect(url_for('home')) #return to home page, as this is where items are added
        else:
            for cart_item in session['cart_list']: #when removing items
                if cart_item in req:
                    session['cart_list'].remove(cart_item)
                    session.modified = True
                    cart = []
                    for i in session["cart_list"]:
                        cart += Items.query.filter_by(id=i).all()
                    return render_template('cart.html', title = 'Cart', cart=cart)

    cart = []
    for i in session["cart_list"]:
        cart += Items.query.filter_by(id=i).all()
    return render_template('cart.html', title = 'Cart', cart=cart)

@app.route('/checkout', methods = ['GET', 'POST'])
@login_required
def checkout():
    #if 'username' not in session:
        #return "You have not yet logged in, <a href = 'login'> click here to login </a>"
    #else:
    form = CheckoutForm()
    if form.validate_on_submit():
        return redirect(url_for('checkout_success'))
    return render_template('checkout.html', form=form, user=current_user.username)

@app.route('/checkout_success')
def checkout_success():
    return render_template('checkout_success')