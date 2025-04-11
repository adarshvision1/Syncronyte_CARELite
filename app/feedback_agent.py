import numpy as np
from sklearn.linear_model import LogisticRegression
from db_interface import DBInterface
import logging

logging.basicConfig(level=logging.INFO)
model = LogisticRegression()

def train_feedback_model(db_path='carelite.db'):
    db = DBInterface(db_path)
    data = db.fetch_query("SELECT clicked, dwell_time FROM feedback")
    if not data:
        logging.warning("No feedback data available for training.")
        return None
    X = [[float(dwell_time)] for clicked, dwell_time in data]
    y = [int(clicked) for clicked, dwell_time in data]
    model.fit(X, y)
    logging.info("Feedback model trained.")
    return model

def adjust_threshold(dwell_time):
    if not hasattr(model, "coef_"):
        raise Exception("Model not trained. Call train_feedback_model() first.")
    probability = model.predict_proba([[dwell_time]])[0][1]
    return probability

def record_feedback(customer_id, product_id, clicked, dwell_time, db_path='carelite.db'):
    db = DBInterface(db_path)
    record = {
        'customer_id': customer_id,
        'product_id': product_id,
        'clicked': clicked,
        'dwell_time': dwell_time,
        'feedback_time': np.datetime64('now').astype('M8[s]').astype(str)
    }
    db.insert_record('feedback', record)
    logging.info("Feedback recorded.")
