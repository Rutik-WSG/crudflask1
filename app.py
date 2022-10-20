from flask import Flask,render_template,request,redirect
import pymysql
 
app=Flask(__name__)


def connection():
    s="127.0.0.1"
    d="crud"
    u="root"
    p=""
    conn=pymysql.connect(host=s, user=u, password=p, database=d)
    return conn
    
@app.route("/")
def main():
    cars = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student")
    for row in cursor.fetchall():
        cars.append({"id": row[0], "name": row[1], "lname": row[2], "number": row[3]})
    conn.close()
    return render_template("home.html", cars = cars )

@app.route("/add", methods = ['GET','POST'])
def add():
    if request.method == 'GET':
        return render_template("addstd.html",car = {})
    if request.method == 'POST':
        id = int(request.form["id"])
        name = request.form["name"]
        lname = str(request.form["lname"])
        number = int(request.form["number"])
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO student (id, name, lname, number) VALUES (%s, %s, %s, %s)", (id, name, lname, number))
        conn.commit()
        conn.close()
        return redirect('/')


@app.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
    cr = []
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM student WHERE id = %s", (id))
        for row in cursor.fetchall():
            cr.append({"id": row[0], "name": row[1], "lname": row[2], "number": row[3]})
        conn.close()
        return render_template("update.html", car = cr[0])
    if request.method == 'POST':
        name = str(request.form["name"])
        lname = str(request.form["lname"])
        number = int(request.form["number"])
        cursor.execute("UPDATE student SET name = %s, lname = %s, number = %s WHERE id = %s", (name, lname, number, id))
        conn.commit()
        conn.close()
        return redirect('/')
    
@app.route('/delete/<int:id>')
def delete(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student WHERE id = %s", (id))
    conn.commit()
    conn.close()
    return redirect('/')


if (__name__=="__main__"):
    app.debug=True
    app.run()