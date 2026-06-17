import os
import tempfile
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView, QMessageBox, QFrame, QGridLayout, QSplitter
)
from PyQt5.QtCore import Qt, QUrl

try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False

import database
import config
from predictor import predict_selling_price

def run_price_optimization_logic(product_id, current_price, cost_price, competitor_price, base_demand, category):
    """
    Simulates price elasticities and returns recommendations.
    """
    # Use ML predicted price as optimal starting point
    ml_base_price = predict_selling_price(cost_price, competitor_price, base_demand, category)
    
    # Simulate prices from -20% to +20% around ml_base_price
    center_price = ml_base_price if ml_base_price > 0 else current_price
    price_steps = np.linspace(center_price * 0.8, center_price * 1.2, 9)
    price_steps = np.unique(np.round(np.append(price_steps, [current_price, competitor_price]), 2))
    price_steps.sort()
    
    k = 1.5 # Price elasticity factor
    simulation_results = []
    best_profit = -float('inf')
    best_scenario = None
    
    for price in price_steps:
        if price < cost_price:
            continue
            
        # Elasticity formula
        price_ratio = (price - competitor_price) / competitor_price if competitor_price > 0 else 0
        sim_demand = base_demand * math.exp(-k * price_ratio)
        sim_demand = max(0, int(round(sim_demand)))
        
        sim_revenue = price * sim_demand
        sim_profit = (price - cost_price) * sim_demand
        
        scenario = {
            "price": float(price),
            "demand": int(sim_demand),
            "revenue": float(sim_revenue),
            "profit": float(sim_profit)
        }
        simulation_results.append(scenario)
        
        if sim_profit > best_profit:
            best_profit = sim_profit
            best_scenario = scenario
            
    if not best_scenario:
        best_scenario = {
            "price": current_price,
            "demand": base_demand,
            "revenue": current_price * base_demand,
            "profit": (current_price - cost_price) * base_demand
        }
        
    return {
        "recommended_price": best_scenario["price"],
        "expected_demand": best_scenario["demand"],
        "expected_revenue": best_scenario["revenue"],
        "expected_profit": best_scenario["profit"],
        "simulation_data": simulation_results
    }

