import pandas as pd
import json
import logging
from db_interface import DBInterface

logging.basicConfig(level=logging.INFO)

def clean_customer_data(df):
    df = df.dropna(subset=['Customer_ID'])
    df['Browsing_History'] = df['Browsing_History'].apply(lambda x: json.dumps(eval(x)) if pd.notnull(x) else '[]')
    df['Purchase_History'] = df['Purchase_History'].apply(lambda x: json.dumps(eval(x)) if pd.notnull(x) else '[]')
    return df

def clean_product_data(df):
    df = df.dropna(subset=['Product_ID'])
    df['Similar_Product_List'] = df['Similar_Product_List'].apply(lambda x: json.dumps(eval(x)) if pd.notnull(x) else '[]')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['avg_rating_similar'] = pd.to_numeric(df['Average_Rating_of_Similar_Products'], errors='coerce')
    df['product_rating'] = pd.to_numeric(df['Product_Rating'], errors='coerce')
    df['customer_review_sentiment_score'] = pd.to_numeric(df['Customer_Review_Sentiment_Score'], errors='coerce')
    df['probability_of_recommendation'] = pd.to_numeric(df['Probability_of_Recommendation'], errors='coerce')
    return df

def ingest_data(customer_csv, product_csv, db_path='carelite.db'):
    cust_df = pd.read_csv(customer_csv, sep='\t')
    prod_df = pd.read_csv(product_csv, sep='\t')
    cust_df = clean_customer_data(cust_df)
    prod_df = clean_product_data(prod_df)
    
    db = DBInterface(db_path)
    db.init_tables()
    
    for _, row in cust_df.iterrows():
        record = {
            'customer_id': row['Customer_ID'],
            'age': int(row['Age']) if pd.notnull(row['Age']) else None,
            'gender': row['Gender'],
            'location': row['Location'],
            'browsing_history': row['Browsing_History'],
            'purchase_history': row['Purchase_History'],
            'customer_segment': row['Customer_Segment'],
            'avg_order_value': float(row['Avg_Order_Value']) if pd.notnull(row['Avg_Order_Value']) else None,
            'holiday': row['Holiday'],
            'season': row['Season']
        }
        db.insert_record('customers', record)
    
    for _, row in prod_df.iterrows():
        record = {
            'product_id': row['Product_ID'],
            'category': row['Category'],
            'subcategory': row['Subcategory'],
            'price': float(row['Price']) if pd.notnull(row['Price']) else None,
            'brand': row['Brand'],
            'avg_rating_similar': float(row['Average_Rating_of_Similar_Products']) if pd.notnull(row['Average_Rating_of_Similar_Products']) else None,
            'product_rating': float(row['Product_Rating']) if pd.notnull(row['Product_Rating']) else None,
            'customer_review_sentiment_score': float(row['Customer_Review_Sentiment_Score']) if pd.notnull(row['Customer_Review_Sentiment_Score']) else None,
            'holiday': row['Holiday'],
            'season': row['Season'],
            'geographical_location': row['Geographical_Location'],
            'similar_product_list': row['Similar_Product_List'],
            'probability_of_recommendation': float(row['Probability_of_Recommendation']) if pd.notnull(row['Probability_of_Recommendation']) else None
        }
        db.insert_record('products', record)
    
    logging.info("Data ingestion complete.")
