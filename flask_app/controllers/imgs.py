from flask_app import app
from flask import Flask,render_template, redirect, session, request, flash, url_for
from flask_app.model.img import Img
from flask_app.model.login import User
import os, urllib.request, pathlib, datetime
from werkzeug.utils import secure_filename
    
UPLOAD_FOLDER = '/Users/Azaly/Desktop/Coding/AlgoProjects/Group/Co-Baby/flask_app/static/gallery'
#  the path will need to be updated!!! it is not relative path

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif'}
EXTENSIONS = {"0":"png","1": "jpg","2": "jpeg","3": "gif"}

@app.route('/test')
def test():
    return f"the path is workign"

@app.route('/gallery') 
def gallery():
    if 'user_id' not in session:
        return render_template('gallery.html',imgs = Img.get_all())
    data ={
        'id': session['user_id']
    }

    return render_template('gallery.html',user=User.get_one_by_id(data),imgs = Img.get_all())

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    # if 'user_id' not in session:
    #     return redirect('/logout')
    data ={ 
        "username": request.form['username'],
        "text": request.form['text'],
        "user_id": session['user_id']
    }
    id = Img.save(data)
    name = id
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            EXTENSION = filename.split('.')
            filename = f'{name}.{EXTENSION[len(EXTENSION)-1]}'
            print(filename)
            data = {
                'id':name,
                'filename':filename
            }
            Img.file_typee(data)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/gallery')
    return redirect('/gallery')

@app.route('/delete/img/<int:img_id>')
def deleteImg(img_id):
    print("we are here in delete def")
    data = {
        'img_id':img_id
    }
    Img.delete(data)
    return redirect('/gallery')