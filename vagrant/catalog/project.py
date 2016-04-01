from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify, session
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
        return cursor.query(User).filter_by(id=uid).first()
    return None

@app.route('/categories/<string:category_name>/JSON')
def categoryJSON(category_name):
    category = cursor.query(Category).filter_by(name=category_name).one()
    items = cursor.query(Item).filter_by(
        category_id=category.id).all()
    return jsonify(Items=[i.serialize for i in items])

@app.route('/categories/<string:category_name>/<string:item_name>/JSON')
def itemJSON(category_name, item_name):
    item = cursor.query(Item).filter_by(name=item_name).one()
    return jsonify(Item=item.serialize)

@app.route('/', methods=['GET', 'POST'])
@app.route('/catalog', methods=['GET', 'POST'])
def catalogMain():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = cursor.query(User).filter_by(username=username).first()
        if user and (user.password == password):
            session['id'] = user.id
        else:
            session['id'] = None
    else:
        user = current_user()

    categories = cursor.query(Category).all()
    items = cursor.query(Item).order_by(Item.id.desc()).join(Category,
        Item.category_id == Category.id).add_columns(Item.id, Item.name,
                                                     Item.category_id,
                                                     Category.name).limit(10)
    return render_template('catalog.html', items=items, categories=categories,
                           user=user)

@app.route('/catalog/<string:category_name>')
def categoryItems(category_name):
    categories = cursor.query(Category).all()
    category = cursor.query(Category).filter_by(name=category_name).one()
    items = cursor.query(Item).filter_by(category_id=category.id)
    user = current_user()
    return render_template('category.html', category=category, items=items,
                           categories=categories, user=user)

@app.route('/catalog/<string:category_name>/<string:item_name>')
def selectItem(category_name, item_name):
    categories = cursor.query(Category).all()
    category = cursor.query(Category).filter_by(name=category_name).first()
    item = cursor.query(Item).filter_by(name=item_name).first()
    user = current_user()
    return render_template('item.html', categories=categories, item=item,
                           user=user, category=category)

@app.route('/catalog/login')
def login():
    categories = cursor.query(Category).all()
    return render_template('login.html', categories=categories)

@app.route('/catalog/logout')
def logout():
    session['id'] = None
    return redirect(url_for('catalogMain'))

@app.route('/catalog/<string:category_name>&<int:category_id>/new/',
           methods=['GET', 'POST'])
def newItem(category_name, category_id):
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
        user = current_user()
        return render_template('newitem.html', category=category,
                               categories=categories, user=user)

@app.route('/catalog/NewCategory', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        cursor.add(newCategory)
        cursor.commit()
        flash("New category created!")
        return redirect(url_for('catalogMain'))
    else:
        categories = cursor.query(Category).all()
        user = current_user()
        return render_template('newcategory.html', categories=categories,
                               user=user)
    
@app.route('/catalog/<string:category_name>/<string:item_name>/edit',
           methods=['GET', 'POST'])
def editItem(category_name, item_name):
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
        user = current_user()
        return render_template(
            'edititem.html', item=editedItem, category=category,
            categories=categories, user=user)

@app.route('/catalog/<string:category_name>/<string:item_name>/delete',
           methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    itemToDelete = cursor.query(Item).filter_by(name=item_name).first()
    category = cursor.query(Category).filter_by(name=category_name).first()
    if request.method == 'POST':
        cursor.delete(itemToDelete)
        cursor.commit()
        flash("Item deleted!")
        return redirect(url_for('categoryItems', category_name=category.name))
    else:
        categories = cursor.query(Category).all()
        user = current_user()
        return render_template('deleteitem.html', item=itemToDelete,
                               categories=categories, user=user,
                               category=category)
    
@app.route('/catalog/<string:category_name>/delete', methods=['GET', 'POST'])
def deleteCategory(category_name):
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
        user = current_user()
        return render_template('deletecategory.html', category=category,
                               categories=categories, user=user)

    
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
