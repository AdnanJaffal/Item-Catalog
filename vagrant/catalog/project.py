from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify, session, make_response
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
import random, string, httplib2, json, requests

app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
cursor = DBSession()

CLIENT_ID = json.loads(open('client_secret.json', 'r').
                       read())['web']['client_id']

@app.route('/catalog/<string:category_name>/JSON')
def categoryJSON(category_name):
    """Returns the JSON of the current category.

       Args:
           category_name: The name of the category.
    """
    
    category = cursor.query(Category).filter_by(name=category_name).one()
    items = cursor.query(Item).filter_by(
        category_id=category.id).all()
    return jsonify(Items=[i.serialize for i in items])

@app.route('/catalog/<string:category_name>/<string:item_name>/JSON')
def itemJSON(category_name, item_name):
    """Returns the JSON of the current item.

       Args:
           category_name: The name of the category.
           item_name: The name of the item.
    """
    item = cursor.query(Item).filter_by(name=item_name).one()
    return jsonify(Item=item.serialize)

@app.route('/')
@app.route('/catalog')
def catalogMain():
    """The main page of the catalog app.

       Args:
           None

       Returns:
           Rendered page.
    """
    if 'username' in session:
        user = session['username']
    else:
        user = None    
    
    categories = cursor.query(Category).all()
    items = cursor.query(Item).order_by(Item.id.desc()).join(Category,
        Item.category_id == Category.id).add_columns(Item.id, Item.name,
                                                     Item.category_id,
                                                     Category.name).limit(10)
    return render_template('catalog.html', items=items, categories=categories,
                           user=user)

@app.route('/catalog/<string:category_name>')
def categoryItems(category_name):
    """Displays all the items for the selected category.

       Args:
           category_name: The name of the selected category.

       Returns:
           Rendered page.
    """
    if 'username' in session:
        user = session['username']
    else:
        user = None
    
    categories = cursor.query(Category).all()
    category = cursor.query(Category).filter_by(name=category_name).one()
    items = cursor.query(Item).filter_by(category_id=category.id)
    return render_template('category.html', category=category, items=items,
                           categories=categories, user=user)

@app.route('/catalog/<string:category_name>/<string:item_name>')
def selectItem(category_name, item_name):
    """Displays the description for the selected item.

       Args:
           category_name: The name of the selected category.
           item_name: The name of the selected item.

       Returns:
           Rendered page.
    """
    if 'username' in session:
        user = session['username']
    else:
        user = None
    
    categories = cursor.query(Category).all()
    category = cursor.query(Category).filter_by(name=category_name).first()
    item = cursor.query(Item).filter_by(name=item_name).first()
    return render_template('item.html', categories=categories, item=item,
                           user=user, category=category)

@app.route('/catalog/login')
def login():
    """The login page of the catalog app.

       Args:
           None

       Returns:
           Rendered page.
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for
                    x in xrange(32))
    session['state'] = state
    categories = cursor.query(Category).all()
    return render_template('login.html', categories=categories, STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Allows login through a google account.

       Args:
           None

       Returns:
           response: The response code if an error occurs.
           output: The name and image of the user who just logged in.
    """
    # Validate state token
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    ##access_token = credentials.access_token
    session['credentials'] = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % credentials.access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                 'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['credentials'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += session['username']
    output += '!</h1>'
    output += '<img src="'
    output += session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % session['username'])
    print "Done!"
    return output

@app.route("/gdisconnect")
def gdisconnect():
    """Logs out any user that is currently logged into the web app.

       Args:
           None

       Returns:
           response: The code to display if an error occurs.
           Redirects to the main page.
    """
    # Only disconnect a connected user
    credentials = session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP GET request to revoke current token.
    access_token = session.get('credentials')
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session.
        del session['credentials']
        del session['gplus_id']
        del session['username']
        del session['email']
        del session['picture']

        response = make_response(json.dumps('disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('catalogMain'))

@app.route('/catalog/<string:category_name>&<int:category_id>/new/',
           methods=['GET', 'POST'])
def newItem(category_name, category_id):
    """Creates a new item in a category.

       Args:
           category_name: The name of the selected category.
           item_name: The name of the selected item.

       Returns:
           POST: Redirects to the category page.
           GET: Rendered page.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'], description=request.form['description'],
            category_id=category_id)
        cursor.add(newItem)
        cursor.commit()
        flash("New item item created!")
        return redirect(url_for('categoryItems', category_name=category_name))
    else:
        category = cursor.query(Category).get(category_id)
        categories = cursor.query(Category).all()
        return render_template('newitem.html', category=category,
                               categories=categories)

@app.route('/catalog/NewCategory', methods=['GET', 'POST'])
def newCategory():
    """Creates a new category.

       Args:
           None

       Returns:
           POST: Redirects to the main page.
           GET: Rendered page.
    """
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        cursor.add(newCategory)
        cursor.commit()
        flash("New category created!")
        return redirect(url_for('catalogMain'))
    else:
        categories = cursor.query(Category).all()
        return render_template('newcategory.html', categories=categories)
    
@app.route('/catalog/<string:category_name>/<string:item_name>/edit',
           methods=['GET', 'POST'])
def editItem(category_name, item_name):
    """Edits an item in a category.

       Args:
           category_name: The name of the selected category.
           item_name: The name of the selected item.

       Returns:
           POST: Redirects to the category page.
           GET: Rendered page.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    editedItem = cursor.query(Item).filter_by(name=item_name).first()
    category = cursor.query(Category).filter_by(name=category_name).first()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
            editedItem.description = request.form['description']
        cursor.add(editedItem)
        cursor.commit()
        flash("Menu item edited!")
        return redirect(url_for('categoryItems', category_name=category.name))
    else:
        categories = cursor.query(Category).all()
        return render_template(
            'edititem.html', item=editedItem, category=category,
            categories=categories)

@app.route('/catalog/<string:category_name>/<string:item_name>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    """Deletes an item in a category.

       Args:
           category_name: The name of the selected category.
           item_name: The name of the selected item.

       Returns:
           POST: Redirects to the category page.
           GET: Rendered page.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    itemToDelete = cursor.query(Item).filter_by(name=item_name).first()
    category = cursor.query(Category).filter_by(name=category_name).first()
    if request.method == 'POST':
        cursor.delete(itemToDelete)
        cursor.commit()
        flash("Item deleted!")
        return redirect(url_for('categoryItems', category_name=category.name))
    else:
        categories = cursor.query(Category).all()
        return render_template('deleteitem.html', item=itemToDelete,
                               categories=categories, category=category)
    
@app.route('/catalog/<string:category_name>/delete', methods=['GET', 'POST'])
def deleteCategory(category_name):
    """Deletes a category.

       Args:
           category_name: The name of the selected category.

       Returns:
           POST: Redirects to the main page.
           GET: Rendered page.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    category = cursor.query(Category).filter_by(name=category_name).first()
    if request.method == 'POST':
        itemsToDelete = cursor.query(
            Item).filter_by(category_id=category.id).all()
        cursor.delete(category)
        cursor.commit()

        for item in itemsToDelete:
            cursor.delete(item)
            cursor.commit()

        flash("Category deleted!")
        return redirect(url_for('catalogMain'))
    else:
        categories = cursor.query(Category).all()
        return render_template('deletecategory.html', category=category,
                               categories=categories)

    
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
