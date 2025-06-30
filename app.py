from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from tools.token_generator import get_facebook_token

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/tool/token_generator', methods=['GET', 'POST'])
def token_generator():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    result = None
    if request.method == 'POST':
        cookies = request.form.get('cookies', '').strip()
        if cookies:
            result = get_facebook_token(cookies)
    return render_template('tool_token_generator.html', result=result)
