from sqlite3.dbapi2 import Cursor
from werkzeug.utils import redirect, secure_filename
from flask import Flask,request,render_template,session,flash,redirect,url_for
import sqlite3 
from flask import send_from_directory
import os 
app=Flask(__name__)
app.config["SECRET_KEY"]="12345"

UPLOAD_FOLDER = 'C:\Imageupload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.add_url_rule(
    "/uploads/<name>", endpoint="download_file", build_only=True
)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route("/")
def index():
    

    return render_template("home.html")

@app.route('/lend', methods=['GET', 'POST'])
def lend():
    if request.method=="GET":
       return render_template("lend.html")
    bookname=request.form.get("book")
    session["bookname"]=bookname
    adress=request.form.get("adress")
    session["adress"]=adress
    email=request.form.get("email")
    session["email"]=email
    tel=request.form.get("tel")
    session["tel"]=tel
    flash("Bookdata submitted sucessfully","success")
    conn=sqlite3.connect("walldorf.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO user(email,adress,tel) VALUES(?,?,?);",(email,adress,tel))
    print("Values Inserted")
    conn=sqlite3.connect("walldorf.db")
    cur=conn.cursor()
    cur.execute("SELECT * FROM user;")
    records=cur.fetchall()
    print(records)
    conn.commit()
    conn.close()
    return render_template("home.html",records=records)


@app.route('/receiver',methods=['GET','POST'])
def receiver():
    if request.method=="GET":
       return render_template("receiver.html")
    adress=request.form.get("adress")
    session["adress"]=adress
    email=request.form.get("email")
    session["email"]=email
    tel=request.form.get("tel")
    session["tel"]=tel
    conn=sqlite3.connect("walldorf.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO receiver(email,adress,tel) VALUES(?,?,?);",(email,adress,tel))
    print("Values Inserted")
    return render_template("home.html",message="Your Data has been saved sucessfully into our Database")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method=="GET":
       return render_template("registration.html")
    adress=request.form.get("adress")
    message=""
    session["adress"]=adress
    email=request.form.get("email")
    session["email"]=email
    tel=request.form.get("tel")
    session["tel"]=tel
    password=request.form.get("password")
    session["password"]=password
    confirm_password=request.form.get("confirm_password")
    session["confirm_password"]=confirm_password
    if password!=confirm_password:
        message=("Password does not match")
        return render_template("registration.html",message=message)
        
    conn=sqlite3.connect("walldorf.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO user(email,adress,tel,password) VALUES(?,?,?);",(email,adress,tel,password))
    print("Values Inserted")
    return render_template("login.html",message="Registration sucessfulla")
    


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")
    



























































if __name__=="__main__":
    app.run(debug=True)






















