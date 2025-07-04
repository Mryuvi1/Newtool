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
    <title>Facebook UID Finder - 🩷𝐋𝐄𝐆𝐄𝐍𝐃𝐗𝐃 𝐘𝐔𝐕𝐈🪽</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: url('https://i.postimg.cc/1XcXKZgm/4fb6778b638a514ffd959077ac731aa8.jpg') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Segoe UI', sans-serif;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        form {
    backdrop-filter: blur(15px);
    background: rgba(255, 255, 255, 0.1);
    padding: 40px 50px;
    border-radius: 20px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
    text-align: center;
    color: #fff;
}
        h2 {
    color: #fff;
    font-size: 28px;
    margin-bottom: 25px;
    text-shadow: 0 0 6px #00ffcc, 0 0 12px #00ffcc;
}
        input[type=text] {
    padding: 14px;
    font-size: 17px;
            width: 100%;
            max-width: 350px;
            margin-bottom: 20px;
            border: none;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.2);
            color: #fff;
            font-size: 16px;
            backdrop-filter: blur(5px);
            box-shadow: inset 0 0 5px rgba(255,255,255,0.2);
        }
        input[type=text]::placeholder {
            color: #eee;
        }
        input[type=submit] {
            padding: 12px 25px;
            background: linear-gradient(135deg, #00ffcc, #00ccff);
            color: #000;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: 0.3s ease;
            box-shadow: 0 0 10px #00ffcc, 0 0 20px #00ccff;
        }
        input[type=submit]:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px #00ffcc, 0 0 30px #00ccff;
        }
        .result {
            margin-top: 20px;
            font-size: 20px;
            color: #fff;
            text-shadow: 0 0 5px #00ffcc, 0 0 10px #00ccff;
        }
        .creator-badge {
            position: absolute;
            top: 20px;
            left: 20px;
            padding: 10px 16px;
            background: rgba(0, 0, 0, 0.4);
            color: #00ffcc;
            font-weight: bold;
            font-size: 17px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 0 12px #00ffcc, 0 0 24px #00ccff;
            text-shadow: 0 0 6px #00ffff;
            font-family: 'Segoe UI', sans-serif;
        }
        .creator-badge img {
            height: 40px;
            width: 40px;
            object-fit: cover;
            border-radius: 50%;
            border: 2px solid #00ccff;
        }
    </style>
</head>
<body>

    <!-- 🔥 Branding badge -->
    <div class="creator-badge">
        <img src="https://i.postimg.cc/c4pk3yRg/a58f941bc7aaad40797dfe63fcaaa34e.jpg" alt="YUVI Logo">
        <span>KING MAKER YUVI</span>
    </div>

    <!-- 💼 Tool Interface -->
    <form method="POST">
        <h2>🔍 Facebook UID Finder</h2>
        <input name="fb_url" placeholder="Enter Facebook Profile / Post / Group URL" required><br>
        <input type="submit" value="Get UID">
        {% if uid %}
            <div class="result" id="uid-box"><strong>UID:</strong> {{ uid }}</div>
            <script>
                const uidText = "{{ uid }}";
                navigator.clipboard.writeText(uidText).then(function() {
                    const notice = document.createElement("div");
                    notice.innerText = "📋 UID copied to clipboard!";
                    notice.style.marginTop = "10px";
                    notice.style.color = "lime";
                    notice.style.fontWeight = "bold";
                    document.getElementById("uid-box").appendChild(notice);
                });
            </script>
        {% endif %}
    </form>

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

        # 🔍 Step 1: Try extracting Post UID directly from URL
        post_patterns = [
            r'/posts/(\d{5,})',
            r'story_fbid=(\d{5,})',
            r'/videos/(\d{5,})',
            r'photo.php\?fbid=(\d{5,})',
            r'/permalink/(\d{5,})',
            r'/reel/(\d{5,})'
        ]
        for pattern in post_patterns:
            match = re.search(pattern, url)
            if match:
                return f"📌 Post UID: {match.group(1)}"

        # 🔁 Now fetch page and search for profile/group UID
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            html = response.text
            patterns = [
                r'entity_id":"(\d+)"',
                r'"userID":"(\d+)"',
                r'page_id=(\d+)',
                r'\"groupID\":\"(\d+)\"',
                r'profile_id=(\d+)',
                r'owner_id=(\d+)',
            ]
            for pattern in patterns:
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
