from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_file import Base, Bank_Name, Customer_Details, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///bank_db.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Banks"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
gts_ca = session.query(Bank_Name).all()


# login for the user
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    gts_ca = session.query(Bank_Name).all()
    sbit = session.query(Customer_Details).all()
    return render_template('login.html',
                           STATE=state, gts_ca=gts_ca, sbit=sbit)
    # return render_template('myhome.html', STATE=state
    # gts_ca=gts_ca,sbit=sbit)


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
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    User1 = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(User1)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

# Here it shows the home


@app.route('/')
@app.route('/home')
def home():
    gts_ca = session.query(Bank_Name).all()
    return render_template('myhome.html', gts_ca=gts_ca)

# banksite for admins


@app.route('/BankSite')
def BankSite():
    try:
        if login_session['username']:
            name = login_session['username']
            gts_ca = session.query(Bank_Name).all()
            bit = session.query(Bank_Name).all()
            sbit = session.query(Customer_Details).all()
            return render_template('myhome.html', gts_ca=gts_ca,
                                   bit=bit, sbit=sbit, uname=name)
    except:
        return redirect(url_for('showLogin'))

# It shows the details according to the id


@app.route('/BankSite/<int:sbid>/AllBanks')
def showBanks(sbid):
    gts_ca = session.query(Bank_Name).all()
    bit = session.query(Bank_Name).filter_by(id=sbid).one()
    sbit = session.query(Customer_Details).filter_by(bank_name_id=sbid).all()
    try:
        if login_session['username']:
            return render_template('showBanks.html', gts_ca=gts_ca,
                                   bit=bit, sbit=sbit,
                                   uname=login_session['username'])
    except:
        return render_template('showBanks.html',
                               gts_ca=gts_ca, bit=bit, sbit=sbit)


# Here we can add a new bank


@app.route('/BankSite/addBank_Name', methods=['POST', 'GET'])
def addBank_Name():
    if request.method == 'POST':
        bank_name = Bank_Name(name=request.form['name'],
                              user_id=login_session['user_id'])
        session.add(bank_name)
        session.commit()
        return redirect(url_for('BankSite'))
    else:
        return render_template('addBank_Name.html', gts_ca=gts_ca)

# Here we can edit a particular bank name


