import os
from flask import Flask, render_template_string, request
from google import genai

app = Flask(__name__)

# Gemini API Configuration
API_KEY = "AQ.Ab8RN6L3AfXnH7SWh4kS0lrS3qUp2zg-AO_b6BSKmY-uWx1C8Q"
client = genai.Client(api_key=API_KEY)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SiteAura AI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Marked.js for Markdown Rendering -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        body { background-color: #f4f6f9; padding: 15px; }
        .card { border-radius: 12px; border: none; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }
        .report-box { background: #ffffff; padding: 20px; border-left: 5px solid #0d6efd; border-radius: 6px; }
        .report-box h1, .report-box h2, .report-box h3 { font-size: 1.25rem; font-weight: bold; margin-top: 15px; color: #0d6efd; }
        .report-box ul { padding-left: 20px; }
    </style>
</head>
<body>
    <div class="container" style="max-width: 800px;">
        <div class="card p-4 mb-4">
            <h3 class="text-center text-primary mb-1">🏗️ SiteAura AI</h3>
            <p class="text-center text-muted mb-4">Automated Daily Site Progress Writer for Civil Engineers</p>
            
            <form method="POST">
                <div class="row g-3">
                    <div class="col-md-6">
                        <label class="form-label font-weight-bold">Project Name</label>
                        <input type="text" name="project_name" class="form-control" placeholder="ABC Housing Project" required>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label font-weight-bold">Engineer Name</label>
                        <input type="text" name="engineer_name" class="form-control" placeholder="Your Name" required>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label font-weight-bold">Site Location</label>
                        <input type="text" name="location" class="form-control" placeholder="Rawalpindi" required>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label font-weight-bold">Weather</label>
                        <select name="weather" class="form-select">
                            <option>Clear / Sunny</option>
                            <option>Rainy</option>
                            <option>Overcast</option>
                        </select>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label font-weight-bold">Date</label>
                        <input type="date" name="date" class="form-control" required>
                    </div>
                    <div class="col-12">
                        <label class="form-label font-weight-bold">📝 Aaj ke kaam ke bullet points likhein</label>
                        <textarea name="notes" class="form-control" rows="4" placeholder="- 100 bag cement aya&#10;- foundation excavation 50% complete" required></textarea>
                    </div>
                    <div class="col-12">
                        <button type="submit" class="btn btn-primary w-100 py-2 fw-bold">Generate Professional Report</button>
                    </div>
                </div>
            </form>
        </div>

        {% if report %}
        <div class="card p-4">
            <h5 class="fw-bold mb-3">DAILY SITE PROGRESS REPORT</h5>
            <div id="report-content" class="report-box"></div>
            <textarea id="raw-report" style="display:none;">{{ report }}</textarea>
        </div>
        <script>
            const rawText = document.getElementById('raw-report').value;
            document.getElementById('report-content').innerHTML = marked.parse(rawText);
        </script>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    report = None
    if request.method == 'POST':
        project_name = request.form.get('project_name')
        engineer_name = request.form.get('engineer_name')
        location = request.form.get('location')
        weather = request.form.get('weather')
        date = request.form.get('date')
        notes = request.form.get('notes')

        prompt = f"""
        Aap ek Civil Site Engineer ke assistant hain. 
        In details ki bunyaad par ek professional "Daily Site Progress Report" format karein:

        - Project Name: {project_name}
        - Engineer Name: {engineer_name}
        - Location: {location}
        - Weather: {weather}
        - Date: {date}
        - Raw Site Notes:
        {notes}

        Report ko clean, professional aur formatted bullet points mein structured pesh karein.
        """

        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
            )
            report = response.text
        except Exception as e:
            report = f"API Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, report=report)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
