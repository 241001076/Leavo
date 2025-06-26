from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os

app = Flask(__name__)
os.makedirs("output", exist_ok=True)

reasons_en = {
    "Sick leave": "I am feeling unwell and have been advised to take rest. I kindly request medical leave to ensure a full recovery and return with renewed focus.",
    "Family Emergency": "An unforeseen family emergency demands my immediate attention and presence.",
    "Attending events": "I am obliged to attend a significant family function during the mentioned period.",
    "Unavoidable reasons": "Due to a personal commitment of unavoidable nature, I kindly request your approval for leave."
}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        from_date = request.form["from_date"]
        to_date = request.form["to_date"]
        recipient = request.form["recipient"]
        reason = request.form["reason"]
        lang = request.form["language"]

        reason_text = reasons_en.get(reason, reasons_en["Unavoidable reasons"])

        if lang == "English":
            letter = f"""
To  {recipient}

Respected Sir/Madam,

I am {name}, a student under your guidance, and I am writing to respectfully request leave from {from_date} to {to_date}.
{reason_text} I assure you that I will stay updated with all academic responsibilities during my absence. Kindly consider my application.

Thank you.

Yours sincerely,
{name}
"""
        else:
            letter = f"""
அன்பிற்கினிய {recipient} அவர்களுக்கு,
மதிப்பிற்குரிய ஐயா/அம்மையார்,

நான் {name}, உங்கள் வழிகாட்டுதலின் கீழ் கல்வி பயிலும் மாணவர்.
{from_date} முதல் {to_date} வரை விடுப்பு வேண்டுகிறேன்.
{reason_text} பாடங்களை பின்வற்று கவனிப்பேன் என உறுதியளிக்கிறேன்.

விடுப்பு வழங்குமாறு கேட்டுக்கொள்கிறேன்.

மிக்க நன்றி.
வணக்கம்,
{name}
"""

        filename = f"output/leave_letter_{name.replace(' ', '_')}.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        for line in letter.strip().split('\n'):
            pdf.multi_cell(0, 10, txt=line)

        pdf.output(filename)
        return send_file(filename, as_attachment=True)

    return render_template("index.html", reasons=list(reasons_en.keys()))

if __name__ == "__main__":
    app.run(debug=True)
