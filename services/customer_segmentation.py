
from database.db_connection import create_connection


def get_customer_purchase_summary():

    connection = create_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                c.customer_id,
                c.customer_name,
                c.email,
                c.city,

                MAX(o.order_date) AS last_order_date,

                COUNT(o.order_id) AS total_orders,

                COALESCE(SUM(o.total_amount), 0) AS total_spent,

                DATEDIFF(CURDATE(), MAX(o.order_date)) AS recency_days

            FROM customers c

            LEFT JOIN orders o
                ON c.customer_id = o.customer_id
                AND o.order_status != 'Cancelled'

            WHERE c.is_deleted = 0

            GROUP BY
                c.customer_id,
                c.customer_name,
                c.email,
                c.city

            ORDER BY total_spent DESC
        """

        cursor.execute(query)

        results = cursor.fetchall()

        return results

    except Exception as e:

        print("Customer Analytics Error:", e)

        return []

    finally:

        cursor.close()
        connection.close()

import pandas as pd


def get_rfm_customer_segments():

    customers = get_customer_purchase_summary()

    if not customers:
        return pd.DataFrame()

    df = pd.DataFrame(customers)

    # Customers without purchases are not included in RFM scoring
    rfm = df[
        (df["total_orders"] > 0) &
        (df["total_spent"] > 0) &
        (df["recency_days"].notna())
    ].copy()

    if len(rfm) < 4:
        print("At least 4 purchasing customers are required for RFM scoring.")
        return pd.DataFrame()

    # Calculate RFM scores from 1 to 4
    # Recency: fewer days means a higher score
    rfm["R_score"] = pd.qcut(
        rfm["recency_days"].rank(method="first"),
        4,
        labels=[4, 3, 2, 1]
    ).astype(int)

    # Frequency: more orders means a higher score
    rfm["F_score"] = pd.qcut(
        rfm["total_orders"].rank(method="first"),
        4,
        labels=[1, 2, 3, 4]
    ).astype(int)

    # Monetary: higher spending means a higher score
    rfm["M_score"] = pd.qcut(
        rfm["total_spent"].rank(method="first"),
        4,
        labels=[1, 2, 3, 4]
    ).astype(int)

    # Combine the three scores
    rfm["RFM_score"] = (
        rfm["R_score"].astype(str) +
        rfm["F_score"].astype(str) +
        rfm["M_score"].astype(str)
    )

    # Assign customer segments
    def assign_segment(row):

        r = row["R_score"]
        f = row["F_score"]
        m = row["M_score"]

        if r >= 3 and f >= 3 and m >= 3:
            return "Champions"

        elif f >= 3:
            return "Loyal Customers"

        elif m >= 3:
            return "Big Spenders"

        elif r <= 2 and (f >= 3 or m >= 3):
            return "At Risk"

        elif r >= 3 and f >= 2:
            return "Potential Loyalists"

        elif r <= 2:
            return "Needs Attention"

        else:
            return "Regular Customers"

    rfm["customer_segment"] = rfm.apply(
        assign_segment,
        axis=1
    )

    return rfm


def get_customer_churn_risk():

    customers = get_customer_purchase_summary()

    if not customers:
        return pd.DataFrame()

    df = pd.DataFrame(customers)

    def calculate_risk(row):

        # Customers who have never purchased
        if row["total_orders"] == 0:
            return "No Purchase History"

        days = row["recency_days"]

        if pd.isna(days):
            return "No Purchase History"

        if days > 90:
            return "High Risk"

        elif days > 60:
            return "Medium Risk"

        else:
            return "Low Risk"

    df["churn_risk"] = df.apply(
        calculate_risk,
        axis=1
    )

    return df[
        [
            "customer_id",
            "customer_name",
            "email",
            "city",
            "total_orders",
            "total_spent",
            "recency_days",
            "churn_risk"
        ]
    ]

