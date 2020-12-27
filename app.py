# Personal link collector and displays shorted Links and also hyperlinks to them
# It stores the links as most visited

from flask import Flask, request, redirect, render_template, url_for
import os
import sqlite3
from sqlite3 import OperationalError

app = Flask(__name__)
m = app.config.from_object('config')

#Connection with the SQLITE database
# con = sqlite3.connect('database.db')
# cur = con.cursor()

def link_table_sqlite():
    table_creation_command = "CREATE TABLE IF NOT EXISTS tabl1(id INT AUTOINCREMENT, link TEXT, link_name TEXT PRIMARY KEY, original_link TEXT)"
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    con.execute("CREATE TABLE IF NOT EXISTS tabl1(id INTEGER PRIMARY KEY AUTOINCREMENT, link TEXT, link_name TEXT, original_link TEXT)")
    con.close()




m = app.config["ADMIN_PWD"]
print(m)

val2 = " "
val = " "
# The below variable is set to 1, if the user has successfully logged in. Then only the user is allowed to move forward to the main index page.
login_flag = 0
val3 = "Click to go back to Index page"



@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_display():
    global login_flag, val, val2
    if request.method == 'GET':
        if login_flag == 1:
            #The below return statement gives the hyperlink to go back to the index page, if you are already logged in
            return (render_template('home_pwd.html', val="You have already logged in, no need to come back to homepage", val2=val2, val3=val3))
        return (render_template('home_pwd.html', val=val))
    elif request.method == 'POST':
        a = request.form
        print(a['pwd_input'])
        if(a['pwd_input'] == m):
            print('y')
            print(m)
            login_flag = 1
            val2 = "/index"
            print(login_flag)

            return redirect(url_for('index_pg'))
        else:
            return redirect(url_for('wrong_try'))
        return "hello"

print(login_flag)


@app.route('/falseuser', methods=['GET'])
def wrong_try():
    global val
    val = "You cannot access the index page without putting the password"
    return redirect(url_for('home_display'))

# The code below redirects the authenticated user to the index page where the shortened links are stored
gg = ['']

@app.route('/index', methods=['GET', 'POST'])
def index_pg():
    if login_flag == 0:
        return redirect(url_for('wrong_try'))
    if request.method == 'POST':

        k = request.form
        print(k['link_name'])
        # link_name, link_text_box
        link_name = k['link_name']
        link_text_box = k['link_text_box']

        # I am traversing the table and displaying the code on the index page using code below
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            print('before search operation')
            cur.execute('''SELECT * FROM tabl1''')
            g = cur.fetchall()
            # gg = g
            print(g)

            # We are ensuring that the name of the website that the user is giving has not been used before
            cur.execute('''SELECT * FROM tabl1 WHERE link_name=?''', (link_name,))
            result = cur.fetchall()
            result1 = not result
            if result1 == 1:
                # This means the result is empty and the procedure to shorten the link and inserting the link will
                # come here
                ##### The code to shorten the link will come here
                shortened_link_main = 'https://link-shortening-and-storing.herokuapp.com/' + link_name
                con.execute('''INSERT INTO tabl1(link, link_name, original_link) VALUES(?,?,?)''', (shortened_link_main, link_name,link_text_box, ))
                con.commit()
                # con.close()
                print('Empty')
                return render_template('main_index.html', g=g)
            else:

                # This means that result is not empty and the user will have to input new name because this name
                # already exists
                return render_template('main_index.html', q = 'The name already exists, use other name',g=g)

            print(result)

    if request.method == 'GET':
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            print('before search operation')
            cur.execute('''SELECT * FROM tabl1''')
            g = cur.fetchall()
            return render_template('main_index.html', g=g)

    print("In logged func ", login_flag)
    return render_template('main_index.html')

@app.route('/<shortened_name>')
def link_forwarder(shortened_name):
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('''SELECT * FROM tabl1 WHERE link_name=?''', (shortened_name,))
        print(shortened_name)
        op = cur.fetchall()
        op1 = not op
        if op1 == 0 and login_flag == 1:
            # This means that op is not empty
            print(op)
            print(type(op[0][3]))
            k = "http://" + op[0][3]

            return redirect(k)
        if op == 1:
            return redirect(url_for('index_pg'))
        if login_flag == 1:
            # k = op[0][3]
            # return redirect(k)
            return "hellp"
        elif login_flag == 0:
            return "You are not logged in"
    return shortened_name

def getAapp():
    return app


if __name__ == '__main__':
    link_table_sqlite()
    app.run()


