from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'

@app.route('/')
def index():
    # RAW Query (aman karena hanya SELECT, tapi tetap bisa diperbaiki)
    students = db.session.execute(text('SELECT * FROM student')).fetchall()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']

    # SIMPLE VALIDATION (optional)
    if not age.isdigit():
        return "Invalid age value", 400

    # FIXED: gunakan SQLAlchemy parameterized query
    db.session.execute(
        text("INSERT INTO student (name, age, grade) VALUES (:name, :age, :grade)"),  # FIXED
        {"name": name, "age": int(age), "grade": grade}  # FIXED
    )
    db.session.commit()  # FIXED

    return redirect(url_for('index'))


@app.route('/delete/<string:id>') 
def delete_student(id):

    # VALIDATION: id harus angka
    if not id.isdigit():
        return "Invalid ID", 400

    # FIXED: hapus f-string, ganti parameterized query
    db.session.execute(
        text("DELETE FROM student WHERE id = :id"),  # FIXED
        {"id": int(id)}  # FIXED
    )
    db.session.commit()  # FIXED

    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']

        if not age.isdigit():
            return "Invalid age", 400

        # FIXED: gunakan parameterized query
        db.session.execute(
            text("UPDATE student SET name = :name, age = :age, grade = :grade WHERE id = :id"),  # FIXED
            {"name": name, "age": int(age), "grade": grade, "id": id}  # FIXED
        )
        db.session.commit()  # FIXED

        return redirect(url_for('index'))

    else:
        # FIXED: SELECT juga dibuat parameterized
        student = db.session.execute(
            text("SELECT * FROM student WHERE id = :id"),  # FIXED
            {"id": id}  # FIXED
        ).fetchone()

        return render_template('edit.html', student=student)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
