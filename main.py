import os
import re
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Minimal HTML test to verify route working
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
  <head><title>Facebook UID Finder</title></head>
  <body style="text-align: center; margin-top: 50px;">
    <h2>🔍 Facebook UID Finder</h2>
    <form method="POST">
      <input name="fb_url" style="width: 300px;" placeholder="Enter Facebook URL" required>
      <br><br>
      <button type="submit">Find UID</button>
    </form>
    {% if uid %}
      <p><strong>UID:</strong> {{ uid }}</p>
    {% endif %}
  </body>
</html>
"""

def extract_uid_from_url(url):
    try:
        if "facebook.com" not in url:
            return "Invalid Facebook URL"

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
            return "UID not found"
        else:
            return f"Failed to fetch ({res.status_code})"
    except Exception as e:
        return f"Error: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    uid = None
    if request.method == "POST":
        fb_url = request.form.get("fb_url")
        if fb_url:
            uid = extract_uid_from_url(fb_url)
    return render_template_string(HTML_TEMPLATE, uid=uid)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
