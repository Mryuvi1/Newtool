
from flask import Flask, render_template, send_from_directory
from tools.uid_finder import uid_finder_bp
from tools.token_checker import token_checker_bp
from tools.spammer1 import spammer1_bp
from tools.spammer2 import spammer2_bp

app = Flask(__name__)
app.register_blueprint(uid_finder_bp, url_prefix='/tool/uid_finder')
app.register_blueprint(token_checker_bp, url_prefix='/tool/token_checker')
app.register_blueprint(spammer1_bp, url_prefix='/tool/spam1')
app.register_blueprint(spammer2_bp, url_prefix='/tool/spam2')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
