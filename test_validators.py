
from services.customer_segmentation import get_customer_churn_risk

df = get_customer_churn_risk()

print("\n--- CUSTOMER CHURN RISK ANALYSIS ---")

if not df.empty:

    print(
        df[
            [
                "customer_name",
                "total_orders",
                "recency_days",
                "churn_risk"
            ]
        ].to_string(index=False)
    )

    print("\n--- CHURN RISK SUMMARY ---")

    print(df["churn_risk"].value_counts())

else:
    print("No customer data available.")
