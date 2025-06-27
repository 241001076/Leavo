from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os
from datetime import datetime

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
        reason = request.form["reason"].strip()
        workplace = request.form["workplace"]
        location = request.form["location"]

        reason_text = reasons_en.get(reason, reasons_en["Unavoidable reasons"])
        current_date = datetime.now().strftime("%d/%m/%Y")

        letter = f"""


From
   {name}
   {workplace}
   {location}
   Date: {current_date}

To
  {recipient}
  {workplace}

Respected Sir/Madam,

            I am {name}, a student under your guidance, and I am writing to respectfully request leave from {from_date} to {to_date}. {reason_text} I assure you that I will stay updated with all academic responsibilities during my absence. Kindly consider my application.

                                                     Thank you.

Yours sincerely,
{name}
"""

        filename = f"output/leave_letter_{name.replace(' ', '_')}.pdf"
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Permission Letter", ln=True, align='C')
        pdf.ln(5)
        pdf.set_font("Arial", size=13)
        for line in letter.strip().split('\n'):
            pdf.multi_cell(0, 10, txt=line)
        pdf.output(filename)
        return send_file(filename, as_attachment=True)

    return render_template("index.html", reasons=list(reasons_en.keys()))

if __name__ == "__main__":
    app.run(debug=True)



