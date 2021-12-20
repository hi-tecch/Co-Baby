
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt 
from flask_app import app
from flask_app.model import login, kid_model ,report
bcrypt = Bcrypt(app)   


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Message:
    db_name="co_baby"   
    def __init__( self , data ):
        self.id  = data['id']
        self.message=data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.freinds_id = data['freinds_id']
        self.sender=None

#show all freinds_id

    @classmethod
    def show_all_messages(cls):       
            
        query = "SELECT * FROM messages join freinds where messages.freinds_id=freinds.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        messages=[]
        for i in results:
            message=cls(i)
            sender_data={
            'id'         : i['freinds.id'],
            'First_name':i['First_name'],
            'Last_name':i['Last_name'],
            'email' : i['email'],
            'password' :i['password'],
            'address' : i['address'],
            'zip_code' : i['zip_code'],
            'created_at' : i['freinds.created_at'],
            'updated_at' : i['freinds.updated_at']
            
            }
            message=cls(i)
            message.sender=login.User(sender_data)
            messages.append(message)
            print('-------------messages')
            print(messages)
        return messages
        
        
    @classmethod
    def create_one_message(cls,data):          
        query = "Insert INTO messages (message,freinds_id) VALUES(%(message)s,%(freinds_id)s);"
        return  connectToMySQL(cls.db_name).query_db(query,data)  