#!/usr/bin/python
import textwrap
from flask import Flask, render_template
from flask import request, redirect
from flask import url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Book, BookItem
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Books Library"


# Connecting to the bookitem database
engine = create_engine('sqlite:///bookitem.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Creating a login session with anti-forgery token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # Rendering the login page for user to login first
    return render_template('login.html', STATE=state)


# The gconnet function to connect the login page to the
# books page
# Create anti-forgery state token
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps(
            'Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(
            'client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade code.'), 401)
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
        response = make_response(json.dumps(result.get(
            'error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token ID doesn't match user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token clientID doesn't match appID."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user already connected.'), 200)
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

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;"'
    '"border-radius: 150px;-webkit-border-radius: 150px;"'
    '"-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# gdisconnect function disconnects the user from the webpage
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps(
            'User not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps(
            'Successfully logged out.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Function that calls on a JSON API Endpoint as a GET rEQUEST
@app.route('/books/<int:book_id>/item/JSON')
def bookItemJSON(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    items = session.query(BookItem).filter_by(
        book_id=book_id).all()
    return jsonify(BookItem=[i.serialize for i in items], book=book)


# Returning the JSON Endpoints of the books
# category and the books items
@app.route('/books/<int:book_id>/item/JSON')
def bookListItemJSON(book_id, item_id):
    bookItem = session.query(BookItem).filter_by(id=item_id).one()
    return jsonify(BookItem=bookItem.serialize)


# The pages that are shown to the users who are not loged in
# the books categories and the books title, price, and description
@app.route('/books/JSON')
def booksJSON():
    books = session.query(Book).all()
    return jsonify(books=[r.serialize for r in books])


@app.route('/')
@app.route('/books/<int:book_id>/')
def bookItem(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    items = session.query(BookItem).filter_by(book_id=book.id)
    return render_template('book.html', book=book, items=items)

# Creating a fucntion that will return the new books in each category


@app.route('/books/<int:book_id>/new/', methods=['GET', 'POST'])
def newBookItem(book_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = BookItem(name=request.form['name'], book_id=book_id)
        session.add(newItem)
        session.commit()
        flash("A new book has been added")
        return redirect(url_for('bookItem', book_id=book_id))
    else:
        return render_template('newbookitem.html', book_id=book_id)


# Creatin a function route for editing
# the book item
@app.route('/books/<int:book_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editBookItem(book_id, item_id):
    editedItem = session.query(BookItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash("A book has been editted")
        return redirect(url_for('bookItem', book_id=book_id))
    else:
        return render_template('editbookitem.html',
                               book_id=book_id, item_id=item_id,
                               item=editedItem)


# Creating the  delete route function for the
# book items
@app.route('/books/<int:book_id>/\
<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteBookItem(book_id, item_id):
    itemToDelete = session.query(BookItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("A book has been deleted")
        return redirect(url_for('bookItem', book_id=book_id))
    else:
        return render_template('deletebook.html', item=itemToDelete)


# The function runs the application
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
app.run(host='0.0.0.0', port=5000)
