from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://alex@localhost:5432/todoapp'
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


db.create_all()

# POST request listener from form element
@app.route('/todos/create', methods=['POST'])
def create_todo():
    # define error flag
    error = False

    body = {}

    # use try-except-finally to handle possible commit failure
    try:
        # gets value of key='description' from returning json
        description = request.get_json()['description']

        # create new Todo with form data
        todo = Todo(description=description)

        # add new todo object to session and commit
        # this adds new entry to database
        db.session.add(todo)
        db.session.commit()

        # define body with description before session closes
        body['description'] = todo.description
    except:
        # set error to T if error
        error = True

        # roll back session if commit fails
        db.session.rollback()

        # print error information
        print(sys.exc_info())
    finally:
        # always close the session
        db.session.close()
    if error:
        # abort request using code for Internal Server Error
        abort(400)
    else:
        # return json using new description information
        return jsonify(body)


@app.route('/')
def index():
    # tells the view to render with index.html using latest model
    return render_template('index.html', data=Todo.query.all())
