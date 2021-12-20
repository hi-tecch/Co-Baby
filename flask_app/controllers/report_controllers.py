from flask_app import app
from flask import Flask, render_template,redirect,request,session
from flask_app.model import login, report ,kid_model, message
# from flask_app.model import report
# from flask_app.model import kid_model
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
import datetime

bcrypt = Bcrypt(app)



# afterlogin go to home page

@app.route('/home')
def homepage():
    if not 'user_id' in session:
            return redirect('/')
    

    data={
    'id':session['user_id']
    }
    the_user=login.User.get_one_by_id(data)
    print(the_user.id)
    
    session['user_id'] = the_user.id
    print(session['user_id'])
    
    return render_template('home.html',the_user=the_user)

# profile will have personal info

@app.route('/profile/<int:id>')
def profile(id):

    data={
    'id':session['user_id']
    }
    # the_user=login.User.get_one_by_id(data)
    # print(the_user)
    
    the_user=login.User.one_parent_with_kid(data)
    return render_template('profile.html',the_user=the_user)


# edit profile

@app.route('/profile/update/<int:id>',methods=['POST'])
def edit_profile(id):
   
    id={
    'id':session['user_id']
    }
   
    data={
    
    'First_name':request.form['First_name'],
    'Last_name' : request.form['Last_name'],
    'email' : request.form ['email'],
    'address' : request.form['address'],
    'zip_code' : request.form['zip_code'],
    'id':session['user_id'] ,
    
    
    
    }
   
    login.User.update_profile(data)
    return redirect('/home')




# create a new schedulee

@app.route('/add_schedule')
def new():
    # if not 'user_id' in session:
    #         return redirect('/')
    
    return render_template('Add_schedule.html')


@app.route('/create',methods=['POST'])
def create():
    if not 'user_id' in session:
        return redirect('/')
        
    # if not report.Report.validate_create_one(request.form):#boolean and ausutme it is true
    #     return redirect('/new')

    id={
    'id':session['user_id']
    }
    
        
   
    data={
    
    'start_datetime' : request.form ['start_datetime'],
    'end_datetime' : request.form['end_datetime'],
    'comments' : request.form['comments'],
    'Freinds_id':session['user_id'] ,
    
    }
   
    report.Schedule.create_one(data)

    return redirect('/future_schedule')


@app.route('/future_schedule') 
def showall_future_report():
    # future_schedules=report.Schedule.show_schedule_wz_freinds()
    # print(future_schedules)
    not_done=report.Schedule.show_all_not_done()
    print(not_done)
    return render_template ('future_schedule.html',kids_name=kid_model.Kid.show_kids(),not_done=not_done)





@app.route('/update/done',methods=['POST'])
def update_done_schedules():
   
    # id={
    # 'id':request.form['kids_id'],
    # }
   
    data={
    
    'kids_id':request.form['kids_id'],
    'id':request.form['schedule_id'],
    'comment' : request.form['comment'],
    }
   
    report.Schedule.update_one_schedule(data)
    return redirect('/future_schedule')








@app.route('/Past_schedules') 
def showall_past_report():
   
    toddler_name=report.Schedule.show_schedule_wz_toddler()
    print('asgdalkjlksdjfaa---------------')
    print(toddler_name)
    test=report.Schedule.show_schedule_toddler_freinds()
    print('------------------------------------------------')
    print(test)
    return render_template ('Past_schedule.html',toddler_name=toddler_name,test=test)







@app.route('/monthly_report') 
def showmonth():
    return render_template ('Past_schedule.html')





@app.route('/message')
def messaging():
    # if not 'user_id' in session:
    #         return redirect('/')
    message_recieved =message.Message.show_all_messages()
    # return (message_recieved)
    return render_template('show_messages.html',message_recieved=message_recieved)



# create a new schedulee
@app.route('/add_message')
def new_message():
    # if not 'user_id' in session:
    #         return redirect('/')
    
  

    return render_template('show_messages.html')


@app.route('/create_message',methods=['POST'])
def create_message():
    # if not 'user_id' in session:
    #     return redirect('/')
        
    # if not report.Report.validate_create_one(request.form):#boolean and ausutme it is true
    #     return redirect('/new')

    id={
    'id':session['user_id']
    }
    
        
   
    data={
    
    'message' : request.form ['message'],
    'freinds_id':session['user_id'] ,
    
    }
   
    message.Message.create_one_message(data)

    return redirect('/message')





        
 
