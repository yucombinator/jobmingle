from flask import Flask, request, flash, url_for, redirect
from flask.ext.github import GitHub

app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = 'XXX'
app.config['GITHUB_CLIENT_SECRET'] = 'YYY'

# For GitHub Enterprise
app.config['GITHUB_BASE_URL'] = 'https://HOSTNAME/api/v3/'
app.config['GITHUB_AUTH_URL'] = 'https://HOSTNAME/login/oauth/'

github = GitHub(app)

@app.route('/login')
def login():
    return github.authorize()

@app.route('/github-callback')
@github.authorized_handler
def authorized(oauth_token):
    next_url = request.args.get('next') or url_for('index')
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

@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run()


