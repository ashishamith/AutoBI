from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
import os
import pandas as pd
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from groq import Groq
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

client = Groq(api_key="") #set Your Own Groq API key here

VALID_EMAIL = " "  # set your email to login
VALID_PASSWORD = " "  # set your password to login

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email == VALID_EMAIL and password == VALID_PASSWORD:
            session["user"] = email
            session["qa_log"] = []  # initialize Q&A log
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Invalid email or password")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})
    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    df = pd.read_csv(filepath)

    date_column = next((col for col in df.columns if "date" in col.lower()), None)
    if date_column:
        df[date_column] = pd.to_datetime(df[date_column], errors="coerce")
        from_date = df[date_column].min().strftime("%d-%m-%Y")
        to_date = df[date_column].max().strftime("%d-%m-%Y")
    else:
        from_date, to_date = "-", "-"

    session["uploaded_file"] = filepath
    return jsonify({"success": True, "from_date": from_date, "to_date": to_date})

def generate_graph(df, question):
    try:
        question = question.lower()
        img = BytesIO()

        if "trend" in question or "over time" in question:
            date_col = next((col for col in df.columns if "date" in col.lower()), None)
            value_col = next((col for col in df.columns if df[col].dtype in ['float64', 'int64']), None)
            if date_col and value_col:
                df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
                df = df.dropna(subset=[date_col])
                plt.figure(figsize=(8, 4))
                sns.lineplot(data=df, x=date_col, y=value_col)
                plt.title(f"{value_col} Trend Over Time")
                plt.xticks(rotation=45)
                plt.tight_layout()
        elif "compare" in question or "vs" in question:
            cols = [col for col in df.columns if df[col].dtype in ['float64', 'int64']]
            if len(cols) >= 2:
                plt.figure(figsize=(6, 4))
                sns.scatterplot(data=df, x=cols[0], y=cols[1])
                plt.title(f"{cols[1]} vs {cols[0]}")
                plt.tight_layout()
        else:
            return None

        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        return base64.b64encode(img.read()).decode('utf-8')
    except:
        return None

@app.route("/ask_question", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question", "")
    filepath = session.get("uploaded_file")
    if not filepath:
        return jsonify({"answer": "Please upload a CSV first."})

    df = pd.read_csv(filepath)
    preview = df.head(10).to_string(index=False)

    prompt = f"""
You are a business data analyst.

Based on the data below, answer the question clearly.

Data:
{preview}

Question: {question}

Format the response in readable sections like:
- Summary
- Observations
- Trends
- Suggestions
"""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"Error: {e}"

    # Save Q&A to session
    if "qa_log" not in session:
        session["qa_log"] = []
    session["qa_log"].append({"question": question, "answer": answer})

    session.modified = True

    graph = generate_graph(df, question)
    return jsonify({"answer": answer, "graph": graph})

@app.route("/download_report")
def download_report():
    qa_log = session.get("qa_log", [])
    if not qa_log:
        return "No Q&A to export", 400

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    text = c.beginText(40, height - 50)
    text.setFont("Helvetica", 10)

    text.textLine("AutoBI - Q&A Report")
    text.textLine(f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    text.textLine("-" * 80)

    for idx, qa in enumerate(qa_log, 1):
        text.textLine(f"Q{idx}: {qa['question']}")
        for line in qa["answer"].split("\n"):
            text.textLine("  " + line)
        text.textLine("-" * 80)

    c.drawText(text)
    c.showPage()
    c.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="AutoBI_Report.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
