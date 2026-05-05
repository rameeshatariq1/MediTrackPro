import streamlit as st
import pandas as pd
from db import run_query, run_action

def show():
    st.markdown("# Supplier Management")
    st.markdown("---")

    tab1, tab2 = st.tabs(["All Suppliers", "Add Supplier"])

    with tab1:
        st.markdown("### Registered Suppliers")
        result = run_query("SELECT * FROM Supplier")
        if result:
            cols, rows = result
            df = pd.DataFrame(rows, columns=cols)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No suppliers found.")

    with tab2:
        st.markdown("### Add New Supplier")
        col1, col2 = st.columns(2)
        with col1:
            sup_id  = st.number_input("Supplier ID", min_value=1, step=1)
            name    = st.text_input("Supplier Name")
            phone   = st.text_input("Phone")
        with col2:
            contact = st.text_input("Contact Person")
            address = st.text_area("Address", height=100)

        if st.button("Add Supplier"):
            if name:
                ok = run_action("""
                    INSERT INTO Supplier VALUES (?, ?, ?, ?, ?)
                """, (sup_id, name, contact, phone, address))
                if ok:
                    st.success(f"Supplier {name} added successfully!")
                    st.balloons()
            else:
                st.warning("Please enter a supplier name.")