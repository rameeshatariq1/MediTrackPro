import streamlit as st
import pandas as pd
from db import run_query, run_action

def show():
    st.markdown("# Patient Management")
    st.markdown("---")

    tab1, tab2 = st.tabs(["View All Patients", "Add New Patient"])

    with tab1:
        st.markdown("### All Registered Patients")

        search = st.text_input(" Search by name or phone", placeholder="Type to search...")

        if search:
            result = run_query("""
                SELECT PatientID, FirstName + ' ' + LastName AS FullName,
                       DOB, Gender, Phone, Address, BloodGroup
                FROM Patient
                WHERE FirstName LIKE ? OR LastName LIKE ? OR Phone LIKE ?
            """, (f'%{search}%', f'%{search}%', f'%{search}%'))
        else:
            result = run_query("""
                SELECT PatientID, FirstName + ' ' + LastName AS FullName,
                       DOB, Gender, Phone, Address, BloodGroup
                FROM Patient
            """)

        if result:
            cols, rows = result
            df = pd.DataFrame(rows, columns=cols)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"Total patients: {len(df)}")
        else:
            st.info("No patients found.")

    with tab2:
        st.markdown("### Register New Patient")

        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.number_input("Patient ID", min_value=1, step=1)
            first_name = st.text_input("First Name")
            dob        = st.date_input("Date of Birth")
            phone      = st.text_input("Phone Number")
            blood      = st.selectbox("Blood Group",
                         ["A+","A-","B+","B-","AB+","AB-","O+","O-"])
        with col2:
            last_name  = st.text_input("Last Name")
            gender     = st.selectbox("Gender", ["Male", "Female"])
            address    = st.text_area("Address", height=105)

        st.markdown("")
        if st.button("Add Patient"):
            if first_name and last_name and phone:
                ok = run_action("""
                    INSERT INTO Patient
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (patient_id, first_name, last_name,
                      dob, gender, phone, address, blood))
                if ok:
                    st.success(f"Patient {first_name} {last_name} added successfully!")
                    st.balloons()
            else:
                st.warning("Please fill in First Name, Last Name, and Phone.")