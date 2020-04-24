from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '98ab54df78yc45zx78'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    post = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'Employee {self.id}'


@app.route('/')
def home():
    employees = Employee.query.order_by(Employee.id).all()
    return render_template('index.html', employees=employees)


@app.route('/newEmployee', methods=['GET', 'POST'])
def newEmployee():
    title = 'Dashboard- New'
    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['Email']
        post = request.form['Post']

        new_employee = Employee(name=name, email=email, post=post)
        flash('Employee added successfully!', 'success')
        try:
            db.session.add(new_employee)
            db.session.commit()
            return redirect(url_for('home'))

        except:
            return 'An error occurred'

    else:
        return render_template('newEmp.html', title=title)


@app.route('/delete/<int:id>')
def delete(id):
    to_delete = Employee.query.get_or_404(id)
    flash('Record deleted!', 'danger')

    try:
        db.session.delete(to_delete)
        db.session.commit()
        return redirect(url_for('home'))

    except:
        return 'An error occurred'


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    title = 'Dashboard- Edit'
    employee = Employee.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form['Name']
        email = request.form['Email']
        post = request.form['Post']
        employee.name = name
        employee.email = email
        employee.post = post
        flash('Details updated successfully!', 'info')

        try:
            db.session.commit()
            return redirect(url_for('home'))

        except:
            return 'An error occurred'

    else:
        return render_template('edit.html', employee=employee, title=title)


if __name__ == '__main__':
    app.run(debug=True)
