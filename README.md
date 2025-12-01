

**Tolgo Revenue Forecasting – ARIMA Model Project**

==============================================



**Project Overview**

----------------

Tolgo Revenue Forecasting is a complete end-to-end analytics pipeline simulating how a fintech startup monitors, models, and forecasts its Monthly Recurring Revenue (MRR).  

The project includes:



\- Synthetic dataset generation (2021–2024)

\- Trend and churn analysis

\- ARIMA time-series forecasting over 12 months

\- Confidence interval calculations

\- Exportable results

\- A well-documented Jupyter Notebook that walks through the full analysis



**Repository Structure**

--------------------

Tolgo-Forecasting/

│

├── Data/

│     ├── tolgo\_revenue\_history.csv

│     ├── forecast\_output.csv

│

├── Scripts/

│     ├── generate\_forecast\_dataset.py

│     ├── forecast\_mrr.py

│

├── notebooks/

│     ├── Tolgo\_Revenue\_Forecasting.ipynb

│

└── README.md



**Dataset Description**

-------------------

The dataset simulates 48 months of fintech subscription metrics:



\- month: Monthly timestamp

\- active\_users: Number of active paying subscribers

\- arpu: Average revenue per user

\- mrr: Monthly recurring revenue

\- total\_revenue: Total revenue including one-offs

\- churn\_rate: Monthly churn rate

\- mrr\_growth\_rate: MRR evolution month-over-month

\- plan\_light\_share, plan\_standard\_share, plan\_premium\_share: Plan distribution



**Modeling Approach**

-----------------

\*\*ARIMA (SARIMAX)\*\* is used for forecasting MRR:

\- Order (p,d,q) = (1,1,1)

\- Seasonal order = (1,1,1,12)

\- 12-month prediction horizon

\- Confidence intervals provided



Prophet is included as an optional model if available, but ARIMA is the primary model.



**How to Run the Project**

----------------------

1\. Generate the dataset

```

python Scripts/generate\_forecast\_dataset.py

```



2\. Run the forecasting model

```

python Scripts/forecast\_mrr.py

```



3\. Open the analysis notebook

```

jupyter notebook notebooks/Tolgo\_Revenue\_Forecasting.ipynb

```



**Key Insights (Summary)**

----------------------

\### 1. Strong MRR Growth

\- MRR increases steadily during 2021–2024.

\- ARIMA forecasts continued growth.

\- Predicted MRR reaches ~530,000 FCFA by the end of the forecast window.



\### 2. Expansion of User Base

\- Active users grow consistently across the dataset.



\### 3. Declining Churn Rate

\- Churn stabilizes around 4–5%, decreasing from ~6.5%.

\- Indicates improved retention.



\### 4. Model Stability

\- Confidence intervals are tight.

\- ARIMA provides a reliable and realistic forecast.



**Business Interpretation**

-----------------------

Tolgo exhibits a strong growth trajectory supported by:



\- Expanding user base  

\- Controlled churn  

\- Stable recurring revenue patterns  



This forecasting workflow resembles real analytics used in financial planning, risk teams, and subscription-based fintech models.



Author

**Fabel Sirpe**

Developed as part of Tolgo’s internal analytics tools and portfolio demonstration work.





