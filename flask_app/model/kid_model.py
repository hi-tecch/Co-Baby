from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt 
from flask_app import app
from flask_app.model import report,login
bcrypt = Bcrypt(app)   



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 



class Kid:#from kids table 
    db_name="co_baby"
    
    def __init__( self , data ):
        self.id         = data['id']
        self.First_name=data['First_name']
        self.Last_name=data['Last_name']
        self.age = data['age']
        self.allergy_to = data['allergy_to']
        self.Parent_id = data['Parent_id']
       
       
       
    @classmethod
    def show_kids(cls,):       
            
        query = "SELECT * FROM kids;"
        results = connectToMySQL(cls.db_name).query_db(query)
        kids=[]
        for i in results:
            kids.append(cls(i))
        return kids
        
        
    @classmethod
    def create_profile(cls,data):
        
        query="INSERT INTO  kids(First_name,Last_name,age,allergy_to,Parent_id) VALUES (%(First_name)s ,%(Last_name)s,%(age)s,%(allergy_to)s,%(Parent_id)s)";
        return connectToMySQL(cls.db_name).query_db(query,data)