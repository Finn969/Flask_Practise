from flask import Flask, render_template, request
from flask_mysqldb import MySQL


import os

app = Flask(__name__)
app.config["MYSQL_HOST"] = os.environ['MYSQLHOST']
app.config["MYSQL_USER"] = os.environ['MYSQLUSE']
app.config["MYSQL_PASSWORD"] = os.environ['MYSQLPASS']
app.config["MYSQL_DB"] = os.environ['MYSQLDB']
mysql= MySQL(app)



@app.route('/', methods=['GET','POST'])
def home():
    cur = mysql.connection.cursor()
   # cur.execute('DROP TABLE IF EXISTS placeholder')
    cur.execute('CREATE TABLE IF NOT EXISTS placeholder (id INT(3) NOT NULL AUTO_INCREMENT, name VARCHAR(20) DEFAULT \'UNKNOWN\', number INT(5) DEFAULT 50,colour VARCHAR(20) DEFAULT \'red\', PRIMARY KEY(id))')
    if request.method == "POST":
        details = request.form
        name = details['name']
        number = details['number']
        colour = details['colour']
        

        cur.execute("INSERT INTO placeholder(name, number, colour) VALUES (%s, %s, %s)", (name, number, colour))
        mysql.connection.commit()
        
        
    
    cur.execute('SELECT * FROM placeholder')
    rows = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    if len(rows) ==0:
        return 'ERROR: no information'
    info = []
    for row in rows:
        info.append(row)
    print(info)
    return render_template('home.html', info = info)

if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)