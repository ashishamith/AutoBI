# **AutoBI** – AI-Powered Business Insights from CSV Data

AutoBI is a **Flask-based web application** that lets non-technical users analyze CSV data using **natural language questions**.  
It uses **Groq's LLaMA-3 model** to understand queries, analyze data, and generate **clear business insights**.  
The app also **auto-generates graphs** and allows downloading **PDF reports** of all Q&A.

---

## **🚀 Features**
1. **Secure Login** – Simple email & password authentication.
2. **CSV Upload** – Upload any business dataset for analysis.
3. **Natural Language Questions** – Ask queries like  
   > "What is the sales trend over time?"  
   > "Compare profit vs sales."
4. **AI-Generated Insights** – Summarized in sections:
   - Summary  
   - Observations  
   - Trends  
   - Suggestions
5. **Automatic Graph Generation** – Detects trends, comparisons, and generates:
   - Line charts for time-based trends  
   - Scatter plots for comparisons
6. **PDF Report Export** – Download all Q&A with timestamps.
7. **Interactive Frontend** – Clean dashboard with responsive design.

---

## **🛠 Tools & Technologies Used**
- **Backend**: Flask – Web framework for Python
- **Frontend**: HTML, CSS, JavaScript
- **AI Model**: Groq LLaMA-3 70B – Natural Language to Data Insight
- **Data Handling**: Pandas – CSV reading & preprocessing
- **Graphs**: Matplotlib, Seaborn
- **PDF Generation**: ReportLab
- **Session Management**: Flask session

---

## **📂 Project Structure**

AutoBI/
│
├── app.py # Main Flask app
├── templates/
│ ├── login.html # Login page
│ └── dashboard.html # Dashboard page
├── static/
│ ├── style.css # Styling
│ └── script.js # Frontend logic
├── uploads/ # Uploaded CSV files
└── README.md # Documentation



---

## ⚙️ Installation & Setup
**1. Clone Repository**
```bash
git clone https://github.com/your-username/AutoBI.git
cd AutoBI


2. Install Requirements
pip install flask pandas matplotlib seaborn reportlab groq


3. Add Your Groq API Key
client = Groq(api_key="YOUR_GROQ_API_KEY") # Set Your Groq API Key 


4. Run the App
python app.py


Login credentials:
Email: # Set up Your own Email in app.py
Password: #set your own password in app.py


💡 How to Use

1. Login to your account.
2. Upload a CSV dataset.
3. Ask a question in plain English.
4. View AI-generated insights.
5. Check generated graph (if available).
6. Download the PDF report.


📝 Example Questions

1. "Which product had the highest sales?"
2. "What is the profit trend over the last year?"
3. "Compare marketing spend vs revenue."
4. "Show monthly growth rate."


📦 Sample Output
AI Answer

Summary:
Sales increased steadily over the year.

Observations:
- Q4 saw the highest spike.
- Marketing spend correlates with revenue growth.

Trends:
Upward trend in overall performance.

Suggestions:
Invest more in high-performing regions.
Graph – Auto-generated chart based on question.