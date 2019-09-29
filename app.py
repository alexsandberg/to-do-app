from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

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
    # gets input from form with name='description'
    description = request.form.get('description', '')

    # create new Todo with form data
    todo = Todo(description=description)

    # add new todo object to session and commit
    # this adds new entry to database
    db.session.add(todo)
    db.session.commit()

    # redirects to index method, which reloads page
    return redirect(url_for('index'))


@app.route('/')
def index():
    # tells the view to render with index.html using latest model
    return render_template('index.html', data=Todo.query.all())
