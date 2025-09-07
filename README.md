# 🛒 E-commerce Propensity Engine

An interactive dashboard powered by an XGBoost model to predict the propensity of product returns in e-commerce. This project helps e-commerce businesses identify which products are likely to be returned, enabling better inventory management, customer targeting, and return policy optimization.

---

## 🎯 The Problem

E-commerce businesses lose billions of dollars annually due to product returns. This process, known as "reverse logistics," involves significant costs in shipping, inspection, restocking, and potential product devaluation. Most companies manage this reactively, only acting after a return has already been initiated.

---

## 💡 The Solution: E-commerce Propensity Engine

E-commerce-Propensity-Engine is a proof-of-concept dashboard that shifts this strategy from reactive to proactive. By leveraging a machine learning model, this tool can predict the return probability for a transaction at the point of input, allowing a business to:

Identify High-Risk Orders: Flag transactions that are likely to be returned.

Make Proactive Interventions: Offer targeted discounts, trigger manual quality checks, or send personalized follow-ups to mitigate the risk.

Gain Business Insights: Understand the key drivers behind product returns.

---

## ✨ Features

- 🖥️ **Interactive Dashboard:** Visualizes model predictions and key metrics for product return propensity.
- 🤖 **XGBoost Model:** Uses advanced machine learning for accurate predictions.
- 🛍️ **E-commerce Focus:** Designed specifically for product return scenarios common in online retail.
- 📊 Interactive Inputs: Dynamic charts and a map that visually represent user-selected transaction data.
- 📈 Animated Results: A beautiful animated gauge chart displays the final prediction outcome, providing a premium user experience.
- 🗺️ High-Resolution Map: A detailed map of Europe that clearly highlights the selected country of purchase.

---

## 🛠️ Tech Stack

- Python  -> Core programming language
- Pandas  -> Data manipulation and analysis
- Scikit-learn  -> Data preprocessing (scaling)
- XGBoost  -> Machine learning model for classification
- Streamlit  -> Web application framework for the dashboard
- Plotly Express  -> Interactive charting and data visualization
- Git & GitHub  -> Version control and project hosting

---

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Aar2284/E-commerce-Propensity-Engine.git
   ```
2. **Install dependencies:**  
   Ensure you have Python and Jupyter Notebook installed.  
   Install required libraries using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Dashboard:**  
   Open the main notebook in Jupyter and follow the instructions to launch the dashboard.

---

## 🗂️ Project Structure

```
├── .streamlit/
│   └── config.toml             # Custom theme configuration
├── Model_Training_Notebook.ipynb # Jupyter Notebook for EDA and model training
├── app.py                      # Main Streamlit application script
├── europe.geojson              # High-resolution map data for Europe
├── model_columns.joblib        # List of model feature columns
├── return_prediction_model.joblib  # Trained XGBoost model
├── scaler.joblib               # Scikit-learn scaler
└── requirements.txt            # Python dependencies
```

---

## 🧠 How It Works

The XGBoost model is trained on historical e-commerce transaction data, including product details, customer information, and previous return history. The dashboard provides real-time insights into the likelihood of a product being returned after purchase.

---

## 🎯 Usage

- 📊 **Business Analysts:** Gain insights into product return risks.
- 🚚 **Operations Teams:** Optimize inventory and logistics based on predicted returns.
- 👨‍💻 **Developers:** Extend the dashboard or model for custom use cases.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request for suggestions and improvements.

---

## 📄 License

This project currently does not specify a license. Please contact the repository owner for usage permissions.

---

## 👤 Author

- [Aar2284](https://github.com/Aar2284)

---

For more information, visit the [project repository](https://github.com/Aar2284/E-commerce-Propensity-Engine).
