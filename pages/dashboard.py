import streamlit as st
import pandas as pd
from db import run_query, run_scalar

def show():
    st.markdown("# Dashboard")
    st.markdown("Welcome to **MediTrack Pro**  your complete pharmacy management system.")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    total_patients  = run_scalar("SELECT COUNT(*) FROM Patient")
    pending_rx      = run_scalar("SELECT COUNT(*) FROM Prescription WHERE Status = 'Pending'")
    low_stock       = run_scalar("SELECT COUNT(*) FROM Medicine WHERE StockQty < ReorderLevel")
    pending_orders  = run_scalar("SELECT COUNT(*) FROM Supply_Order WHERE Status = 'Ordered'")

    with col1:
        st.metric("Total Patients",          total_patients)
    with col2:
        st.metric("Pending Prescriptions",   pending_rx)
    with col3:
        st.metric("Low Stock Medicines",     low_stock)
    with col4:
        st.metric("Pending Orders",           pending_orders)

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("###  Recent Prescriptions")
        result = run_query("""
            SELECT TOP 5
                p.PrescriptionID,
                pt.FirstName + ' ' + pt.LastName AS Patient,
                p.Diagnosis,
                p.Status,
                CAST(p.PrescriptionDate AS VARCHAR) AS Date
            FROM Prescription p, Patient pt
            WHERE p.PatientID = pt.PatientID
            ORDER BY p.PrescriptionDate DESC
        """)
        if result:
            cols, rows = result
            df = pd.DataFrame(rows, columns=cols)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No prescriptions yet.")

    with col_right:
        st.markdown("### Low Stock Alert")
        result = run_query("""
            SELECT MedicineName, StockQty, ReorderLevel,
                   CASE
                       WHEN StockQty = 0 THEN 'Out of Stock'
                       ELSE 'Low Stock'
                   END AS Status
            FROM Medicine
            WHERE StockQty < ReorderLevel
        """)
        if result:
            cols, rows = result
            df = pd.DataFrame(rows, columns=cols)
            if len(df) == 0:
                st.markdown(
                    "<div class='success-box'> All medicines are well stocked!</div>",
                    unsafe_allow_html=True
                )
            else:
                for _, row in df.iterrows():
                    color = "danger-box" if row['Status'] == 'Out of Stock' else "warning-box"
                    st.markdown(
                        f"<div class='{color}'>"
                        f"<b>{row['MedicineName']}</b> — "
                        f"Stock: {row['StockQty']} / Reorder at: {row['ReorderLevel']}"
                        f"</div>",
                        unsafe_allow_html=True
                    )
        else:
            st.markdown(
                "<div class='success-box'> All medicines are well stocked!</div>",
                unsafe_allow_html=True
            )

    st.markdown("---")

  
    st.markdown("###  Medicine Stock Overview")
    result = run_query("""
        SELECT
            MedicineName,
            Category,
            StockQty,
            ReorderLevel,
            CASE
                WHEN StockQty = 0 THEN 'Out of Stock'
                WHEN StockQty < ReorderLevel THEN 'Low Stock'
                ELSE 'Available'
            END AS StockStatus
        FROM Medicine
        ORDER BY StockQty ASC
    """)
    if result:
        cols, rows = result
        df = pd.DataFrame(rows, columns=cols)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No medicines found.")