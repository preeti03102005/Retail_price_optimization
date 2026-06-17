import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import database
import config

def train_and_evaluate_models():
    """
    Trains Linear Regression and Decision Tree on Products data.
    Saves the best model based on R2 score.
    Returns (success_bool, results_dict, best_model_name)
    """
    conn = database.get_connection()
    try:
        df = pd.read_sql("SELECT CostPrice, CompetitorPrice, QuantitySold, Category, SellingPrice FROM Products", conn)
    except Exception as e:
        return False, str(e), None
    finally:
        conn.close()
        
    if len(df) < 5:
        return False, "Not enough products in database to train models. Need at least 5 products.", None
        
    feature_cols = ['CostPrice', 'CompetitorPrice', 'QuantitySold', 'Category']
    target_col = 'SellingPrice'
    
    X = df[feature_cols].copy()
    y = df[target_col].copy()
    
    # Encode Category
    le = LabelEncoder()
    X['Category'] = le.fit_transform(X['Category'].astype(str))
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(max_depth=6, random_state=42)
    }
    
    results = {}
    best_name = None
    best_r2 = -float('inf')
    best_model_obj = None
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        
        mae = float(mean_absolute_error(y_test, preds))
        rmse = float(np.sqrt(mean_squared_error(y_test, preds)))
        r2 = float(r2_score(y_test, preds))
        
        results[name] = {
            "MAE": round(mae, 4),
            "RMSE": round(rmse, 4),
            "R2": round(r2, 4)
        }
        
        if r2 > best_r2:
            best_r2 = r2
            best_name = name
            best_model_obj = model
            
    # Save best model meta
    best_model_meta = {
        "model_name": best_name,
        "model": best_model_obj,
        "encoder": le,
        "feature_cols": feature_cols,
        "metrics": results[best_name],
        "all_results": results
    }
    
    model_path = os.path.join(config.MODELS_DIR, "best_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(best_model_meta, f)
        
    return True, results, best_name

def get_best_model():
    """Loads the best model from disk."""
    model_path = os.path.join(config.MODELS_DIR, "best_model.pkl")
    if not os.path.exists(model_path):
        return None
    with open(model_path, "rb") as f:
        return pickle.load(f)

def predict_selling_price(cost_price, competitor_price, quantity_sold, category):
    """Predicts optimal selling price using the saved ML model."""
    meta = get_best_model()
    if not meta:
        # Heuristic fallback if model not trained
        return (cost_price * 1.15 + competitor_price) / 2
        
    model = meta["model"]
    le = meta["encoder"]
    
    # Prep inputs
    input_data = pd.DataFrame([{
        "CostPrice": float(cost_price),
        "CompetitorPrice": float(competitor_price),
        "QuantitySold": int(quantity_sold),
        "Category": str(category)
    }])
    
    # Handle category encoding
    cat_val = input_data["Category"].iloc[0]
    if cat_val in le.classes_:
        input_data["Category"] = le.transform([cat_val])
    else:
        input_data["Category"] = 0
        
    # Reorder columns
    input_df = input_data[meta["feature_cols"]]
    predicted_val = float(model.predict(input_df)[0])
    
    # Constraints: cannot be below CostPrice
    if predicted_val < cost_price:
        predicted_val = cost_price * 1.05
        
    return predicted_val
