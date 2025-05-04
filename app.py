from flask import Flask, request, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
os.environ["GOOGLE_API_KEY"] = "AIzaSyBnjqVHJ6QI62sicPiQyv2xk9rPv2uXstU"
# Initialize Gemini AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_stroke_risk(form_data):
    prompt = f"""Based on the following patient data, analyze if the patient is at significant risk of stroke. Respond with 'Yes' or 'No' followed by the reasons line by line without using any special characters like asterisks:
    - Gender: {form_data['gender']}
    - Age: {form_data['age']}
    - Hypertension: {'Yes' if form_data['hypertension'] == '1' else 'No'}
    - Heart Disease: {'Yes' if form_data['disease'] == '1' else 'No'}
    - Marital Status: {form_data['married']}
    - Work Type: {form_data['work']}
    - Residence Type: {form_data['residence']}
    - Average Glucose Level: {form_data['glucose']}
    - BMI: {form_data['bmi']}
    - Smoking Status: {form_data['smoking']}
    
    Respond with 'Yes' or 'No' and provide reasons in plain text, line by line. Do not use any special characters or formatting symbols."""

    try:
        response = model.generate_content(prompt)
        # Extract and return the response as plain text without special characters
        return response.text.strip()
    except Exception as e:
        print(f"Error calling Gemini API: {str(e)}")
        return "Error in prediction. Please try again."

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_text = ""
    
    if request.method == 'POST':
        try:
            # Get form data
            form_data = {
                'gender': request.form.get('gender'),
                'age': request.form.get('age'),
                'hypertension': request.form.get('hypertension'),
                'disease': request.form.get('disease'),
                'married': request.form.get('married'),
                'work': request.form.get('work'),
                'residence': request.form.get('residence'),
                'glucose': request.form.get('glucose'),
                'bmi': request.form.get('bmi'),
                'smoking': request.form.get('smoking')
            }
            
            # Validate required fields
            if not all(form_data.values()):
                prediction_text = "Please fill all the required fields."
            else:
                prediction_text = analyze_stroke_risk(form_data)
        
        except Exception as e:
            print(f"Error processing form: {str(e)}")
            prediction_text = "An error occurred. Please try again."
    
    return render_template('index.html', prediction_text=prediction_text)

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    return render_template('analysis.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')

@app.route('/chart', methods=['GET', 'POST'])
def chart():
    return render_template('chart.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
