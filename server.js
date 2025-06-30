async function getUID() {
  const fbLink = document.getElementById("fbLink").value.trim();
  const output = document.getElementById("output");

  if (!fbLink.includes("facebook.com")) {
    output.innerHTML = "❌ Please enter a valid Facebook URL.";
    return;
  }

  output.innerHTML = "⏳ Checking UID...";

  try {
    const res = await fetch(`https://your-backend-url.com/get-uid?url=${encodeURIComponent(fbLink)}`);
    const data = await res.json();

    if (data.uid) {
      output.innerHTML = `✅ UID Found: <span style="color:green">${data.uid}</span>`;
    } else {
      output.innerHTML = `❌ ${data.error || "UID not found."}`;
    }
  } catch (e) {
    output.innerHTML = "⚠️ Error fetching profile.";
  }
}
