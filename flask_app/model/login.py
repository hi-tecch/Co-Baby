from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt 
from flask_app import app
from flask_app.model import report
from flask_app.model import kid_model
bcrypt = Bcrypt(app)   



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    db_name="co_baby"
    
    def __init__( self , data ):
        self.id         = data['id']
        self.First_name=data['First_name']
        self.Last_name=data['Last_name']
        self.email = data['email']
        self.password = data['password']
        self.address = data['address']
        self.zip_code = data['zip_code']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.kids=[]
        
        


    @classmethod
    def register(cls,data):
        
        query="INSERT INTO  freinds(First_name,Last_name,email,password,zip_code) VALUES (%(First_name)s ,%(Last_name)s,%(email)s,%(password)s,%(zip_code)s)";
        return connectToMySQL(cls.db_name).query_db(query,data)# return the id of the insert object
        
        
        
        
        
       

    @classmethod
    def get_one_by_id(cls,data):
        query = "SELECT * FROM freinds WHERE id=%(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if not results:
            return False
        else:
            return cls(results[0])
            
            
    @classmethod
    def get_user_by_email(cls,data):       
            
        query = "SELECT * FROM freinds WHERE email=%(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if not results:
            return False
        else:
            return cls(results[0])
            
            
            
            
            
            
    @classmethod
    def one_parent_with_kid(cls,data):
        query = "SELECT * FROM freinds JOIN kids on kids.parent_id=freinds.id WHERE freinds.id=%(id)s ;"
        results = connectToMySQL(cls.db_name).query_db(query,data)  
        print(results)
        freinds_kids=cls(results[0])
        print(freinds_kids)
        
        for a_row in results:
            
            kid_data={
                'id'       : a_row['kids.id'],
                'First_name':a_row['kids.First_name'],
                'Last_name':a_row['kids.Last_name'],
                'age' : a_row['age'],
                'allergy_to' : a_row['allergy_to'],
                'Parent_id' : a_row['Parent_id']
        }  
            kids=kid_model.Kid(kid_data)
            print(kids)
            print('----line')
            freinds_kids.kids.append(kid_model.Kid(kid_data))
            print(freinds_kids)
           
        return  freinds_kids
        
        
    @classmethod
    def update_profile(cls,data):     
            
        query = "Update freinds SET First_name=%(First_name)s, Last_name=%(Last_name)s, email=%(email)s, address= %(address)s,zip_code=%(zip_code)s where id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
        
        
        
 
  
            
            
            
            
            
            
            

#####################################   VALIDATION ############################################
    @staticmethod# static method  does not take  the class or the self 
    def validate_registration(form_data):
        is_valid = True
      #First Name - letters only, at least 2 characters and that it was submitted
        if  not form_data['First_name'].isalpha():
            flash("the name should be all characters and atleast 2 and more ",'Register')
            is_valid=False
        elif len(form_data['First_name'])<2:
            flash("the name should be all characters and atleast 2 and more ",'Register')
            is_valid=False
    #Last Name - letters only, at least 2 characters and that it was submitted
        if not form_data['Last_name'].isalpha():
            if len(form_data['Last_name'])<2:
                flash("the last name should be all characters and atleast 2 and more ",'Register')
            is_valid=False
#Email - valid Email format, does not already exist in the database, and that it was submitted
        query = "SELECT * FROM freinds WHERE email=%(email)s;"
        results = connectToMySQL(User.db_name).query_db(query,form_data)
        if len(results)>=1:
            flash("thie email has been taken",'Register')
            is_valid=False
            
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!",'Register')
            is_valid = False
        
        #validate the email is uinque    

#Password - at least 8 characters, and that it was submitted
        if len(form_data['password'])<8:
            flash("the Password should be atleast 8 characters! ",'Register')
            is_valid=False
       
          
#Password Confirmation - matches password: this would nb in login not nessasary in registration??
        if not form_data['password']==form_data['confirm_password']:
            flash("the Password must match! ",'Register')
            is_valid=False
            
            
        return is_valid
        
        
        
        #####logiin###############################
    @staticmethod  
    def validate_login(form_data):
        is_valid = True
        
# check the email provided matches the user in the database
        email_data={
        'email':form_data['email']
        }
        
        the_user=User.get_user_by_email(email_data)
        print(the_user)
        if not the_user:
            flash("invalid email/password!",'login')
            is_valid=False
    #password_check   
        elif not bcrypt.check_password_hash(the_user.password, form_data['password']):
            flash("invalid email/password!",'login')
            is_valid=False
        return is_valid
     