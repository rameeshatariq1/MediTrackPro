import streamlit as st
import pandas as pd
from db import run_query, run_action

def show():
    st.markdown("#  Doctor Management")
    st.markdown("---")

    tab1, tab2 = st.tabs(["View All Doctors", "Add New Doctor"])

    with tab1:
        st.markdown("### Registered Doctors")
        result = run_query("""
            SELECT DoctorID,
                   FirstName + ' ' + LastName AS FullName,
                   Specialization, LicenseNo, Phone
            FROM Doctor
        """)
        if result:
            cols, rows = result
            df = pd.DataFrame(rows, columns=cols)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"Total doctors: {len(df)}")
        else:
            st.info("No doctors found.")

    with tab2:
        st.markdown("### Add New Doctor")
        col1, col2 = st.columns(2)
        with col1:
            doc_id    = st.number_input("Doctor ID", min_value=1, step=1)
            first     = st.text_input("First Name")
            license_no = st.text_input("License Number")
        with col2:
            last  = st.text_input("Last Name")
            spec  = st.text_input("Specialization")
            phone = st.text_input("Phone")

        if st.button(" Add Doctor"):
            if first and last and license_no:
                ok = run_action("""
                    INSERT INTO Doctor VALUES (?, ?, ?, ?, ?, ?)
                """, (doc_id, first, last, spec, license_no, phone))
                if ok:
                    st.success(f" Dr. {first} {last} added successfully!")
                    st.balloons()
            else:
                st.warning("Please fill all required fields.")