def save_prediction_log(product_id, current_price, recommended_price, expected_demand, expected_revenue, expected_profit):
    """Saves predictions in database."""
    conn = database.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO Predictions (ProductID, CurrentPrice, RecommendedPrice, ExpectedDemand, ExpectedRevenue, ExpectedProfit, PredictionDate)
            VALUES (?, ?, ?, ?, ?, ?, GETDATE())
            """,
            (product_id, current_price, recommended_price, expected_demand, expected_revenue, expected_profit)
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error saving prediction log: {e}")
        return False
    finally:
        conn.close()


class PriceOptimizationView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.temp_files = []
        self.current_results = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        title_label = QLabel("Price Optimization & Simulation")
        title_label.setObjectName("HeaderTitle")
        layout.addWidget(title_label)
        layout.addSpacing(10)
        
        splitter = QSplitter(Qt.Horizontal)
        
        # Left Panel (Inputs)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        form_frame = QFrame()
        form_frame.setProperty("class", "Card")
        form_layout = QGridLayout(form_frame)
        
        form_layout.addWidget(QLabel("<b>Parameters Input</b>"), 0, 0, 1, 2)
        
        form_layout.addWidget(QLabel("Product:"), 1, 0)
        self.product_selector = QComboBox()
        self.load_products()
        self.product_selector.currentIndexChanged.connect(self.autofill_details)
        form_layout.addWidget(self.product_selector, 1, 1)
        
        form_layout.addWidget(QLabel("Current Price (₹):"), 2, 0)
        self.curr_price_input = QLineEdit()
        form_layout.addWidget(self.curr_price_input, 2, 1)
        
        form_layout.addWidget(QLabel("Cost Price (₹):"), 3, 0)
        self.cost_price_input = QLineEdit()
        form_layout.addWidget(self.cost_price_input, 3, 1)
        
        form_layout.addWidget(QLabel("Competitor Price (₹):"), 4, 0)
        self.comp_price_input = QLineEdit()
        form_layout.addWidget(self.comp_price_input, 4, 1)
        
        form_layout.addWidget(QLabel("Current Quantity Sold:"), 5, 0)
        self.demand_input = QLineEdit()
        form_layout.addWidget(self.demand_input, 5, 1)
        
        form_layout.addWidget(QLabel("Category:"), 6, 0)
        self.cat_input = QLineEdit()
        form_layout.addWidget(self.cat_input, 6, 1)
        
        optimize_btn = QPushButton("Calculate Best Price")
        optimize_btn.clicked.connect(self.run_optimization)
        form_layout.addWidget(optimize_btn, 7, 0, 1, 2)
        
        save_btn = QPushButton("Save Prediction Log")
        save_btn.setObjectName("SecondaryButton")
        save_btn.clicked.connect(self.save_prediction)
        form_layout.addWidget(save_btn, 8, 0, 1, 2)
        
        left_layout.addWidget(form_frame)
        left_layout.addStretch()
        splitter.addWidget(left_widget)
        
        # Right Panel (Outputs)
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # KPI Grid
        self.kpi_grid = QGridLayout()
        self.kpi_grid.setSpacing(10)
        
        def create_kpi_card(title, value, row, col):
            card = QFrame()
            card.setProperty("class", "KPICard")
            c_layout = QVBoxLayout(card)
            val_lbl = QLabel(value)
            val_lbl.setObjectName("MetricVal")
            val_lbl.setAlignment(Qt.AlignCenter)
            title_lbl = QLabel(title)
            title_lbl.setObjectName("MetricTitle")
            title_lbl.setAlignment(Qt.AlignCenter)
            c_layout.addWidget(val_lbl)
            c_layout.addWidget(title_lbl)
            self.kpi_grid.addWidget(card, row, col)
            return val_lbl
            
        self.kpi_curr = create_kpi_card("Current Price", "-", 0, 0)
        self.kpi_rec = create_kpi_card("Recommended Price", "-", 0, 1)
        self.kpi_demand = create_kpi_card("Expected Demand", "-", 0, 2)
        self.kpi_rev = create_kpi_card("Expected Revenue", "-", 1, 0)
        self.kpi_profit = create_kpi_card("Expected Profit", "-", 1, 1)
        
        right_layout.addLayout(self.kpi_grid)
        
        # Chart Frame
        self.chart_frame = QFrame()
        self.chart_frame.setProperty("class", "Card")
        self.chart_layout = QVBoxLayout(self.chart_frame)
        self.chart_layout.addWidget(QLabel("<b>Revenue & Profit Simulation Projections</b>"))
        
        if WEBENGINE_AVAILABLE:
            self.web_view = QWebEngineView()
            self.web_view.setMinimumHeight(240)
            
            # Configure settings to enable local content features
            settings = self.web_view.settings()
            settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
            settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
            
            self.chart_layout.addWidget(self.web_view)
        else:
            self.fallback = QLabel("Chart Engine fallback. Simulation details listed in table below.")
            self.chart_layout.addWidget(self.fallback)
            
        right_layout.addWidget(self.chart_frame)
        
        # Data Grid Table
        right_layout.addWidget(QLabel("<b>Simulation Scenarios</b>"))
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Price (₹)", "Demand (Units)", "Revenue (₹)", "Profit (₹)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setMaximumHeight(150)
        right_layout.addWidget(self.table)
        
        splitter.addWidget(right_widget)
        splitter.setSizes([300, 600])
        layout.addWidget(splitter)
        
        self.autofill_details()
        
    def load_products(self):
        try:
            conn = database.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT ProductID, ProductName FROM Products ORDER BY ProductName")
            rows = cursor.fetchall()
            conn.close()
            
            for row in rows:
                self.product_selector.addItem(row[1], userData=row[0])
        except Exception as e:
            print(f"Error loading products in optimizer: {e}")

    def autofill_details(self):
        p_idx = self.product_selector.currentIndex()
        if p_idx < 0:
            return
            
        product_id = self.product_selector.currentData()
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                SELECT SellingPrice, CostPrice, CompetitorPrice, QuantitySold, Category
                FROM Products
                WHERE ProductID = ?
                """,
                (product_id,)
            )
            row = cursor.fetchone()
            if row:
                self.curr_price_input.setText(str(row[0]))
                self.cost_price_input.setText(str(row[1]))
                self.comp_price_input.setText(str(row[2]))
                self.demand_input.setText(str(row[3]))
                self.cat_input.setText(str(row[4]))
        except Exception as e:
            print(f"Error autofilling: {e}")
        finally:
            conn.close()

    def run_optimization(self):
        p_idx = self.product_selector.currentIndex()
        if p_idx < 0:
            return
            
        product_id = self.product_selector.currentData()
        
        try:
            curr_p = float(self.curr_price_input.text())
            cost_p = float(self.cost_price_input.text())
            comp_p = float(self.comp_price_input.text())
            demand = int(self.demand_input.text())
            cat = self.cat_input.text().strip()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Verify prices and quantity fields are numeric values.")
            return
            
        self.current_results = run_price_optimization_logic(product_id, curr_p, cost_p, comp_p, demand, cat)
        res = self.current_results
        
        # Populate Scorecard
        self.kpi_curr.setText(f"₹{curr_p:,.2f}")
        self.kpi_rec.setText(f"₹{res['recommended_price']:,.2f}")
        self.kpi_demand.setText(f"{res['expected_demand']:,}")
        self.kpi_rev.setText(f"₹{res['expected_revenue']:,.2f}")
        self.kpi_profit.setText(f"₹{res['expected_profit']:,.2f}")
        
        # Populate Table
        sim_data = res["simulation_data"]
        self.table.setRowCount(0)
        
        prices = []
        revenues = []
        profits = []
        
        for row in sim_data:
            r_idx = self.table.rowCount()
            self.table.insertRow(r_idx)
            
            p = row["price"]
            d = row["demand"]
            rev = row["revenue"]
            prof = row["profit"]
            
            prices.append(p)
            revenues.append(rev)
            profits.append(prof)
            
            self.table.setItem(r_idx, 0, QTableWidgetItem(f"₹{p:.2f}"))
            self.table.setItem(r_idx, 1, QTableWidgetItem(f"{d:,}"))
            self.table.setItem(r_idx, 2, QTableWidgetItem(f"₹{rev:,.2f}"))
            self.table.setItem(r_idx, 3, QTableWidgetItem(f"₹{prof:,.2f}"))
            
            if p == res["recommended_price"]:
                for c in range(4):
                    self.table.item(r_idx, c).setBackground(Qt.green)
                    
        # Render plot
        if WEBENGINE_AVAILABLE:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=prices, y=revenues, mode='lines+markers', name='Revenue (₹)', line=dict(color='#3F51B5', width=2)))
            fig.add_trace(go.Scatter(x=prices, y=profits, mode='lines+markers', name='Profit (₹)', line=dict(color='#EF4444', width=2)))
            fig.add_vline(x=res["recommended_price"], line_dash="dash", line_color="green", annotation_text=f"Optimal: ₹{res['recommended_price']:.2f}")
            fig.update_layout(title="Optimization Simulation curves", xaxis_title="Price Point (₹)", yaxis_title="Value (₹)", template="plotly_white")
            
            temp_dir = config.TEMP_DIR
            temp_path = os.path.join(temp_dir, f"opt_sim_chart_{len(self.temp_files)}.html")
            # Generate HTML string first and replace :focus-visible CSS rules to support older Chromium engines in PyQtWebEngine
            html_content = fig.to_html(include_plotlyjs=True)
            html_content = html_content.replace(":focus-visible", ":focus")
            
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            self.temp_files.append(temp_path)
            
            try:
                # Use setUrl with fromLocalFile for superior performance and local execution stability
                self.web_view.setUrl(QUrl.fromLocalFile(temp_path))
            except Exception as e:
                print(f"Error loading HTML into web_view: {e}")

    def save_prediction(self):
        if not self.current_results:
            QMessageBox.warning(self, "Calculate First", "Please run optimization calculation first.")
            return
            
        product_id = self.product_selector.currentData()
        curr_p = float(self.curr_price_input.text())
        res = self.current_results
        
        success = save_prediction_log(
            product_id, curr_p, res["recommended_price"], 
            res["expected_demand"], res["expected_revenue"], res["expected_profit"]
        )
        
        if success:
            QMessageBox.information(self, "Saved", "Prediction logs saved to Predictions table successfully.")
        else:
            QMessageBox.critical(self, "Error", "Failed to save prediction log to database.")

    def closeEvent(self, event):
        for f in self.temp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass
        event.accept()
