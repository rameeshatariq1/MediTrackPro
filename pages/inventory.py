import streamlit as st
import pandas as pd
from db import run_query

def show():
    st.markdown("# Inventory Log")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        type_filter = st.selectbox(
            "Filter by Transaction Type",
            ["All", "Restock", "Dispensed", "Damaged", "Expired", "Return"]
        )
    with col2:
        med_result = run_query("SELECT MedicineID, MedicineName FROM Medicine")
        if med_result:
            options = {"All Medicines": None}
            for r in med_result[1]:
                options[r[1]] = r[0]
            sel_med = st.selectbox("Filter by Medicine", list(options.keys()))

    query = """
        SELECT il.LogID, m.MedicineName, il.TransactionType,
               il.Quantity, il.LogDate, il.Notes
        FROM Inventory_Log il, Medicine m
        WHERE il.MedicineID = m.MedicineID
    """
    params = []
    if type_filter != "All":
        query += " AND il.TransactionType = ?"
        params.append(type_filter)
    if med_result and options.get(sel_med):
        query += " AND il.MedicineID = ?"
        params.append(options[sel_med])

    query += " ORDER BY il.LogID DESC"

    result = run_query(query, params if params else None)
    if result:
        cols, rows = result
        df = pd.DataFrame(rows, columns=cols)
        st.markdown(f"### Inventory Log ({len(df)} entries)")
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("---")
        col_a, col_b, col_c = st.columns(3)
        restock   = df[df['TransactionType'] == 'Restock']['Quantity'].sum()
        dispensed = df[df['TransactionType'] == 'Dispensed']['Quantity'].sum()
        damaged   = df[df['TransactionType'] == 'Damaged']['Quantity'].sum()
        with col_a:
            st.metric("Total Restocked",  int(restock))
        with col_b:
            st.metric("Total Dispensed",  int(dispensed))
        with col_c:
            st.metric("Total Damaged",    int(damaged))
    else:
        st.info("No inventory log entries found.")