async function getHealth() {
  const r = await fetch("/api/health");
  const h = await r.json();
  document.querySelector("#runtime").textContent =
    h.cloud_run_service === "local" ? "Local" : `Cloud Run: ${h.cloud_run_service}`;
  document.querySelector("#model").textContent = h.model;
}

const button = document.querySelector("#run");
button.addEventListener("click", async () => {
  button.disabled = true;
  button.textContent = "Running tests → Gemini → patch → tests…";
  document.querySelector("#progress").classList.remove("hidden");
  document.querySelector("#result").classList.add("hidden");
  document.querySelector("#actions").innerHTML =
    "<li>Starting isolated repair workflow…</li>";

  try {
    const r = await fetch("/api/run-demo", {method: "POST"});
    const data = await r.json();
    if (!r.ok && !data.actions) throw new Error(data.error || "Repair run failed.");

    document.querySelector("#actions").innerHTML =
      (data.actions || []).map(x => `<li>${escapeHtml(x)}</li>`).join("");

    document.querySelector("#result").classList.remove("hidden");
    document.querySelector("#badge").textContent = data.ok ? "VALIDATED" : "FAILED";
    document.querySelector("#badge").className = data.ok ? "good" : "bad";
    document.querySelector("#diagnosis").textContent =
      data.agent?.decision?.diagnosis || "No diagnosis returned.";
    document.querySelector("#reason").textContent =
      data.agent?.decision?.reason || "No reason returned.";
    document.querySelector("#diff").textContent = data.patch?.diff || "";
    document.querySelector("#before").textContent =
      (data.before?.stdout || "") + "\n" + (data.before?.stderr || "");
    document.querySelector("#after").textContent =
      (data.after?.stdout || "") + "\n" + (data.after?.stderr || "");
  } catch (e) {
    alert(e.message);
  } finally {
    button.disabled = false;
    button.textContent = "Run repair agent";
  }
});

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

getHealth().catch(() => {
  document.querySelector("#runtime").textContent = "unavailable";
  document.querySelector("#model").textContent = "unavailable";
});
