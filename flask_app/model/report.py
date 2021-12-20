
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt 
from flask_app import app
from flask_app.model import login, kid_model
bcrypt = Bcrypt(app)   



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class Schedule:
    db_name="co_baby"
    
    def __init__( self , data ):
        
        self.id   = data['id']
        self.month=data['month']
        self.year=data['year']
        self.start_datetime = data['start_datetime']
        self.end_datetime = data['end_datetime']
        self.comments = data['comments']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.kids_id = data['kids_id']
        self.Freinds_id=  data['Freinds_id'] 
        self.schedule=[]
        self.freinds=[]
        self.kids=[]
        self.freinds_schedule=[]
        self.sitter=None

#show all 

    @classmethod
    def show_all(cls):       
            
        query = "SELECT * FROM schedule;"
        results = connectToMySQL(cls.db_name).query_db(query)
        schedule=[]
        for i in results:
            schedule.append(cls(i))
        return schedule
        
        

    @classmethod
    def create_one(cls,data):          
        query = "Insert INTO schedule (start_datetime,end_datetime,comments,Freinds_id) VALUES(%(start_datetime)s,%(end_datetime)s,%(comments)s,%(Freinds_id)s);"
        return  connectToMySQL(cls.db_name).query_db(query,data)  
        
 
    @classmethod
    def show_all_not_done(cls):     
        query = "select * from  schedule JOIN freinds on schedule.freinds_id=freinds.id WHERE schedule.comment <>'done' or ISNULL(comment);"
        results = connectToMySQL(cls.db_name).query_db(query)
        freinds_schedule=[]
        print(results)
        for i in results:
            
                freind_data={
                'id'         :i['id'],
                'First_name':i['First_name'],
                'Last_name':i['Last_name'],
                'email' :i['email'],
                'password' :i['password'],
                'address':i['address'],
                'zip_code':i['zip_code'],
                'created_at' :i['created_at'],
                'updated_at' :i['updated_at']

            
                }
                freinds=login.User(freind_data)
                new_schedule=cls(i)
                new_schedule.freinds=freinds
                print(new_schedule.freinds)
                print('fdshdfhdfhhdsh')
                freinds_schedule.append(new_schedule)
                print('freindsschedul---------')
                print(freinds_schedule)
                
                print('freindsschedul---------')
        return freinds_schedule   


            
            
    @classmethod
    def show_schedule_wz_toddler(cls):       
            
        query = "select * from schedule join freinds freinds1 on schedule.Freinds_id=freinds1.id join kids on schedule.Kids_id=kids.id join freinds  freinds2 on kids.Parent_id=freinds2.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)  
        schedule_wz_kids=[]
        print(results)    
        
        for i in results:
            kids_data={
                'id'         :i['kids.id'],
                'First_name':i['kids.First_name'],
                'Last_name':i['kids.Last_name'],
                'age' :i['age'],
                'allergy_to' :i['allergy_to'],
                'Parent_id' :i['Parent_id'],
            }
            kids=kid_model.Kid(kids_data)
            a_schedule=cls(i)
            a_schedule.kids=kids
            schedule_wz_kids.append(a_schedule)
            
        return schedule_wz_kids  
        
        
        
  
            
        
              
   
    @classmethod
    def show_schedule_toddler_freinds(cls):       
            
        query = " SELECT * fROM schedule JOIN freinds as sitter on schedule.Freinds_id=sitter.id JOIN kids on schedule.Kids_id=kids.id ;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)  
        all=[]
        print(all)    
     
        for i in results:
            
            sitter_data={
                    'id'         :i['id'],
                    'First_name':i['First_name'],
                    'Last_name':i['Last_name'],
                    'email' :i['email'],
                    'password' :i['password'],
                    'address':i['address'],
                    'zip_code':i['zip_code'],
                    'created_at' :i['created_at'],
                    'updated_at' :i['updated_at'],
                    'kidos':[]
                    }
                
            sitters=login.User(sitter_data)
            schedule_of_sitter=cls(i)
          
            schedule_of_sitter.sitter=sitters
            all.append(schedule_of_sitter)
            print('--------list  of alllllllllllllllllwzkiddds')
            print(all)
            if len(all)>0 :
                
                
                    kids_schedule=cls(i)
                    kids_data={
                        'id'         :i['kids.id'],
                        'First_name':i['kids.First_name'],
                        'Last_name':i['kids.Last_name'],
                        'age' :i['age'],
                        'allergy_to' :i['allergy_to'],
                        'Parent_id' :i['Parent_id'],
                    }
                    kids_schedule.kids=kid_model.Kid(kids_data)
                    all.append(kids_schedule)
                    # sitters.kidos.append(kids_schedule)
                    print('--------list  of alllllllllllllllllwzkiddds')
                    print(all)
                
        return  all              
         
        
        
        
        
        
        # update schedule by inserting kids id and comment done if the baby sitting is already done 
        
    @classmethod
    def update_one_schedule(cls,data):     
            
        query = "Update schedule SET kids_id= %(kids_id)s,comment=%(comment)s where id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
        

        
        
    @classmethod
    def update_one(cls,data):     
            
        query = "Update report SET location= %(location)s,incident=%(incident)s,date_of_siting=%(date_of_siting)s,num_sasquatches=%(num_sasquatches)s  where id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
        
        
        
    @classmethod
    def delete_one(cls,data):  
            
        query = "delete from report where id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
        

##############validation for create one ###############

    @staticmethod  
    def validate_create_one(form_data):
        is_valid = True

        if len(form_data['location'])<1:
            flash("Location should be filled out",'create_one')
            is_valid=False
            
        if len(form_data['incident'])<1:
            flash("Incident  should be filled out",'create_one')
            is_valid=False
        if form_data['date_of_siting']=='':
            flash("Date should be submitted",'create_one')
            is_valid=False
    
        
        if form_data['num_sasquatches']=='':
            flash("the num of sasquatches should be entered ",'create_one')
            is_valid=False

        return is_valid
   ##############validation for edit one ###############
     
    @staticmethod  
    def validate_edit_one(form_data):
        is_valid = True

        if len(form_data['location'])<1:
            flash("Location should be filled out",'edit_one')
            is_valid=False
            
        if len(form_data['incident'])<1:
            flash("Incident  should be filled out",'edit_one')
            is_valid=False
        if form_data['date_of_siting']=='':
            flash("Date should be submitted",'edit_one')
            is_valid=False
    
        
        if form_data['num_sasquatches']=='':
            flash("the num of sasquatches should be entered ",'edit_one')
            is_valid=False

        return is_valid