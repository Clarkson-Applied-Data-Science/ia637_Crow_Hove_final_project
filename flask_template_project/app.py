from flask import Flask
from flask import render_template
from flask import request,session, redirect,send_from_directory,make_response 
from flask_session import Session
from datetime import timedelta, datetime
from user import user
import time
from rooms import room
from reservations import reservation

#create Flask app instance
app = Flask(__name__,static_url_path='')

#Configure serverside sessions 
app.config['SECRET_KEY'] = '56hdtryhRTg'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)

#Basic root route - show the word 'homepage'
@app.route('/')  #route name
def home(): #view function
    #return 'homepage'
    return render_template('homepage.html')   


@app.context_processor
def inject_user():
    return dict(me=session.get('user'))

'''
- DDL (init) script
- MyISAM engine
- no referential integrity in create statement

TODO:
-show login form
-check login on submit
    -set session if login ok
-redirect to menu
-check session on login required pages
'''
@app.route('/login',methods = ['GET','POST'])
def login():
    if request.form.get('name') is not None and request.form.get('password') is not None:
        u = user()
        if u.tryLogin(request.form.get('name'),request.form.get('password')):
            print("Login ok")
            session['user'] = u.data[0]
            session['active'] = time.time()
            return redirect('main')
        else:
            print("Login Failed")
            return render_template('login.html', title='Login', msg='Incorrect username or password.')
    else:   
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your email and password to continue.'
        else:
            m = session['msg']
            session['msg'] = None
        return render_template('login.html', title='Login', msg=m)    
    
@app.route('/logout',methods = ['GET','POST'])
def logout():
    if session.get('user') is not None:
        del session['user']
        del session['active']
    return render_template('login.html', title='Login', msg='You have logged out.')

@app.route('/main')
def main():
    if checkSession() == False: 
        return redirect('/login')
    if session['user']['role'] == 'admin':
        return render_template('main.html', title='Main menu') 
    else:
        return render_template('customer_main.html', title='Main menu') 

