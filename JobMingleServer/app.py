from flask import Flask, request, flash, url_for, redirect, g, jsonify
from flask.ext.github import GitHub
from card import Card
import oauth_config

app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = oauth_config.github_public_key
app.config['GITHUB_CLIENT_SECRET'] = oauth_config.github_secret_key

github = GitHub(app)

@app.route('/login')
def login():
    return github.authorize()

@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('hello_world')
    if oauth_token is None:
        flash("Authorization failed.")
        return redirect(next_url)

    #user = User.query.filter_by(github_access_token=oauth_token).first()
    #if user is None:
    #    user = User(oauth_token)
    #    db_session.add(user)

   # user.github_access_token = oauth_token
   # db_session.commit()
    return redirect(next_url)

@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token

@app.route('/api/getCards/<int:number>')
def get_cards(number):
    cards = []
    for i in range(number):
        cards.append(get_card())
    return jsonify(cards)

def get_card():
    #get a random user
    #user = #getdb
    #populate a card
    #repo = github.get('user/repos/' + user)

    #username = github.get('users/' + user)
    #name = github.get('repos/cenkalti/github-flask')
    #description = github.get('repos/cenkalti/github-flask')
    #image...
    return Card(username,name, None, description)

@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run(debug = True)


