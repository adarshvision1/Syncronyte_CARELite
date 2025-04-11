import json
from db_interface import DBInterface
import logging

logging.basicConfig(level=logging.INFO)

def recommend_products_for_user(customer_id, db_path='carelite.db'):
    db = DBInterface(db_path)
    q = "SELECT browsing_history FROM customers WHERE customer_id = ?"
    result = db.fetch_query(q, (customer_id,))
    recommendations = []
    if result:
        try:
            history = json.loads(result[0][0])
            for cat in history:
                sql = """
                    SELECT product_id, category, subcategory, price, brand, product_rating, probability_of_recommendation 
                    FROM products 
                    WHERE category = ? AND probability_of_recommendation > 0.5
                    ORDER BY probability_of_recommendation DESC LIMIT 3
                """
                recommendations.extend(db.fetch_query(sql, (cat,)))
        except Exception as e:
            logging.error(f"Error processing browsing history: {e}")
    if not recommendations:
        recommendations = db.fetch_query(
            "SELECT product_id, category, subcategory, price, brand, product_rating, probability_of_recommendation FROM products ORDER BY product_rating DESC LIMIT 5"
        )
    return recommendations
