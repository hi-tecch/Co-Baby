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


@app.route('/message')
def messaging():
    # if not 'user_id' in session:
    #         return redirect('/')
    message_recieved =message.Message.show_all_messages
    return render_template('show_messages.html',message_recieved=message_recieved)



# # create a new schedulee
# @app.route('/add_message')
# def new_message():
#     # if not 'user_id' in session:
#     #         return redirect('/')
    
  

#     return render_template('create_message.html')


# @app.route('/create',methods=['POST'])
# def create():
#     # if not 'user_id' in session:
#     #     return redirect('/')
        
#     # if not report.Report.validate_create_one(request.form):#boolean and ausutme it is true
#     #     return redirect('/new')

#     id={
#     'id':session['user_id']
#     }
    
        
   
#     data={
    
#     'message' : request.form ['message'],
#     'freinds_id':session['user_id'] ,
    
#     }
   
#     message.Message.create_one_message(data)

#     return redirect('/message')

