from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import requests
import logging as lg

app = Flask(__name__)
#lg.basicConfig(filename='Employee_Management.log', level=lg.INFO,  format='%(asctime)s %(message)s', filemode='w')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/Employee_Management'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)



class Department(db.Model):
    __table_args__ = (db.UniqueConstraint('dep_id', 'dep_name', name='unique_component_commit'),)
    dep_id = db.Column(db.Integer, primary_key=True)
    dep_name = db.Column(db.String(50), nullable=False, unique=True)
    emp = db.relationship('Employee', backref='employee')

    def __init__(self, dep_name):
        self.dep_name = dep_name
        #self.dep_id = dep_id


class Employee(db.Model):
    emp_id = db.Column(db.Integer, unique=True, primary_key=True)
    emp_name = db.Column(db.String(50), nullable=False)
    emp_age = db.Column(db.Integer)
    dep_id = db.Column(db.Integer, db.ForeignKey('department.dep_id'))

    def __init__(self, emp_name, emp_age, dep_id):
        #self.emp_id = emp_id
        self.emp_name = emp_name
        self.emp_age = emp_age
        self.dep_id = dep_id


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/add_department", methods=['POST'])
def add_department():
    if request.method == 'POST':
        try:
            if not request.form['dep_name']:
                return '<h2 style = "text-align: center" >Please Enter Department Name.</h2>'
                # return 'Please enter Department Name.'
            else:
                dep_name = request.form['dep_name']
                #dep_id = request.form['dep_id']
                dep = Department(dep_name)
                db.session.add(dep)
                db.session.commit()
                flash("Department is added in table.")
                return redirect(url_for('index'))
        except Exception as e:
            return '<h2 style = "text-align: center" >This Department Is Already Present In Table Add New Department.</h2>'


@app.route("/add_employee", methods=['POST'])
def add_employee():
    if request.method == 'POST':
        try:
            if not request.form['emp_name'] or not request.form['emp_dep_id']:
                return '<h2 style = "text-align: center" >Please enter all details.</h2>'
            else:
                #emp_id = request.form['emp_id']
                emp_name = request.form['emp_name']
                emp_age = request.form['emp_age']
                emp_dep_id = request.form['emp_dep_id']
                emp = Employee(emp_name, emp_age, emp_dep_id)
                db.session.add(emp)
                db.session.commit()
                flash("Employee is added in table.")
                return redirect(url_for('index'))
        except Exception as e:
            return '<h2 style = "text-align: center" >Entered Employee Id or Employee Name Is Already Present.</h2>'


@app.route("/emp_table")
def emp_table():
    emp_data = Employee.query.all()
    return render_template('index.html', emp_data=emp_data)


@app.route("/dep_table")
def dep_table():
    dep_data = Department.query.all()
    return render_template('index.html', dep_data=dep_data)


@app.route("/sort_emp_table")
def sort_emp_table():
    sort_emp_data = Employee.query.order_by(Employee.emp_id).all()
    return render_template('index.html', sort_emp_data=sort_emp_data)


@app.route("/change_department", methods=['POST'])
def change_department():
    if request.method == 'POST':
        try:
            if not request.form['old_emp_id'] or not request.form['new_dep_id']:
                return '<h2 style = "text-align: center" >Please enter all details.</h2>'
            else:
                old_emp_id = request.form['old_emp_id']
                new_dep_id = request.form['new_dep_id']
                emp = Employee.query.filter_by(emp_id=old_emp_id).first()
                emp.dep_id = new_dep_id
                db.session.commit()
                flash("Employee's Department is updated in table.")
                return render_template('emptable.html', emp_data=emp)
        except Exception as e:
            return str(e)
            #return '<h2 style = "text-align: center" >Entered Employee Id or Department Id Is Not Present In Database.</h2>'


@app.route("/delete_employee", methods=['POST'])
def delete_employee():
    if request.method == 'POST':
        try:
            if not request.form['del_emp_id']:
                return '<h2 style = "text-align: center" >Please enter Employee Id To Delete From Table.</h2>'
                # return 'Please enter all details.'
            else:
                del_emp_id = request.form['del_emp_id']
                del_emp = Employee.query.filter_by(emp_id=del_emp_id).first()
                db.session.delete(del_emp)
                db.session.commit()
                flash("Employee Deleted From Table.")
                return redirect(url_for('index'))
        except Exception as e:
            return '<h2 style = "text-align: center" >Entered Employee Id or Department Id Is Not Present In Database.</h2>'


# tried But not Working
"""
@app.route("/search_employee", methods=['POST'])
def search_employee():
    if request.method == 'POST':
        try:
            if not request.form['ser_emp_id']:
                return '<h2 style = "text-align: center" >Please enter Employee Id To Search From Table.</h2>'
                # return 'Please enter all details.'
            else:
                ser_emp_id = request.form['ser_emp_id']
                ser_emp = Employee.query.filter_by(emp_id=ser_emp_id).first()
                flash("Employee Deleted From Table.")
                #emp_data = Employee.query.all()
                return render_template('emptable.html', emp_data=ser_emp)
                #return redirect(url_for('index'))
        except Exception as e:
            return str(e)
            #return '<h2 style = "text-align: center" >Entered Employee Id or Department Id Is Not Present In Database.</h2>'
"""


if __name__ == "__main__":
    db.create_all()
    lg.info("All Tables Are Created")
    app.run(debug=True)
