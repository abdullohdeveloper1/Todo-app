from flask import Flask, redirect, render_template, url_for, request, Request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12@localhost:5432/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True, nullable=False)
  title = db.Column(db.String())
  author = db.Column(db.String())
  year = db.Column(db.String())

  def __repr__(self):
    return f'<Todo title {self.title} author {self.author} year {self.year}>'

@app.route('/')
def index():
  return render_template('index.html', todos=Todo.query.all())

@app.route('/', methods=['POST'])
def create():
  try:
    todo = Todo(
      title = request.form['title'],
      author = request.form['author'],
      year = request.form['year']
    )
    db.session.add(todo)
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  return redirect(url_for('index'))

@app.route('/todo/<int:todo_id>/delete', methods=['GET', 'DELETE'])
def delete(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))