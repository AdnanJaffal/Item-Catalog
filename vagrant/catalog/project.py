from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

app = Flask(__name__)

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
cursor = DBSession()

# OAuth code
def current_user():
    if 'id' in session:
        uid = session['id']
        return cursor.query(User).filter_by(id=uid).one()
    return None

@app.route('/categories/<int:category_id>/item/JSON')
def categoryJSON(category_id):
    category = cursor.query(Category).filter_by(id=category_id).one()
    items = cursor.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])

@app.route('/categories/<int:category_id>/item/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    item = cursor.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=item.serialize)

@app.route('/', methods=['GET', 'POST'])
@app.route('/catalog', methods=['GET', 'POST'])
def catalogMain():
    if request.method == 'POST':
        username = request.form['username']
        user = cursor.query(User).filter_by(username=username).first()
        print user
        if user:
            session['id'] = user.id
    else:
        user = current_user()

    categories = cursor.query(Category).all()
    items = cursor.query(Item).order_by(Item.id).limit(10)
    return render_template('catalog.html', items=items, categories=categories, user=user)

@app.route('/catalog/<string:category_name>')
def categoryItems(category_name):
    categories = cursor.query(Category).all()
    category = cursor.query(Category).filter_by(name=category_name).first()
    print category
    items = cursor.query(Item).filter_by(category_id=category.id)
    user = current_user()
    return render_template('category.html', category=category, items=items, categories=categories, user=user)

@app.route('/catalog/<int:category_id>/<string:item_name>')
def loadItem(item_id, item_name, category_id):
    print category_id
    print item_id
    print item_name
    categories = cursor.query(Category).all()
    print categories
    items = cursor.query(Item).filter_by(id=item_id)
    print items
    user = current_user()
    print user
    return render_template('item.html', items=items, categories=categories, user=user)

@app.route('/catalog/login')
def login():
    categories = cursor.query(Category).all()
    return render_template('login.html', categories=categories)

# Task 1: Create route for newItem function here


@app.route('/category/<int:category_id>/new/', methods=['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'], category_id=category_id)
        cursor.add(newItem)
        cursor.commit()
        flash("New item item created!")
        return redirect(url_for('categoryMenu', category_id=category_id))
    else:
        return render_template('newmenuitem.html', category_id=category_id)

# Task 2: Create route for editItem function here


@app.route('/categories/<int:category_id>/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    editedItem = cursor.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        cursor.add(editedItem)
        cursor.commit()
        flash("Menu item edited!")
        return redirect(url_for('categoryMenu', category_id=category_id))
    else:
        return render_template(
            'editmenuitem.html', category_id=category_id, item_id=item_id, item=editedItem)

# Task 3: Create a route for deleteItem function here


@app.route('/categories/<int:category_id>/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    itemToDelete = cursor.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        cursor.delete(itemToDelete)
        cursor.commit()
        flash("Menu item deleted!")
        return redirect(url_for('categoryMenu', category_id=category_id))
    else:
        return render_template('deleteconfirmation.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
