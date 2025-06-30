const express = require("express");
const fetch = require("node-fetch");
const cors = require("cors");

const app = express();
app.use(cors());

app.get("/get-uid", async (req, res) => {
  const fbUrl = req.query.url;
  if (!fbUrl || !fbUrl.includes("facebook.com")) {
    return res.status(400).json({ error: "Invalid Facebook URL" });
  }

  try {
    const response = await fetch(fbUrl, {
      headers: {
        "User-Agent": "Mozilla/5.0" // Required for Facebook to respond
      }
    });
    const html = await response.text();

    const match = html.match(/"entity_id":"(\d{6,20})"/);
    if (match && match[1]) {
      return res.json({ uid: match[1] });
    } else {
      return res.status(404).json({ error: "UID not found" });
    }
  } catch (err) {
    return res.status(500).json({ error: "Server error" });
  }
});

app.listen(3000, () => console.log("✅ Server running on port 3000"));
