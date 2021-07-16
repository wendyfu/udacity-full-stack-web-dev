from flask import (
    flash, Flask, g, jsonify, make_response,
    Markup, redirect, render_template, request,
    session as login_session, url_for
)

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

from user import *
import random
import string
import httplib2
import json
import requests

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
# Check if a user has logged in


@app.before_request
def load_logged_in_user():
    if login_session.get('state') is None:
        login_session['state'] = ''.join(
            random.choice(
                string.ascii_uppercase +
                string.digits) for x in range(32))

    g.STATE = login_session['state']
    username = login_session.get('username')

    if username is None:
        g.user = None
    else:
        g.user = 'getUserInfo(username)'

# Handle login with Google


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
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
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
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    response = make_response(json.dumps('Successfully logged in'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response

# Handle logout


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['state']
        return redirect('/catalog')
    else:
        response = make_response(
            json.dumps(
                'Failed to revoke token for given user.',
                400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON APIs to retrieve all catalog items


@app.route('/catalog.json')
def catalogJSON():
    db_categories = session.query(Category).all()
    categories = []

    for c in db_categories:
        items = session.query(Item).filter_by(category_id=c.id).all()
        category = c.serialize

        if (len(items) > 0):
            category['Item'] = []

        for i in items:
            category['Item'].append(i.serialize)

        categories.append(category)

    return jsonify(Category=categories)

# JSON API to retriever certain catalog items


@app.route('/catalog/<string:name>/<string:title>.json')
def catalogItemJSON(name, title):
    item = session.query(Item).filter_by(title=title).one()
    return jsonify(Item=item.serialize)

# The homepage displays all current categories with 10 latest added items


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    categories = session.query(Category)
    items = session.query(Item).order_by(desc(Item.id)).limit(10)
    return render_template('catalog.html', categories=categories, items=items)

# Show all items available for selected category


@app.route('/catalog/<string:name>/items')
def showCategoryDetails(name):
    categories = session.query(Category)
    category = categories.filter_by(name=name).one()
    items = session.query(Item).filter_by(category_id=category.id).all()
    size = len(items)
    return render_template(
        'category.html',
        name=name,
        categories=categories,
        items=items,
        size=size)

# Show specific information about selected item


@app.route('/catalog/<string:name>/<string:title>')
def showItemDetails(name, title):
    item = session.query(Item).filter_by(title=title).one()
    return render_template('item.html', item=item)

# Add an item


@app.route('/catalog/new', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        flash('You are not logged in!')
        return render_template('newItem.html')

    if request.method == 'POST':
        category = session.query(Category).filter_by(
            id=request.form['category']).one()

        # Check if item already exist
        existingItem = session.query(Item).filter_by(
            title=request.form['title']).first()
        if existingItem is not None:
            flash(
                Markup(
                    '<div class="flash text-danger">Item \
                        %s already exist</div>'
                    % existingItem.title))
            return redirect(
                url_for(
                    'showItemDetails',
                    name=category.name,
                    title=existingItem.title))

        newItem = Item(
            user_id=login_session['email'],
            title=request.form['title'],
            description=request.form['description'],
            category=category)
        session.add(newItem)
        flash(
            Markup(
                '<div class="flash text-success">New item \
                    %s successfully created</div>'
                % newItem.title))
        session.commit()
        return redirect(
            url_for(
                'showItemDetails',
                name=category.name,
                title=newItem.title))

    categories = session.query(Category)
    return render_template('newItem.html', categories=categories)

# Edit an item


@app.route('/catalog/<string:title>/edit/', methods=['GET', 'POST'])
def editItem(title):
    item = session.query(Item).filter_by(title=title).first()

    if item is None:
        flash(
            Markup(
                '<div class="flash text-danger">Requested \
                    item %s does not exist</div>' %
                title))
        return redirect(url_for('showCatalog'))

    if 'username' not in login_session:
        flash(Markup('<div class="flash text-danger">\
            You are not logged in!</div>'))
        return redirect(
            url_for(
                'showItemDetails',
                name=item.category.name,
                title=item.title))

    if item.user_id != login_session['email']:
        flash(Markup(
            '<div class="flash text-danger">You \
            have no authorization to edit this item!</div>'))
        return redirect(
            url_for(
                'showItemDetails',
                name=item.category.name,
                title=item.title))

    if request.method == 'POST':
        if request.form['title']:
            item.title = request.form['title']
        if request.form['description']:
            item.description = request.form['description']
        if request.form['category']:
            category = session.query(Category).filter_by(
                id=request.form['category']).one()
            item.category = category

        session.add(item)
        flash(
            Markup(
                '<div class="flash text-success">Item \
                    %s successfully edited</div>' %
                item.title))
        session.commit()
        return redirect(
            url_for(
                'showItemDetails',
                name=category.name,
                title=item.title))

    categories = session.query(Category)
    return render_template('editItem.html', item=item, categories=categories)

# Delete an item


@app.route('/catalog/<string:title>/delete/', methods=['GET', 'POST'])
def deleteItem(title):
    item = session.query(Item).filter_by(title=title).first()

    if item is None:
        flash(
            Markup(
                '<div class="flash text-danger">\
                Requested item %s does not exist</div>' %
                title))
        return redirect(url_for('showCatalog'))

    if 'username' not in login_session:
        flash(Markup('<div class="flash text-danger">\
            You are not logged in!</div>'))
        return redirect(
            url_for(
                'showItemDetails',
                name=item.category.name,
                title=item.title))

    if item.user_id != login_session['email']:
        flash(Markup(
            '<div class="flash text-danger">\
            You have no authorization to delete this item!</div>'))
        return redirect(
            url_for(
                'showItemDetails',
                name=item.category.name,
                title=item.title))

    if request.method == 'POST':
        session.delete(item)
        flash(
            Markup(
                '<div class="flash text-success">\
                Succesfully deleted %s</div>' %
                title))
        session.commit()
        return redirect(url_for('showCatalog'))

    return render_template('deleteItem.html', item=item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
