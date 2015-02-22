from flask import Flask, request, flash, url_for, redirect, session, g, jsonify
from flask.ext.github import GitHub
from flask.ext.sqlalchemy import SQLAlchemy
from card import Card
import random
import oauth_config

app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = oauth_config.github_public_key
app.config['GITHUB_CLIENT_SECRET'] = oauth_config.github_secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = oauth_config.db_uri
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

SECRET_KEY = 'development key'
app.secret_key = SECRET_KEY

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oauth_token = db.Column(db.String(300), unique=True)
    def __init__(self, token):
        self.oauth_token = token

    def __repr__(self):
        return '<User %r>' % self.oauth_token

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    liker_id = db.Column(db.Integer)
    liked_id = db.Column(db.Integer)
    def __init__(self, liker, liked):
        self.liker_id = liker
        self.liked_id = liked

    def __repr__(self):
        return '<Match %i>' % self.id

github = GitHub(app)

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@app.route('/login')
def login():
    return github.authorize()

@app.route('/github-callback')
@github.authorized_handler
def authorized(token):
    next_url = request.args.get('next') or url_for('hello_world')
    if token is None:
        flash("Authorization failed.")
        return redirect(next_url)

    user = User.query.filter_by(oauth_token=token).first()
    if user is None:
        user = User(token)
        db.session.add(user)

    user.oauth_token = token
    db.session.commit()
    session['user_id'] = user.id
    g.user = user
    return redirect(next_url)

@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.oauth_token

@app.route('/api/getCards/<int:number>')
def get_cards(number):
    cards = []
    for i in range(number):
        cards.append(get_card())
    return jsonify(**{'data':cards})

def get_card():
    #get a random user
    #user = User.query.all()
    user = 'icechen1'
    #populate a card
    username = github.get('users/' + user)["login"] 
    name = github.get('users/'+user)["name"] 
    nbOfRepos = github.get('users/' + user)['public_repos'] 
    repositories = github.get('users/' + user + '/repos') 
    repoIndex = -1 
    if nbOfRepos <= 5: 
        repoIndex = random.randint(0,nbOfRepos-1) 
    else: 
        tuples = [] 
        for x in range(len(repositories)): 
            tuples.append((x,repositories[x]['stargazers_count'])) 
        sorted(tuples, key = lambda stars:stars[1], reverse = True)
        repoIndex = tuples[random.randint(0,4)][0] 
    repoName = repositories[repoIndex]['name'] 
    repoDescription = repositories[repoIndex]['description']
   
    #image...
    return {'username': username, 'name': name, 'repo_name' : repoName, 'description' : repoDescription}

@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80, debug = True)


