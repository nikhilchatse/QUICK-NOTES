from flask import *
import sqlite3

app=Flask(__name__)
app.secret_key="secret123"
# database connection 
def db_connection():
    con=sqlite3.connect("notes.db")
    return con

# tables
def db_tables():
    con=db_connection()
    cur=con.cursor()
    # user table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT ,name varchar(50),email varchar(50) ,contact varchar(50), password varchar(50))"
    )
    cur.execute(
        "CREATE TABLE IF NOT EXISTS content(id INTEGER PRIMARY KEY AUTOINCREMENT, title varchar(50),description varchar(50), user_id INTEGER)"
    )

    con.commit()
    con.close()
db_tables()

@app.route("/")
def home():
    

    return render_template("index.html")

@app.route("/register",methods=['POST','GET'])
def register():
    
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        contact=request.form['contact']
        password=request.form['password']
        
        con=db_connection()
        cur=con.cursor()

        cur.execute("INSERT INTO users (name,email,contact,password) VALUES (?,?,?,?)",(name,email,contact,password))
        con.commit()
        data=cur.fetchall()
        print(data)
        return redirect(url_for("login"))
    
    return render_template("register.html")


@app.route("/login",methods=['POST','GET'])
def login():
    con=db_connection()
    cur=con.cursor()
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        cur.execute("SELECT * FROM users WHERE email=? AND password=?",(email,password))
        user=cur.fetchone()
        print(user)
        con.commit()

        if user:
            session["user_id"]=user[0]
            return redirect(url_for("mynotes"))
        else:
            return "Invalid"

    return render_template("login.html")


@app.route("/mynotes",methods=['GET','POST'])
def mynotes():
    if "user_id" not in session:
        return "<script> alert('PLEASE, LOGIN FIRST!!!');window.location.href=('/login')</script>"
    user_id=session["user_id"]
    
    con=db_connection()
    cur=con.cursor()
    
    if request.method=='POST':
        title=request.form["title"]
        content=request.form["content"]
    
        cur.execute("INSERT INTO content(title,description,user_id)VALUES(?,?,?)",(title,content,user_id,))
        con.commit()
        cur.execute("SELECT * FROM content WHERE user_id=?",(user_id,))
        userContend=cur.fetchall()
        con.commit()
        print(userContend)
        
        return render_template("MyNotes.html",userContend=userContend)
    cur.execute("SELECT * FROM content WHERE user_id=?",(user_id,))
    userContend=cur.fetchall()
    con.commit()
    con.close()
    return render_template("MyNotes.html",userContend=userContend)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# DELETE OPRETIONS

@app.route("/delete/<int:id>")
def delete(id):
    if "user_id" not in session:
        redirect("login")
    user_id=session["user_id"]
    con=db_connection()
    cur=con.cursor()

    cur.execute("DELETE FROM content WHERE id=? AND user_id=?",(id,user_id,))

    con.commit()

    return "<script> alert('Note deleted');window.location.href=('/mynotes')</script>"
    # return redirect(url_for("mynotes"))

#update opretions

@app.route("/update/<int:id>")
def update(id):
    if "user_id " not in session:
        redirect(url_for("login"))
    
    user_id=session["user_id"]
    con=db_connection()
    cur=con.cursor()

    cur.execute("SELECT * FROM content WHERE id=? AND user_id=?",(id,user_id,))
    user=cur.fetchall()
    con.commit()
    return render_template("update.html",user=user)

@app.route("/updatesave")
def updatesave():
    if "user_id" not in session:
        redirect(url_for("login"))
    user_id=session["user_id"]

    con=db_connection()
    cur=con.cursor()

    if request.method=='POST':
        id=request.form['id']
        title=request.form['title']
        content=request.form['content']

        cur.execute("UPDATE content SET title=?,description=? WHERE id=? AND user_id=?",(title,content,id,user_id,))

        con.commit()
        con.close()

        redirect(url_for("mynotes"))
    


if __name__=="__main__":
    app.run(debug=True)