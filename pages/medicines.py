import streamlit as st
import pandas as pd
from db import run_query, run_action

def show():
    st.markdown("#  Medicine Management")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([
        "All Medicines", "Add Medicine", " Update Stock"
    ])

    # ── Tab 1: View ───────────────────────────────────────────────────
    with tab1:
        st.markdown("### Medicine Catalogue")

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            search = st.text_input(" Search medicine name")
        with col_f2:
            category_filter = st.selectbox(
                "Filter by category",
                ["All", "Analgesic", "Antibiotic", "Antidiabetic",
                 "Antacid", "Statin", "Antihistamine"]
            )

        query = """
            SELECT MedicineID, MedicineName, Category, DosageForm,
                   UnitPrice, StockQty, ExpiryDate, ReorderLevel,
                   CASE
                       WHEN StockQty = 0 THEN 'Out of Stock'
                       WHEN StockQty < ReorderLevel THEN 'Low Stock'
                       ELSE 'Available'
                   END AS Status
            FROM Medicine WHERE 1=1
        """
        params = []
        if search:
            query  += " AND MedicineName LIKE ?"
            params.append(f'%{search}%')
        if category_filter != "All":
            query  += " AND Category = ?"
            params.append(category_filter)

        result = run_query(query, params if params else None)
        if result:
            cols, rows = result
            df = pd.DataFrame(rows, columns=cols)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"Showing {len(df)} medicines")

    with tab2:
        st.markdown("### Add New Medicine")
        col1, col2 = st.columns(2)
        with col1:
            med_id   = st.number_input("Medicine ID", min_value=1, step=1)
            med_name = st.text_input("Medicine Name")
            dosage_f = st.selectbox("Dosage Form",
                       ["Tablet","Capsule","Syrup","Injection","Cream","Drops"])
            stock    = st.number_input("Stock Quantity", min_value=0, step=1)
            expiry   = st.date_input("Expiry Date")
        with col2:
            category = st.selectbox("Category",
                       ["Analgesic","Antibiotic","Antidiabetic",
                        "Antacid","Statin","Antihistamine","Other"])
            price    = st.number_input("Unit Price (PKR)", min_value=0.0, step=0.5)
            reorder  = st.number_input("Reorder Level", min_value=0, step=5)

        if st.button("Add Medicine"):
            if med_name:
                ok = run_action("""
                    INSERT INTO Medicine
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (med_id, med_name, category, dosage_f,
                      price, stock, expiry, reorder))
                if ok:
                    st.success(f"{med_name} added successfully!")
                    st.balloons()
            else:
                st.warning("Please enter a medicine name.")

    with tab3:
        st.markdown("### Update Medicine Stock")

        result = run_query("SELECT MedicineID, MedicineName, StockQty FROM Medicine")
        if result:
            cols, rows = result
            options    = {f"{r[0]} — {r[1]} (Current: {r[2]})": r[0] for r in rows}
            selected   = st.selectbox("Select Medicine", list(options.keys()))
            med_id_sel = options[selected]
            qty_add    = st.number_input("Quantity to Add", min_value=1, step=1)
            notes      = st.text_input("Notes", placeholder="e.g. Received from supplier")

            if st.button("Update Stock"):
                ok1 = run_action("""
                    UPDATE Medicine SET StockQty = StockQty + ?
                    WHERE MedicineID = ?
                """, (qty_add, med_id_sel))

                log_id_result = run_query("SELECT MAX(LogID) FROM Inventory_Log")
                next_id = (log_id_result[1][0][0] or 0) + 1

                ok2 = run_action("""
                    INSERT INTO Inventory_Log
                    VALUES (?, ?, 'Restock', ?, GETDATE(), ?)
                """, (next_id, med_id_sel, qty_add, notes))

                if ok1 and ok2:
                    st.success(f"Stock updated! Added {qty_add} units.")