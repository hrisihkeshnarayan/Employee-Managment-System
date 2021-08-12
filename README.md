# Employee-Managment-System


Emplyee Managment System using Python, HTML, PostgreSQL, Flask, Flask-SQLAlchemy.

Create Employees and Department table in PostgreSQL by and perform various operations like insert, show_table, update, delete, sort, select using Python, Flask, Flask_SQLAlchemy.

Flask used as an API to connect backend Python code with HTML webpage, Flask-SQLAlchmy module used to connect database and run query with PostgreSQL.

Note:

Before running code on your system install all modules by run this commands in terminal: pip install -r requirements.txt

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/Employee_Management'

In this PostgreSQL connectivity statement use your PostgreSQL username, password and database name otherwise this will give you error.

fill your database connectivity information and use this:

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://"username":"password"@localhost/"database_name"'

If after running code localhost URL not appear in terminal then paste this URl in Browser : http://127.0.0.1:5000/

For better experiance use crome as default browser and Pycharm as IDE.
