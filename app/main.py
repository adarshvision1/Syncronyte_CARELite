from flask import Flask, request, jsonify, render_template, redirect, url_for
from data_extraction import ingest_data
from rule_recommender import recommend_products_for_user
from feedback_agent import record_feedback, train_feedback_model, adjust_threshold
import os, logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__, template_folder='templates', static_folder='static')

# Define constants for file paths
CUSTOMER_CSV = os.path.join('data', 'customer_data_collection.csv')
PRODUCT_CSV = os.path.join('data', 'product_recommendation_data.csv')
DB_PATH = 'carelite.db'

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

# Upload route for CSV files
@app.route('/upload', methods=['POST'])
def upload_files():
    customer_file = request.files.get('customer_file')
    product_file = request.files.get('product_file')
    if not customer_file or not product_file:
        return render_template('dashboard.html', message="Missing files for upload.")
    try:
        customer_path = CUSTOMER_CSV
        product_path = PRODUCT_CSV
        customer_file.save(customer_path)
        product_file.save(product_path)
        ingest_data(customer_path, product_path, db_path=DB_PATH)
        message = "Files uploaded and data ingested successfully."
    except Exception as e:
        logging.error(f"Upload error: {e}")
        message = f"Error during file upload: {e}"
    return render_template('dashboard.html', message=message)

# Ingest route (can be triggered separately too)
@app.route('/ingest', methods=['POST'])
def ingest():
    try:
        ingest_data(CUSTOMER_CSV, PRODUCT_CSV, db_path=DB_PATH)
        return jsonify({'msg': 'Data ingestion complete.'}), 200
    except Exception as e:
        logging.error(f"Ingestion error: {e}")
        return jsonify({'error': str(e)}), 500

# Get recommendations via dashboard form submission
@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    customer_id = request.form.get('customer_id')
    try:
        recs = recommend_products_for_user(customer_id, db_path=DB_PATH)
        return render_template('dashboard.html', recommendations=recs, message=f"Recommendations for {customer_id}")
    except Exception as e:
        logging.error(f"Recommendation error: {e}")
        return render_template('dashboard.html', message=str(e))

# Route to record feedback using a form
@app.route('/feedback_form', methods=['POST'])
def feedback_form():
    customer_id = request.form.get('feedback_customer_id')
    product_id = request.form.get('feedback_product_id')
    try:
        clicked = int(request.form.get('feedback_clicked'))
        dwell_time = float(request.form.get('feedback_dwell_time'))
        record_feedback(customer_id, product_id, clicked, dwell_time, db_path=DB_PATH)
        message = "Feedback recorded successfully."
    except Exception as e:
        logging.error(f"Feedback form error: {e}")
        message = str(e)
    return render_template('dashboard.html', message=message)

# Train feedback model endpoint (called via JS button)
@app.route('/train-feedback-model', methods=['POST'])
def train_model():
    try:
        mdl = train_feedback_model(db_path=DB_PATH)
        msg = "Feedback model trained." if mdl else "No feedback data available to train the model."
        return jsonify({'msg': msg}), 200
    except Exception as e:
        logging.error(f"Train model error: {e}")
        return jsonify({'error': str(e)}), 500

# Predict feedback outcome endpoint (called via JS button)
@app.route('/predict-feedback', methods=['GET'])
def predict_feedback():
    try:
        dwell_time = float(request.args.get('dwell_time'))
        probability = adjust_threshold(dwell_time)
        return jsonify({'dwell_time': dwell_time, 'probability': probability}), 200
    except Exception as e:
        logging.error(f"Predict feedback error: {e}")
        return jsonify({'error': str(e)}), 500

# Main dashboard showing all functionalities
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    message = request.args.get('message', '')
    # Optional: pass along recommendations if available
    recommendations = None
    return render_template('dashboard.html', message=message, recommendations=recommendations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
