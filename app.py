from flask import Flask, redirect, request, jsonify
import requests
import os

app = Flask(__name__)

CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDIRECT_URI = 'https://your-backend-url.com/callback'
GUILD_ID = 'your_guild_id'

@app.route('/login')
def login():
    return redirect(f'https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify%20guilds')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
    response_json = response.json()
    access_token = response_json.get('access_token')
    user_guilds = requests.get('https://discord.com/api/users/@me/guilds', headers={'Authorization': f'Bearer {access_token}'}).json()
    
    if any(guild['id'] == GUILD_ID for guild in user_guilds):
        return redirect('https://discord.com/oauth2/authorize?client_id=1197661699826798622')
    else:
        return "<script>window.close();</script>"

if __name__ == '__main__':
    app.run(debug=True)
