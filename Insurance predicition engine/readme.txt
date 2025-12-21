#  Healthcare Risk Engine: Predictive Cost Modeling

###  Overview
This project focuses on building a machine learning pipeline to predict individual medical insurance costs based on demographic and health factors. By leveraging historical patient data, the model identifies key cost drivers and provides accurate risk assessments for new patients.

**Goal:** Transform raw data into an actionable pricing engine using Supervised Learning.

###  Tech Stack
* **Language:** Python
* **Libraries:** Pandas, NumPy, Scikit-Learn, Matplotlib, Seaborn
* **Techniques:** Exploratory Data Analysis (EDA), Feature Engineering (One-Hot Encoding), Regression Modeling.

### Key Results
We compared two modeling approaches to determine the best predictor for insurance charges:

| Model | R² Score (Accuracy) | RMSE (Avg Error) | Verdict |
| :--- | :--- | :--- | :--- |
| **Linear Regression** | 0.8069 | ~$5,956 | Good baseline, but missed non-linear patterns. |
| **Random Forest** | **0.8798** | **~$4,700** | **Winner.** Captures complex interactions (e.g., Age + Smoker). |

**Top Cost Drivers Identified:**
1.  **Smoker Status:** The single strongest predictor of high costs.
2.  **BMI:** Correlation with cost increases significantly for smokers.
3.  **Age:** Linear increase in base costs over time.

###  Usage
The project includes an interactive predictor function that allows users to input raw data and receive an immediate cost estimate.

```python
# Example Usage
cost = predict_my_cost(
    age=30,
    sex='male',
    bmi=25.5,
    children=0,
    smoker='yes',
    region='southwest'
)
print(f"Estimated Bill: ${cost}")