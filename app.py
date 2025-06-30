
from flask import Flask, render_template, request, session, redirect, url_for
from tools.token_generator import get_facebook_token

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/tool/token_generator', methods=['GET', 'POST'])
def token_generator():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'DARKHUNTER':  # You can change this password
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    result = None
    if request.method == 'POST':
        cookies = request.form.get('cookies', '').strip()
        if cookies:
            result = get_facebook_token(cookies)
    return render_template('tool_token_generator.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
