# Modern QSS Styling sheets for Retail Price Optimization
# Indigo, Violet, and Ocean Blue/Cyan theme

LIGHT_THEME = """
QMainWindow {
    background-color: #F8FAFC;
}

QFrame#SidebarFrame {
    background-color: #0F172A;
    border: none;
    min-width: 240px;
    max-width: 240px;
}

QFrame#SidebarFrame QPushButton {
    background-color: transparent;
    color: #94A3B8;
    border: none;
    border-radius: 6px;
    padding: 12px 16px;
    text-align: left;
    font-size: 11pt;
    font-weight: 500;
}

QFrame#SidebarFrame QPushButton:hover {
    background-color: #1E293B;
    color: #FFFFFF;
}

QFrame.Card {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
}

QFrame.KPICard {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
}

QFrame.KPICard QLabel#MetricVal {
    font-size: 18pt;
    font-weight: bold;
    color: #4F46E5;
}

QFrame.KPICard QLabel#MetricTitle {
    font-size: 9pt;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
}

QFrame#MainContainer {
    background-color: #F8FAFC;
}

QLineEdit, QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #D1D5DB;
    border-radius: 6px;
    padding: 8px 12px;
    color: #1F2937;
    font-size: 10pt;
}

QPushButton {
    background-color: #4F46E5;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 10pt;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #4338CA;
}

QPushButton#SecondaryButton {
    background-color: #F1F5F9;
    color: #475569;
}

QPushButton#SecondaryButton:hover {
    background-color: #E2E8F0;
}

QPushButton#ThemeToggle {
    background-color: transparent;
    border: 1px solid #CBD5E1;
    color: #475569;
    border-radius: 15px;
    padding: 4px;
    margin-bottom: 10px;
}

QLabel#HeaderTitle {
    font-size: 18pt;
    font-weight: bold;
    color: #0F172A;
}

QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    gridline-color: #E2E8F0;
    font-size: 10pt;
    color: #334155;
}

QHeaderView::section {
    background-color: #F8FAFC;
    color: #475569;
    padding: 8px;
    border: none;
    border-bottom: 2px solid #E2E8F0;
    font-weight: bold;
}
"""

DARK_THEME = """
QMainWindow {
    background-color: #030712;
}

QFrame#SidebarFrame {
    background-color: #0B0F19;
    border: none;
    min-width: 240px;
    max-width: 240px;
}

QFrame#SidebarFrame QPushButton {
    background-color: transparent;
    color: #94A3B8;
    border: none;
    border-radius: 6px;
    padding: 12px 16px;
    text-align: left;
    font-size: 11pt;
    font-weight: 500;
}

QFrame#SidebarFrame QPushButton:hover {
    background-color: #1E293B;
    color: #FFFFFF;
}

QFrame.Card {
    background-color: #0B0F19;
    border: 1px solid #1E293B;
    border-radius: 12px;
}

QFrame.KPICard {
    background-color: #0B0F19;
    border: 1px solid #1E293B;
    border-radius: 12px;
}

QFrame.KPICard QLabel#MetricVal {
    font-size: 18pt;
    font-weight: bold;
    color: #818CF8;
}

QFrame.KPICard QLabel#MetricTitle {
    font-size: 9pt;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
}

QFrame#MainContainer {
    background-color: #030712;
}

QLineEdit, QComboBox {
    background-color: #0B0F19;
    border: 1px solid #1E293B;
    border-radius: 6px;
    padding: 8px 12px;
    color: #F9FAFB;
    font-size: 10pt;
}

QPushButton {
    background-color: #6366F1;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    font-size: 10pt;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #4F46E5;
}

QPushButton#SecondaryButton {
    background-color: #1F2937;
    color: #E5E7EB;
}

QPushButton#SecondaryButton:hover {
    background-color: #374151;
}

QPushButton#ThemeToggle {
    background-color: transparent;
    border: 1px solid #1E293B;
    color: #94A3B8;
    border-radius: 15px;
    padding: 4px;
    margin-bottom: 10px;
}

QLabel#HeaderTitle {
    font-size: 18pt;
    font-weight: bold;
    color: #F9FAFB;
}

QTableWidget {
    background-color: #0B0F19;
    border: 1px solid #1E293B;
    border-radius: 8px;
    gridline-color: #1E293B;
    font-size: 10pt;
    color: #E5E7EB;
}

QHeaderView::section {
    background-color: #030712;
    color: #9CA3AF;
    padding: 8px;
    border: none;
    border-bottom: 2px solid #1F2937;
    font-weight: bold;
}
"""
