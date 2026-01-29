"""
Flask application to receive GitHub webhooks,
store minimal event data in MongoDB,
and serve UI polling endpoints.
"""

from flask import Flask, request, jsonify, render_template
from datetime import datetime
from models import save_event, get_recent_events

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """
    Render the UI page.
    """
    return render_template("index.html")


@app.route("/webhook", methods=["GET", "POST"])
def github_webhook():
    """
    GitHub webhook receiver.
    Handles:
    - GET  : Health check
    - ping : Webhook validation
    - push : Push events
    - pull_request : PR open & merge events
    """

    # Health check (browser / tunnel / GitHub GET)
    if request.method == "GET":
        return jsonify({"status": "webhook alive"}), 200

    payload = request.get_json(silent=True)
    github_event = request.headers.get("X-GitHub-Event")

    # GitHub ping event (sent when webhook is created)
    if github_event == "ping":
        return jsonify({"msg": "pong"}), 200

    # If payload is missing, exit gracefully
    if not payload:
        return jsonify({"status": "no payload"}), 200

    event_data = None
    current_time = datetime.now()



    # PUSH EVENT

    if github_event == "push":
        branch_name = payload.get("ref", "").split("/")[-1]

        event_data = {
            "request_id": payload.get("after"),
            "author": payload.get("pusher", {}).get("name"),
            "action": "PUSH",
            "from_branch": branch_name,
            "to_branch": branch_name,
            "timestamp": current_time.strftime("%d %B %Y - %I:%M %p IST"),
            "created_at": current_time
        }


    # PULL REQUEST / MERGE EVENT

    elif github_event == "pull_request":
        action_type = payload.get("action")
        pr_data = payload.get("pull_request", {})

        # Pull request opened
        if action_type == "opened":
            event_data = {
                "request_id": str(pr_data.get("id")),
                "author": pr_data.get("user", {}).get("login"),
                "action": "PULL_REQUEST",
                "from_branch": pr_data.get("head", {}).get("ref"),
                "to_branch": pr_data.get("base", {}).get("ref"),
                "timestamp": current_time.strftime("%d %B %Y - %I:%M %p UTC"),
                "created_at": current_time
            }

        # Pull request merged 
        elif action_type == "closed" and pr_data.get("merged"):
            event_data = {
                "request_id": pr_data.get("merge_commit_sha"),
                "author": pr_data.get("merged_by", {}).get("login"),
                "action": "MERGE",
                "from_branch": pr_data.get("head", {}).get("ref"),
                "to_branch": pr_data.get("base", {}).get("ref"),
                "timestamp": current_time.strftime("%d %B %Y - %I:%M %p UTC"),
                "created_at": current_time
            }

    # Persist event if valid
    if event_data:
        try:
            save_event(event_data)
        except Exception as e:
            # Prevent webhook failure if DB has transient issues
            print("MongoDB insert failed:", e)

    return jsonify({"status": "success"}), 200


@app.route("/events", methods=["GET"])
def fetch_events():
    """
    UI polling endpoint.
    Returns only events from the last 15 seconds.
    Never crashes the UI if MongoDB fails.
    """
    try:
        return jsonify(get_recent_events()), 200
    except Exception as e:
        print("MongoDB fetch failed:", e)
        return jsonify([]), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

