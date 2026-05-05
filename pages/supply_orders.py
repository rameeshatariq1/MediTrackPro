import streamlit as st
import pandas as pd
from db import run_query, run_action

def show():
    st.markdown("# Supply Orders")
    st.markdown("---")

    tab1, tab2 = st.tabs(["  All Orders", "  Place New Order"])

    with tab1:
        st.markdown("### All Supply Orders")

        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Ordered", "Received", "Cancelled", "Partial"],
            key="so_status_filter"
        )

        if status_filter == "All":
            result = run_query("""
                SELECT so.OrderID,
                       s.SupplierName,
                       m.MedicineName,
                       so.OrderedQty,
                       so.UnitPrice,
                       CAST(so.OrderDate AS VARCHAR) AS OrderDate,
                       so.Status
                FROM Supply_Order so, Supplier s, Medicine m
                WHERE so.SupplierID = s.SupplierID
                AND   so.MedicineID = m.MedicineID
                ORDER BY so.OrderDate DESC
            """)
        else:
            result = run_query("""
                SELECT so.OrderID,
                       s.SupplierName,
                       m.MedicineName,
                       so.OrderedQty,
                       so.UnitPrice,
                       CAST(so.OrderDate AS VARCHAR) AS OrderDate,
                       so.Status
                FROM Supply_Order so, Supplier s, Medicine m
                WHERE so.SupplierID = s.SupplierID
                AND   so.MedicineID = m.MedicineID
                AND   so.Status = ?
                ORDER BY so.OrderDate DESC
            """, (status_filter,))

        if result:
            cols, rows = result
            df = pd.DataFrame(rows, columns=cols)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"Total: {len(df)} orders")
        else:
            st.info("No orders found.")

        st.markdown("---")
        st.markdown("### Mark Order as Received")
        col1, col2 = st.columns(2)
        with col1:
            order_id_update = st.number_input(
                "Order ID to Mark Received",
                min_value=1, step=1,
                key="so_receive_id"        
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Mark as Received", key="so_receive_btn"):
                ok = run_action("""
                    UPDATE Supply_Order SET Status = 'Received'
                    WHERE OrderID = ?
                """, (order_id_update,))
                if ok:
                    st.success(f"Order #{order_id_update} marked as Received!")

   
    with tab2:
        st.markdown("### Place New Supply Order")

        sup_result = run_query(
            "SELECT SupplierID, SupplierName FROM Supplier"
        )
        med_result = run_query(
            "SELECT MedicineID, MedicineName FROM Medicine"
        )

        if sup_result and med_result:
            sup_opts = {r[1]: r[0] for r in sup_result[1]}
            med_opts = {r[1]: r[0] for r in med_result[1]}

            col1, col2 = st.columns(2)
            with col1:
                order_id_new = st.number_input(
                    "Order ID",
                    min_value=1, step=1,
                    key="so_new_id"         
                )
                sel_sup      = st.selectbox(
                    "Select Supplier",
                    list(sup_opts.keys()),
                    key="so_new_supplier"
                )
                qty          = st.number_input(
                    "Quantity",
                    min_value=1, step=10,
                    key="so_new_qty"
                )
            with col2:
                sel_med      = st.selectbox(
                    "Select Medicine",
                    list(med_opts.keys()),
                    key="so_new_medicine"
                )
                price        = st.number_input(
                    "Unit Price (PKR)",
                    min_value=0.0, step=0.5,
                    key="so_new_price"
                )
                order_date   = st.date_input(
                    "Order Date",
                    key="so_new_date"
                )

            if st.button("🛒 Place Order", key="so_place_btn"):
                sup_id = sup_opts[sel_sup]
                med_id = med_opts[sel_med]
                ok = run_action("""
                    INSERT INTO Supply_Order
                    VALUES (?, ?, ?, ?, ?, ?, 'Ordered')
                """, (order_id_new, sup_id, med_id, qty, price, order_date))
                if ok:
                    st.success(f"Order #{order_id_new} placed successfully!")
                    st.balloons()
        else:
            st.warning("No suppliers or medicines found. Please add them first.")