@app.route('/users/manage',methods=['GET','POST'])
def manage_user():
    if checkSession() == False or session['user']['role'] != 'admin': 
        return redirect('/login')
    o = user()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action == 'delete': #action=delete&pkval=123
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.")
    if action is not None and action == 'insert':
        d = {}
        d['name'] = request.form.get('name')
        d['role'] = request.form.get('role')
        d['password'] = request.form.get('password')
        d['password2'] = request.form.get('password2')
        d['phone'] = request.form.get('phone')
        d['email'] = request.form.get('email')
        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html',msg= "User added.")
        else:
            return render_template('users/add.html',obj = o)
    if action is not None and action == 'update':
        o.getById(pkval)
        o.data[0]['name'] = request.form.get('name')
        o.data[0]['role'] = request.form.get('role')
        o.data[0]['password'] = request.form.get('password')
        o.data[0]['password2'] = request.form.get('password2')
        o.data[0]['phone'] = request.form.get('phone')
        o.data[0]['email'] = request.form.get('email')
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "User updated. <")
        else:
            return render_template('users/manage.html',obj = o)
        
    if pkval is None: #list all items
        o.getAll()
        return render_template('users/list.html',objs = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('users/add.html',obj = o)
    else:
        print(pkval)
        o.getById(pkval)
        return render_template('users/manage.html',obj = o)

@app.route('/users/signup',methods=['GET','POST'])
def signup_user():
    o = user()
    if request.method == 'POST':
        d = {}
        d['name'] = request.form.get('name')
        d['role'] = request.form.get('role')
        d['password'] = request.form.get('password')
        d['password2'] = request.form.get('password2')
        d['phone'] = request.form.get('phone')
        d['email'] = request.form.get('email')
        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html',msg= "User Created.")
        else:
            return render_template('users/signup.html',obj = o)
    o.createBlank()
    return render_template('users/signup.html',obj = o)

@app.route('/rooms/manage',methods=['GET','POST'])
def manage_rooms():
    if checkSession() == False or session['user']['role'] != 'admin': 
        return redirect('/login')
    o = room()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    if action is not None and action == 'delete': #action=delete&pkval=123
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.")
    if action is not None and action == 'insert':
        d = {}
        d['room_num'] = request.form.get('room_num')
        d['price'] = request.form.get('price')
        d['status'] = request.form.get('status')
        d['room_type'] = request.form.get('room_type')
        d['description'] = request.form.get('description')
        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html',msg= "Room added.")
        else:
            return render_template('rooms/add.html',obj = o)
    if action is not None and action == 'update':
        o.getById(pkval)
        o.data[0]['room_num'] = request.form.get('room_num')
        o.data[0]['price'] = request.form.get('price')
        o.data[0]['status'] = request.form.get('status')
        o.data[0]['room_type'] = request.form.get('room_type')
        o.data[0]['description'] = request.form.get('description')
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "Room updated. <")
        else:
            return render_template('rooms/manage.html',obj = o)
        
    if pkval is None: #list all items
        o.getAll()
        return render_template('rooms/list.html',objs = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('rooms/add.html',obj = o)
    else:
        print(pkval)
        o.getById(pkval)
        return render_template('rooms/manage.html',obj = o)
    

@app.route('/reservations/manage',methods=['GET','POST'])
def manage_reserve():
    if checkSession() == False or session['user']['role'] != 'admin': 
        return redirect('/login')
    o = reservation()
    action = request.args.get('action')
    pkval = request.args.get('pkval')
    u = user()
    u.getAll()
    o.guests = u
    r = room()
    r.getAll()
    o.rooms= r
    if action is not None and action == 'delete': #action=delete&pkval=123
        o.deleteById(request.args.get('pkval'))
        return render_template('ok_dialog.html',msg= "Deleted.")
    if action is not None and action == 'insert':
        d = {}
        d['uid'] = request.form.get('uid')
        d['room_id'] = request.form.get('room_id')
        d['check_in_date'] = request.form.get('check_in_date')
        d['check_out_date'] = request.form.get('check_out_date')
        d['payment_method'] = request.form.get('payment_method')
        d['payment_date'] = request.form.get('payment_date')
        d['amount'] = request.form.get('amount')
        o.set(d)
        if o.verify_new():
            o.insert()
            return render_template('ok_dialog.html',msg= "Reservation added.")
        else:
            return render_template('reservations/add.html',obj = o)
    if action is not None and action == 'update':
        o.getById(pkval)
        d['uid'] = request.form.get('uid')
        d['room_id'] = request.form.get('room_id')
        o.data[0]['check_in_date'] = request.form.get('check_in_date')
        o.data[0]['check_out_date'] = request.form.get('check_out_date')
        o.data[0]['payment_method'] = request.form.get('payment_method')
        o.data[0]['payment_date'] = request.form.get('payment_date')
        o.data[0]['amount'] = request.form.get('amount')
        if o.verify_update():
            o.update()
            return render_template('ok_dialog.html',msg= "Reservation updated. <")
        else:
            return render_template('reservations/manage.html',obj = o)
        
    if pkval is None: #list all items
        o.getAll()
        return render_template('reservations/list.html',objs = o)
    if pkval == 'new':
        o.createBlank()
        return render_template('reservations/add.html',obj = o)
    else:
        print(pkval)
        o.getById(pkval)
        return render_template('reservations/manage.html',obj = o)

@app.template_filter('format_date')
def format_date(value, format='%Y-%m-%d'):
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return value  # Return the original string if parsing fails
    return value.strftime(format) if isinstance(value, datetime) else value
app.jinja_env.filters['format_date'] = format_date
   


# endpoint route for static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

#standalone function to be called when we need to check if a user is logged in.
def checkSession():
    if 'active' in session.keys():
        timeSinceAct = time.time() - session['active']
        print(timeSinceAct)
        if timeSinceAct > 500:
            session['msg'] = 'Your session has timed out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False      
  
if __name__ == '__main__':
   app.run(host='127.0.0.1',debug=True)   