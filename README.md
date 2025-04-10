# CARE Lite: Intelligent Product Recommender

**Hackathon:** Hack the Future: A Gen AI Sprint Powered by Data
**Team:** Syncronyte

## Overview

CARE Lite is a lightweight and deployable intelligent product recommender system designed to enhance personalization for niche e-commerce platforms. It addresses the challenges of manual recommendation processes by providing an automated and adaptive solution powered by a multi-agent system. CARE Lite combines the speed and predictability of rule-based logic with the continuous learning capabilities of a lightweight machine learning model to deliver relevant product suggestions, ultimately aiming to boost customer engagement and drive sales.

## Problem Statement

In the competitive e-commerce landscape, personalized product recommendations are crucial for improving customer engagement and increasing conversion rates. Many niche e-commerce platforms struggle with:

* **Labor-intensive manual data collection and segmentation.**
* **Inefficient recommendation generation based on rudimentary segmentation.**
* **Limited ability to capture nuanced customer preferences.**
* **Delayed and suboptimal product recommendations leading to lower conversion rates.**

Existing open-source recommendation engines can often be too complex and resource-intensive for smaller platforms. CARE Lite offers a lightweight and immediately deployable alternative.

## Proposed Solution

CARE Lite utilizes a multi-agent system to automate and personalize product recommendations:

* **Data Extraction Agent (DEA):** Automatically ingests and preprocesses customer Browse and purchase data from CSV datasets (`customer_data_collection.csv` and `product_recommendation_data.csv`).
* **Rule-Based Recommendation Agent (RRA):** Applies dynamic, manually curated rules to generate initial recommendations (e.g., recommending top-rated items from frequently viewed categories).
* **Feedback Integration Agent (FIA):** Employs a lightweight logistic regression model to incorporate real-time user interaction feedback (clicks, dwell time) and dynamically adjust recommendation thresholds.
* **Human Override:** A merchant dashboard (conceptualized) allows for real-time monitoring and manual adjustments when needed.

This hybrid approach combines the immediate effectiveness of rule-based recommendations with the continuous improvement offered by adaptive feedback learning.

## Key Features

* **Automated Data Processing:** Simplifies data ingestion and preparation.
* **Dynamic Rule Engine:** Enables flexible and easily modifiable recommendation rules.
* **Adaptive Learning:** Continuously improves recommendation accuracy based on user interactions.
* **Lightweight and Deployable:** Optimized for small-to-medium e-commerce platforms with minimal infrastructure requirements.
* **Scalability Roadmap:** Designed with future migration to cloud databases in mind.
* **Potential for Generative AI Integration:** Future plans include using generative AI to suggest dynamic rule modifications.

## Technologies Used

* **Core Programming Language:** Python 3.x
* **Web Framework:** Flask
* **Data Processing & Storage:** Pandas, SQLite
* **AI/ML Components:** Logistic regression (scikit-learn), Generative AI (conceptual)
* **Version Control:** Git

## Getting Started

Follow these steps to set up and run CARE Lite:

### Prerequisites

* Python 3.x installed on your system.
* pip package installer.

### Installation

1.  Clone the repository:
    ```bash
    git clone [Your GitHub Repository Link]
    cd CARE_Lite
    ```

2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You might need to create a `requirements.txt` file with the necessary dependencies: `Flask`, `pandas`, `scikit-learn`)*

### Dataset Setup

1.  Place your `customer_data_collection.csv` and `product_recommendation_data.csv` files in the `data/` directory.
2.  **Crucially, within the `data/customer_data_collection.csv` file or in a configuration setting, specify whether the data is a real-world sample or synthetic.** This information is important for understanding the context of the recommendations.

### Running the Application

1.  Navigate to the project root directory.
2.  Run the Flask application:
    ```bash
    python main.py
    ```
    *(Note: Ensure `main.py` contains the Flask application setup.)*

The API should now be running (likely on `http://127.0.0.1:5000/` by default). Refer to the `main.py` file for available API endpoints.

## Code Structure

CARE_Lite/
├── main.py                   # Flask API entry point
├── agents/
│   ├── init.py
│   ├── data_extraction.py    # DataExtractionAgent
│   ├── rule_recommender.py   # RuleBasedRecommendationAgent
│   └── feedback_agent.py     # FeedbackIntegrationAgent
├── database/
│   ├── init.py
│   ├── db_interface.py       # Manages SQLite interactions
│   └── init_db.py            # Initializes the database
├── data/
│   ├── customer_data_collection.csv  # Customer dataset (specify if real or synthetic)
│   └── product_recommendation_data.csv  # Product dataset
└── utils/
└── helpers.py            # Utility functions


## Usage

The `main.py` file likely exposes a RESTful API. You can interact with it to get product recommendations. Example (conceptual):

Send a GET request to an endpoint like `/recommendations/<user_id>` to retrieve personalized product recommendations for a specific user. The API will utilize the agents to process data and generate the recommendations based on the defined logic.

*(Note: The specific API endpoints and request/response formats will depend on the implementation in `main.py`.)*

## Future Enhancements

* Implement the Merchant Dashboard for real-time monitoring and manual rule adjustments.
* Migrate from SQLite to cloud-hosted databases (e.g., PostgreSQL, NoSQL) for improved scalability and performance.
* Expand the agent framework to handle more complex recommendation scenarios.
* Integrate advanced generative AI techniques via prompt engineering to suggest dynamic rule modifications based on evolving user trends.
* Extend CARE Lite to cover multi-channel customer interactions.
* Develop more sophisticated machine learning models for the Feedback Integration Agent.

## Contributing

[Optional: Add information about how others can contribute to the project.]

## License

[Optional: Add license information here.]

## Acknowledgements

Thank you to the organizers and mentors of the Hack the Future: A Gen AI Sprint Powe
