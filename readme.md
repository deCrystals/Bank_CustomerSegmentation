# Optimising Retail Banking Strategies Through RFM-Based Customer Segmentation

## Project Overview
**Click here**[Dashboard]https://bank-segmentation.streamlit.app/
This project implements a customer segmentation analysis for BankTrust based on RFM (Recency, Frequency, Monetary) methodology. The goal is to segment bank customers based on their transaction behaviors and develop targeted strategies to reduce churn, improve personalization, and optimize marketing efficiency.

## Features

- **RFM Analysis**: Segments customers based on recency, frequency, and monetary value of transactions
- **Customer Segmentation**: Creates meaningful customer segments with distinct characteristics
- **Targeted Strategies**: Provides tailored strategies for each customer segment
- **Interactive Dashboard**: Streamlit-powered dashboard for exploring customer segments and insights
  
## Dataset

The analysis uses a banking transaction dataset with the following structure:

- `TransactionID`: Unique identifier for each transaction
- `CustomerID`: Unique identifier for each customer
- `CustomerDOB`: Customer date of birth
- `CustGender`: Customer gender
- `CustLocation`: Customer location
- `CustAccountBalance`: Customer account balance in INR
- `TransactionDate`: Date of transaction
- `TransactionTime`: Time of transaction
- `TransactionAmount (INR)`: Transaction amount in Indian Rupees


## Installation

### Prerequisites

- Python 3.8+
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/deCrystals/Bank_CustomerSegmentation

```

2. Create a virtual environment and activate it:
```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Analysis Script

To perform the RFM analysis without the dashboard:

```bash
cd Notebook
python main.py
```

This will:
- Load and preprocess the transaction data
- Calculate RFM metrics
- Segment customers
- Generate analysis results
- Save the results to CSV files

### Running the Dashboard

To launch the interactive dashboard:

```bash
streamlit run app.py
```

This will start a local Streamlit server. Open your web browser and navigate to the provided URL (typically http://localhost:8501) to access the dashboard.

### Dashboard Sections

1. **Overview**: Shows key metrics and demographics
2. **Segment Analysis**: Detailed analysis of each customer segment
3. **Targeted Strategies**: Strategies for each customer segment


