import secrets
import inference
from flask import Flask, current_app, request, make_response

app = Flask(__name__)

contexts = {}

@app.route("/")
def handle_index():
    return current_app.send_static_file("index.html")

@app.post("/upload")
def handle_upload():
    session_id    = secrets.token_urlsafe(32)
    uploaded_file = request.get_data().decode("utf-8")

    contexts[session_id] = inference.make_context(uploaded_file)
    
    response = make_response()
    response.set_cookie("session_id", session_id)
    return response

@app.route("/query")
def handle_query():
    session_id = request.cookies.get("session_id")
    query      = request.args.get("query")

    if query is None or session_id not in contexts:
        return ""
    
    context    = contexts[session_id]
    return inference.run_query(context, query)

