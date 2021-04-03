from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# default path
@app.route('/')
def index():
    return 'Hello!'

# GET for all users in list
@app.route('/users')
def get_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {'name': user.name, 'email': user.email, 'password': user.password, 'id': user.userID}
        output.append(user_data)
    return {'users':output}

# GET for specfied user
@app.route('/users/<id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return {'name': user.name, 'email': user.email, 'password': user.password}

# POST for creating new user
@app.route('/users', methods=['POST'])
def create_user():
    user = User(name = request.json['name'], email = request.json['email'], password = request.json['password'])
    db.session.add(user)
    db.session.commit()
    return {'id':user.userID}

# DELETE for specfied user
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    if user is None:
        return {'success': 'false'}
    db.session.delete(user)
    db.session.commit()
    return {'success': 'true'}

# User class for database
class User(db.Model):
    userID =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    # return string representation mainly for printing purposes
    def __repr__(self):
        return f"Name: {self.name} Email: {self.email} Password: {self.password}"

if __name__ == "__main__":
    app.run()