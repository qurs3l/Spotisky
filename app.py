from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

#defining consts
CLIENT_ID = "b3d8a81abd2c44da92c119308d490849"
CLIENT_SECRET = "d9544c2e106946f5b73b336ce5460b79"

app = Flask(__name__)

app.secret_key = 'aldkfjalkdjflakdfj'
app.config['SESSION_COOKIE_NAME'] = 'Spotisky Cookie'
TOKEN_INFO = 'token_info'


def create_spotify_auth():
    return SpotifyOAuth(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri = url_for('redirectPage', _external = True),
        scope = 'user-top-read'
    )

@app.route('/')
def login():
    sp_auth = create_spotify_auth()
    auth_url = sp_auth.get_authorize_url()
    return redirect(auth_url)

@app.route("/redirect")
def redirectPage():
    sp_auth = create_spotify_auth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_auth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external = True))

@app.route("/getTracks")
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for('login', _external = False))
    
    sp = spotipy.Spotify(auth = token_info['access_token'])
    return str(sp.current_user_top_tracks(limit=10, offset=0, time_range='medium_term')['items'][0])

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_auth = create_spotify_auth()
        token_info = sp_auth.refresh_access_token(token_info['refresh_token'])
    return token_info