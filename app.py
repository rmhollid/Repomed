import os
from flask import Flask, jsonify, render_template, request
from repomedic.engine import RepairEngine

app = Flask(__name__)
engine = RepairEngine()

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "RepoMedic",
        "model": engine.model_name,
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
        "cloud_run_service": os.getenv("K_SERVICE", "local"),
    })

@app.post("/api/run-demo")
def run_demo():
    result = engine.run_demo()
    status = 200 if result.get("ok") else 500
    return jsonify(result), status

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=False)
