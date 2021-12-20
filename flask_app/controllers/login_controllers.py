from flask_app import app
from flask import Flask, render_template,redirect,request,session
from flask_app.model import login
from flask_app.model import report, kid_model
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)  





@app.route('/')              
def home():
    return render_template('login_form.html')

@app.route('/register', methods=['POST'])  
def register():
    
    if not login.User.validate_registration(request.form):#boolean and ausutme it is true
        return redirect('/')
        #bcrybt the password on the form

    data={
        'First_name':request.form['First_name'],
        'Last_name':request.form['Last_name'],
        'zip_code':request.form['zip_code'],
        'email':request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password']),
        

        
        }
    
    user_id=login.User.register(data)#we are saving nto one_usr object
    print(user_id)
    flash(f"the email address you entered {request.form['email']} is valid address! thank you!", 'email')
    # store user id into session
    session['user_id'] = user_id
    print(session['user_id'])

    return redirect('/create_profile')
    
    
@app.route('/create_profile')              
def create_profile():
    
    return render_template('create_profile.html')  
    
    

@app.route('/profile/create', methods=['POST'])  
def add_kid():


    data={
        'First_name':request.form['First_name'],
        'Last_name':request.form['Last_name'],
        'age':request.form['age'],
        'allergy_to':request.form['allergy_to'],
        'Parent_id':session['user_id']
        

        
        }
    
    the_kid=kid_model.Kid.create_profile(data)#we are saving nto one_usr object
    print(the_kid)
    
    return redirect('/home')
    
    
    

@app.route('/login', methods=['POST'])  
def login_user():
    
    if not login.User.validate_login(request.form):
        return redirect('/')
    
    data={
    'email':request.form['email'],
    }
    the_user=login.User.get_user_by_email(data)
    session['user_id'] = the_user.id
    print(session['user_id'] )
    return redirect('/home')
    
    
    
# @app.route('/dashboard' )  
# def dashboard():
#     if not 'user_id' in session:
#         return redirect('/')
#     data={
#     'id':session['user_id'] 
#     }
    
#     all_reports=report.Report.show_all_wz_reporter()
#     return render_template('report.html',the_user=login.User.get_one_by_id(data),all_reports=all_reports)

    
@app.route('/logout' )  
def logout():
    session.pop('user_id')
    return redirect('/')

