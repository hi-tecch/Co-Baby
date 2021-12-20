from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Img:
    db = "co_baby"
    def __init__(self,data):
        self.id = data['id']
        self.filename = data['filename']
        self.username = data['username']
        self.user_id = data['user_id']
        self.text = data['text']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    @classmethod
    def save(cls,data):
        query = "INSERT INTO gallery (username,text,user_id) VALUES(%(username)s,%(text)s,%(user_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)
    @classmethod
    def file_typee(cls,data):
        query = "UPDATE gallery SET filename = %(filename)s where id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM gallery WHERE id = %(img_id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM gallery;"
        results = connectToMySQL(cls.db).query_db(query)
        imgs = []
        for row in results:
            imgs.append( cls(row))
        if len(imgs) < 1:
            print('img less < 1')
            return False
        return imgs
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM gallery WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])