@app.route('/BankSite/<int:sbid>/edit', methods=['POST', 'GET'])
def editBank_Name(sbid):
    editBank_Name = session.query(Bank_Name).filter_by(id=sbid).one()
    creator = getUserInfo(editBank_Name.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this bankname."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('BankSite'))
    if request.method == "POST":
        if request.form['name']:
            editBank_Name.name = request.form['name']
        session.add(editBank_Name)
        session.commit()
        flash("bankname Edited Successfully")
        return redirect(url_for('BankSite'))
    else:
        # gts_ca is global variable we can them in entire application
        return render_template('editBank_Name.html',
                               sb=editBank_Name, gts_ca=gts_ca)

# delete particular bank name


@app.route('/BankSite/<int:sbid>/delete', methods=['POST', 'GET'])
def deleteBank_Name(sbid):
    sb = session.query(Bank_Name).filter_by(id=sbid).one()
    creator = getUserInfo(sb.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this bank name."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('BankSite'))
    if request.method == "POST":
        session.delete(sb)
        session.commit()
        flash("bank name Deleted Successfully")
        return redirect(url_for('BankSite'))
    else:
        return render_template('deleteBank_Name.html', sb=sb, gts_ca=gts_ca)

# add a customer details to a particular bank


@app.route('/BankSite/addBank_Name/addCustomer_Details/<string:sbname>/add',
           methods=['GET', 'POST'])
def addCustomer_Details(sbname):
    bit = session.query(Bank_Name).filter_by(name=sbname).one()
    # See if the logged in user is not the owner
    creator = getUserInfo(bit.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new customer"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showBanks', sbid=bit.id))
    if request.method == 'POST':
        cus_name = request.form['cus_name']
        acc_number = request.form['acc_number']
        cus_phone_number = request.form['cus_phone_number']
        acc_type = request.form['acc_type']
        cus_address = request.form['cus_address']
        customerdetails = Customer_Details(cus_name=cus_name,
                                           acc_number=acc_number,
                                           cus_phone_number=cus_phone_number,
                                           acc_type=acc_type,
                                           cus_address=cus_address,
                                           bank_name_id=bit.id,
                                           user_id=login_session['user_id'])
        session.add(customerdetails)
        session.commit()
        return redirect(url_for('showBanks', sbid=bit.id))
    else:
        return render_template('addCustomer_Details.html',
                               sbname=bit.name, gts_ca=gts_ca)

# edit a customer details of a bank


@app.route('/BankSite/<int:sbid>/<string:sbename>/edit',
           methods=['GET', 'POST'])
def editCustomer_Details(sbid, sbename):
    sb = session.query(Bank_Name).filter_by(id=sbid).one()
    customerdetails = session.query(Customer_Details
                                    ).filter_by(cus_name=sbename).one()
    #  See if the logged in user is not the owner
    creator = getUserInfo(sb.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user !=  owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this details"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showBanks', sbid=sb.id))
    # POST methods
    if request.method == 'POST':
        customerdetails.cus_name = request.form['cus_name']
        customerdetails.acc_number = request.form['acc_number']
        customerdetails.cus_phone_number = request.form['cus_phone_number']
        customerdetails.acc_type = request.form['acc_type']
        customerdetails.cus_address = request.form['cus_address']
        session.add(customerdetails)
        session.commit()
        flash("Details Edited Successfully")
        return redirect(url_for('showBanks', sbid=sbid))
    else:
        return render_template('editCustomer_Details.html',
                               sbid=sbid, customerdetails=customerdetails,
                               gts_ca=gts_ca)

# Here we can delete a customer details


@app.route('/BankSite/<int:sbid>/<string:sbename>/delete',
           methods=['GET', 'POST'])
def deleteCustomer_Details(sbid, sbename):
    sb = session.query(Bank_Name).filter_by(id=sbid).one()
    customerdetails = session.query(Customer_Details
                                    ).filter_by(cus_name=sbename).one()
    # See if the logged in user is not the owner
    creator = getUserInfo(sb.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this details"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showBanks', sbid=sb.id))
    if request.method == "POST":
        session.delete(customerdetails)
        session.commit()
        flash("Deleted details Successfully")
        return redirect(url_for('showBanks', sbid=sbid))
    else:
        return render_template('deleteCustomer_Details.html',
                               sbid=sbid, customerdetails=customerdetails,
                               gts_ca=gts_ca)

# USER LOGOUT


@app.route('/logout')
def logout():
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
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type': 'application/x-www-form-urlencoded'
                           })[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = make_response(json.dumps('Successfully disconnected user..'
                                            ), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Json
# It displays the all details that you have


@app.route('/BankSite/JSON')
def allBanksJSON():
    bank_names = session.query(Bank_Name).all()
    category_dict = [c.serialize for c in bank_names]
    for c in range(len(category_dict)):
        customernames = [i.serialize for i in session.query(
            Customer_Details).filter_by(bank_name_id=category_dict[c]["id"]
                                        ).all()]
        if customernames:
            category_dict[c]["banks"] = customernames
    return jsonify(Bank_Name=category_dict)

# Displays the bank name and its id


@app.route('/BankSite/bank_Name/JSON')
def categoriesJSON():
    banks = session.query(Bank_Name).all()
    return jsonify(bank_Name=[c.serialize for c in banks])

# It displays all customer details in banks


@app.route('/BankSite/banks/JSON')
def detailsJSON():
    details = session.query(Customer_Details).all()
    return jsonify(banks=[i.serialize for i in details])

# It displays the details in a bank


@app.route('/BankSite/<path:bankname>/banks/JSON')
def categorydetailsJSON(bankname):
    bankName = session.query(Bank_Name).filter_by(name=bankname).one()
    banks = session.query(Customer_Details).filter_by(bank_name=bankName
                                                      ).all()
    return jsonify(bankName=[i.serialize for i in banks])

# It displays the details that you given


@app.route('/BankSite/<path:bankname>/<path:cusdetails_name>/JSON')
def DetailsJSON(bankname, cusdetails_name):
    bankName = session.query(Bank_Name).filter_by(name=bankname).one()
    customerDetailsName = session.query(Customer_Details).filter_by(
           cus_name=cusdetails_name, bank_name=bankName).one()
    return jsonify(customerDetailsName=[customerDetailsName.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
