from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Data_Setup import Base, CategoryName, ItemName, GmailUser
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///items.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Creamy Corner"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
cat_nam = session.query(CategoryName).all()

# completed
# login


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    cat_nam = session.query(CategoryName).all()
    i_nam = session.query(ItemName).all()
    return render_template('login.html',
                           STATE=state, cat_nam=cat_nam, i_nam=i_nam)
    # return render_template('myhome.html', STATE=state
    # cat_nam=cat_nam,i_nam=i_nam)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    otp = ''
    otp += '<h1>Welcome, '
    otp += login_session['username']
    otp += '!</h1>'
    otp += '<img src="'
    otp += login_session['picture']
    otp += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return otp


# User Helper Functions
def createUser(login_session):
    User1 = GmailUser(name=login_session['username'], email=login_session[
                   'email'])
    session.add(User1)
    session.commit()
    user = session.query(
                         GmailUser).filter_by(
                         email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(GmailUser).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(GmailUser).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

# completed
# Home


@app.route('/')
@app.route('/home')
def home():
    cat_nam = session.query(CategoryName).all()
    return render_template('myhome.html', cat_nam=cat_nam)
# completed
# Category for admins


@app.route('/CreamyCorner')
def CreamyCorner():
    try:
        if login_session['username']:
            name = login_session['username']
            cat_nam = session.query(CategoryName).all()
            its = session.query(CategoryName).all()
            i_nam = session.query(ItemName).all()
            return render_template('myhome.html', cat_nam=cat_nam,
                                   its=its, i_nam=i_nam, uname=name)
    except:
        return redirect(url_for('showLogin'))

#
# Showing Items based on Category


@app.route('/CreamyCorner/<int:itid>/showCategory')
def showCategory(itid):
    if 'username' in login_session:
        cat_nam = session.query(CategoryName).all()
        its = session.query(CategoryName).filter_by(id=itid).one_or_none()
        i_nam = session.query(ItemName).filter_by(categorynameid=itid).all()
        try:
            if login_session['username']:
                return render_template('showCategory.html', cat_nam=cat_nam,
                                       its=its, i_nam=i_nam,
                                       uname=login_session['username'])
        except:
            return render_template('showCategory.html',
                                   cat_nam=cat_nam, its=its, i_nam=i_nam)
    else:
        flash("You must login first")
        return render_template('login.html')

#####
# Add a New category i.e; flavour


@app.route('/CreamyCorner/addCategory', methods=['POST', 'GET'])
def addCategory():
    if 'username' in login_session:
        if request.method == 'POST':
            com = CategoryName(name=request.form['name'],
                               user_id=login_session['user_id'])
            session.add(com)
            session.commit()
            return redirect(url_for('CreamyCorner'))
        else:
            return render_template('addCategory.html', cat_nam=cat_nam)
    else:
        flash("You must login first")
        return render_template('login.html')

#
# Edit a Category name


@app.route('/CreamyCorner/<int:itid>/edit', methods=['POST', 'GET'])
def editCategory(itid):
    if 'username' in login_session:
        editCategory = session.query(CategoryName).filter_by(id=itid).one()
        creator = getUserInfo(editCategory.user_id)
        user = getUserInfo(login_session['user_id'])
        # If logged in user != item owner redirect them
        if creator.id != login_session['user_id']:
            flash("You cannot edit this category."
                  "This is belongs to %s" % creator.name)
            return redirect(url_for('CreamyCorner'))
        if request.method == "POST":
            if request.form['name']:
                editCategory.name = request.form['name']
                session.add(editCategory)
            session.commit()
            flash("Category Edited Successfully")
            return redirect(url_for('CreamyCorner'))
        else:
            # cat_nam is global variable we can them in entire application
            return render_template('editCategory.html',
                                   it=editCategory, cat_nam=cat_nam)
    else:
        flash("You must login first")
        return render_template('login.html')

######
# Delete Category


@app.route('/CreamyCorner/<int:itid>/delete', methods=['POST', 'GET'])
def deleteCategory(itid):
    if 'username' in login_session:
        it = session.query(CategoryName).filter_by(id=itid).one()
        creator = getUserInfo(it.user_id)
        user = getUserInfo(login_session['user_id'])
        # If logged in user != item owner redirect them
        if creator.id != login_session['user_id']:
            flash("You cannot Delete this Category."
                  "This is belongs to %s" % creator.name)
            return redirect(url_for('CreamyCorner'))
        if request.method == "POST":
            session.delete(it)
            session.commit()
            flash("Category Deleted Successfully")
            return redirect(url_for('CreamyCorner'))
        else:
            return render_template(
                'deleteCategory.html', it=it, cat_nam=cat_nam)
    else:
        flash("You must login first")
        return render_template('login.html')

######
# Add New Category  Name Details


@app.route('/CreamyCorner/addCategory/addItemDetails/<string:itname>/add',
           methods=['GET', 'POST'])
def addItemDetails(itname):
    if 'username' in login_session:
        its = session.query(CategoryName).filter_by(name=itname).one()
        # See if the logged in user is not the owner of item
        creator = getUserInfo(its.user_id)
        user = getUserInfo(login_session['user_id'])
        # If logged in user != item owner redirect them
        if creator.id != login_session['user_id']:
            flash("You can't add new item ."
                  "This is belongs to %s" % creator.name)
            return redirect(url_for('showCategory', itid=its.id))
        if request.method == 'POST':
            itemname = request.form['itemname']
            brand = request.form['brand']
            rating = request.form['rating']
            price = request.form['price']
            packing = request.form['packing']
            itemdetails = ItemName(itemname=itemname,
                                   brand=brand, rating=rating,
                                   price=price, packing=packing,
                                   date=datetime.datetime.now(),
                                   categorynameid=its.id,
                                   gmailuser_id=login_session['user_id'])
            session.add(itemdetails)
            session.commit()
            return redirect(url_for('showCategory', itid=its.id))
        else:
            return render_template('addItemDetails.html',
                                   itname=its.name, cat_nam=cat_nam)
    else:
        flash("You must login first")
        return render_template('login.html')
######
# Edit Item details


@app.route('/CreamyCorner/<int:itid>/<string:itemname>/edit',
           methods=['GET', 'POST'])
def editItem(itid, itename):
    if 'username' in login_session:
        it = session.query(CategoryName).filter_by(id=itid).one()
        itemdetails = session.query(ItemName).filter_by(itemname=itename).one()
        # See if the logged in user is not the owner of item
        creator = getUserInfo(it.user_id)
        user = getUserInfo(login_session['user_id'])
        # If logged in user != item owner redirect them
        if creator.id != login_session['user_id']:
            flash("You can't edit this item"
                  "This is belongs to %s" % creator.name)
            return redirect(url_for('showCategory', itid=it.id))
        # POST methods
        if request.method == 'POST':
            itemdetails.itemname = request.form['itemname']
            itemdetails.brand = request.form['brand']
            itemdetails.rating = request.form['rating']
            itemdetails.price = request.form['price']
            itemdetails.packing = request.form['packing']
            itemdetails.date = datetime.datetime.now()
            session.add(itemdetails)
            session.commit()
            flash("Item Edited Successfully")
            return redirect(url_for('showCategory', itid=itid))
        else:
            return render_template('editItem.html',
                                   itid=itid, itemdetails=itemdetails,
                                   cat_nam=cat_nam)
    else:
        flash("You must login first")
        return render_template('login.html')
#####
# Delete Edit


@app.route('/CreamyCorner/<int:itid>/<string:itename>/delete',
           methods=['GET', 'POST'])
def deleteItem(itid, itename):
    if 'username' in login_session:
        it = session.query(CategoryName).filter_by(id=itid).one()
        itemdetails = session.query(ItemName).filter_by(itemname=itename).one()
        # See if the logged in user is not the owner of item
        creator = getUserInfo(it.user_id)
        user = getUserInfo(login_session['user_id'])
        # If logged in user != item owner redirect them
        if creator.id != login_session['user_id']:
            flash("You can't delete this item"
                  "This is belongs to %s" % creator.name)
            return redirect(url_for('showCategory', itid=it.id))
        if request.method == "POST":
            session.delete(itemdetails)
            session.commit()
            flash("Deleted item Successfully")
            return redirect(url_for('showCategory', itid=itid))
        else:
            return render_template('deleteItem.html',
                                   itid=itid,
                                   itemdetails=itemdetails,
                                   cat_nam=cat_nam)
    else:
        flash("You must login first")
        return render_template('login.html')
####
# Logout from current user


@app.route('/logout')
def logout():
    if 'username' in login_session:
        access_token = login_session['access_token']
        print ('In gdisconnect access token is %s', access_token)
        print ('User name is: ')
        print (login_session['username'])
        if access_token is None:
            print ('Access Token is None')
            response = make_response(
                json.dumps('Current user not connected....'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        access_token = login_session['access_token']
        url = 'https://accounts.google.com/'
        'o/oauth2/revoke?token=%s' % access_token
        h = httplib2.Http()
        result = \
            h.request(uri=url, method='POST', body=None, headers={
                'content-type': 'application/x-www-form-urlencoded'})[0]

        print (result['status'])
        if result['status'] == '200':
            del login_session['access_token']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            response = make_response(json.dumps(
                'Successfully disconnected user..'), 200)
            response.headers['Content-Type'] = 'application/json'
            flash("Successful logged out")
            return redirect(url_for('showLogin'))
            # return response
        else:
            response = make_response(
                json.dumps('Failed to revoke token for given user.', 400))
            response.headers['Content-Type'] = 'application/json'
            return response
    else:
        flash("You must login first")
        return render_template('login.html')
#####
# Json
# Displays all the items in each and every category


@app.route('/CreamyCorner/JSON')
def allItemJSON():
    category = session.query(CategoryName).all()
    category_dict = [c.serialize for c in category]
    for c in range(len(category_dict)):
        item = [i.serialize for i in session.query(
            ItemName).filter_by(categorynameid=category_dict[c]["id"]).all()]
        if item:
            category_dict[c]["item"] = item
    return jsonify(CategoryName=category_dict)

####
# Displays all the categories


@app.route('/CreamyCorner/Category/JSON')
def categoriesJSON():
    item = session.query(CategoryName).all()
    return jsonify(Category=[c.serialize for c in item])

####
# Displays all items


@app.route('/CreamyCorner/item/JSON')
def itemsJSON():
    items = session.query(ItemName).all()
    return jsonify(item=[i.serialize for i in items])

#####
# Displays all the items in a category as required based on the category name
'''
    Enter the name of the required flavour in the path
            as specified to view the items
    For E.g.;
        'localhost:4444/CreamyCorner/Vanilla/item/JSON'
'''


@app.route('/CreamyCorner/<path:flavour_name>/item/JSON')
def categoryItemsJSON(flavour_name):
    category = session.query(CategoryName).filter_by(name=flavour_name).one()
    item = session.query(ItemName).filter_by(categoryname=category).all()
    return jsonify(items=[i.serialize for i in item])

#####
''' Displays all the items in a category as required,
        based on the category name and the brand name provided

    Enter the name of the required flavour and brand names ;
        in the path as specified to view the items
    For E.g.;
        'localhost:4444/CreamyCorner/Chocolate/Amul/JSON'
'''


@app.route('/CreamyCorner/<path:flavour_name>/<path:brand_name>/JSON')
def ItemJSON(flavour_name, brand_name):
    category = session.query(CategoryName).filter_by(name=flavour_name).one()
    items = session.query(ItemName).filter_by(
           categoryname=category, brand=brand_name).all()
    return jsonify(items=[i.serialize for i in items])


if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=4444)
