import os
import re
import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# ✅ Your Facebook Cookie Here (get from browser dev tools > Application tab > Cookies)
FB_COOKIE = "sb=lCRXaOOuEAI8jwj6vAhxZU8o;ps_l=1;ps_n=1;vpd=v1%3B1130x552x1.1751712560653687;pas=100059549485809%3ASOFoyggusW;wl_cbv=v2%3Bclient_version%3A2852%3Btimestamp%3A1750868437;dpr=1.2920383214950562;datr=LD1gaN36qbuLuFpo7ZjkMyN9;locale=en_GB;c_user=100059549485809;fr=1eVdlYyJ0pjiGSVe3.AWcMD1r2cJKoWtKwazaUH1JRdLP7CKHdzqBhrCG9ffeNstdIrqM.BoZyV4..AAA.0.0.BoZyV4.AWf7Hi2h444kAZrn94KqEwxi8Jo;xs=30%3A0natGunnQV5Dtw%3A2%3A1751590212%3A-1%3A-1%3A%3AAcWc-eAEQxwMlAh2A4JQnWRUkZAcTCTm8jRHOtiCcA;wd=991x2027;presence=C%7B%22lm3%22%3A%22g.10023169007731270%22%2C%22t3%22%3A%5B%5D%2C%22utc3%22%3A1751590274043%2C%22v%22%3A1%7D;"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Facebook UID Finder - KING MAKER YUVI</title>
    <style>
        body { background: #e1f5fe; font-family: sans-serif; text-align: center; padding-top: 60px; }
        form { background: #ffffffcc; padding: 20px; display: inline-block; border-radius: 12px; }
        input[type=text] { padding: 10px; width: 300px; border-radius: 5px; border: 1px solid #ccc; }
        input[type=submit] { padding: 10px 20px; background-color: #4caf50; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .result { margin-top: 20px; font-size: 18px; }
    </style>
</head>
<body>
    <h2>🔍 Facebook UID Finder</h2>
    <form method="POST">
        <input name="fb_url" placeholder="Enter Facebook Profile / Post / Group URL" required><br><br>
        <input type="submit" value="Get UID">
    </form>
    {% if uid %}
    <div class="result"><strong>UID:</strong> {{ uid }}</div>
    {% endif %}
</body>
</html>
"""

def extract_uid_from_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Cookie': FB_COOKIE
    }

    try:
        if "facebook.com" not in url:
            return "❌ Invalid Facebook URL"

        # 🔍 1. Direct post ID from URL
        post_patterns = [
            r'/posts/(\d+)',
            r'story_fbid=(\d+)',
            r'/videos/(\d+)',
            r'photo.php\?fbid=(\d+)',
            r'/permalink/(\d+)',
            r'/reel/(\d+)',
        ]
        for pattern in post_patterns:
            match = re.search(pattern, url)
            if match:
                return f"📌 Post UID: {match.group(1)}"

        # 🔍 2. Fallback: check page source (for profile/group UID)
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            html = response.text
            uid_patterns = [
                r'entity_id":"(\d+)"',
                r'"userID":"(\d+)"',
                r'page_id=(\d+)',
                r'\"groupID\":\"(\d+)\"',
                r'profile_id=(\d+)',
                r'owner_id=(\d+)',
            ]
            for pattern in uid_patterns:
                match = re.search(pattern, html)
                if match:
                    return f"👤 Profile/Group UID: {match.group(1)}"
            return "❌ UID not found in page"
        else:
            return f"❌ HTTP Error: {response.status_code}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

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
