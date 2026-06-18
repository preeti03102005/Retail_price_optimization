# Retail Price Optimization Platform

## Overview

The Retail Price Optimization Platform is a machine learning-based application designed to help retailers determine the optimal selling price for their products. By analyzing historical sales data, the system predicts demand, revenue, and profit at different price points and recommends the price that can maximize profit.

## Features

* User Authentication (Login System)
* Sales Data Import (CSV/Excel)
* Data Processing and Storage
* Interactive Dashboard
* Sales Analytics and Visualizations
* Machine Learning-Based Predictions
* Price Optimization Engine
* Revenue and Profit Analysis
* Report Generation and Export

## Technology Stack

### Frontend / User Interface

* PyQt5

### Backend

* Python

### Database

* SQL Server / SQLite

### Machine Learning Libraries

* Scikit-learn
* Pandas
* NumPy

### Data Visualization

* Matplotlib
* Seaborn

## Project Workflow

1. User logs into the application.
2. Sales data is uploaded through CSV or Excel files.
3. The system processes and stores the data.
4. Historical sales data is analyzed using machine learning models.
5. Different price values are evaluated.
6. Expected demand, revenue, and profit are calculated.
7. The system recommends the optimal price that maximizes profit.
8. Results are displayed through dashboards, charts, and reports.

## Machine Learning Approach

The machine learning model learns patterns from historical sales data and predicts how customer demand changes with different prices. Based on these predictions, the platform identifies the most profitable selling price.

## Installation

```bash
git clone https://github.com/preeti03102005/Retail_price_optimization.git

cd Retail-Price-Optimization

pip install -r requirements.txt

python main.py
```

## Usage

1. Launch the application.
2. Login to the system.
3. Upload a sales dataset.
4. View analytics and visualizations.
5. Run price optimization.
6. Review the recommended price and generated reports.

## Future Enhancements

* Real-time pricing recommendations
* Cloud deployment
* Advanced forecasting models
* Multi-user access control
* Web-based version using Flask/Django

## Author

Developed as an academic project for Retail Price Optimization using Machine Learning and Data Analytics.
