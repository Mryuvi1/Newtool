import os
import re
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Facebook UID Finder - KING MAKER YUVI</title>
    <style>
        body {
            background: linear-gradient(to right, #1c92d2, #f2fcfe);
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        h1 {
            color: #0c4b33;
            margin-bottom: 20px;
        }
        form {
            background: rgba(255, 255, 255, 0.15);
            padding: 20px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        input[type=text] {
            width: 300px;
            padding: 10px;
            border: none;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        input[type=submit] {
            background-color: #4caf50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        .result {
            margin-top: 20px;
            font-size: 18px;
            color: #222;
        }
    </style>
</head>
<body>
    <h1>🔍 Facebook UID Finder</h1>
    <form method="POST">
        <input type="text" name="fb_url" placeholder="Enter Facebook Profile/Post/Group URL" required>
        <br>
        <input type="submit" value="Find UID">
    </form>
    {% if uid %}
    <div class="result">
        <strong>UID:</strong> {{ uid }}
    </div>
    {% endif %}
</body>
</html>
"""

def extract_uid_from_url(url):
    try:
        if "facebook.com" not in url:
            return "❌ Invalid Facebook URL"

        headers = {'User-Agent': 'Mozilla/5.0'}
        mobile_url = url.replace("www.facebook.com", "m.facebook.com").replace("facebook.com", "m.facebook.com")
        res = requests.get(mobile_url, headers=headers, timeout=10)

        if res.status_code == 200:
            patterns = [
                r'entity_id":"(\d+)"',
                r'"userID":"(\d+)"',
                r'fb://profile/(\d+)',
                r'page_id=(\d+)',
                r'\"groupID\":\"(\d+)\"',
                r'profile_id=(\d+)',
                r'owner_id=(\d+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, res.text)
                if match:
                    return match.group(1)
            return "❌ UID not found in source"
        else:
            return f"❌ Request failed ({res.status_code})"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    uid = None
    if request.method == "POST":
        url = request.form.get("fb_url")
        if url:
            uid = extract_uid_from_url(url)
    return render_template_string(HTML_TEMPLATE, uid=uid)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
