import streamlit as st
import pandas as pd
from db import run_query, run_action

def show():
    st.markdown("# Prescription Management")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([
        " All Prescriptions", " New Prescription", " Patient History"
    ])

    # ── Tab 1: View ───────────────────────────────────────────────────
    with tab1:
        st.markdown("### All Prescriptions")

        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Pending", "Dispensed", "Expired", "Cancelled"],
            key="rx_status_filter"
        )

        if status_filter == "All":
            result = run_query("""
                SELECT p.PrescriptionID,
                       pt.FirstName + ' ' + pt.LastName AS Patient,
                       d.FirstName  + ' ' + d.LastName  AS Doctor,
                       CAST(p.PrescriptionDate AS VARCHAR) AS Date,
                       p.Diagnosis,
                       p.Status
                FROM Prescription p, Patient pt, Doctor d
                WHERE p.PatientID = pt.PatientID
                AND   p.DoctorID  = d.DoctorID
                ORDER BY p.PrescriptionDate DESC
            """)
        else:
            result = run_query("""
                SELECT p.PrescriptionID,
                       pt.FirstName + ' ' + pt.LastName AS Patient,
                       d.FirstName  + ' ' + d.LastName  AS Doctor,
                       CAST(p.PrescriptionDate AS VARCHAR) AS Date,
                       p.Diagnosis,
                       p.Status
                FROM Prescription p, Patient pt, Doctor d
                WHERE p.PatientID = pt.PatientID
                AND   p.DoctorID  = d.DoctorID
                AND   p.Status = ?
                ORDER BY p.PrescriptionDate DESC
            """, (status_filter,))

        if result:
            cols, rows = result
            df = pd.DataFrame(rows, columns=cols)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.caption(f"Total: {len(df)} prescriptions")
        else:
            st.info("No prescriptions found.")

        st.markdown("---")
        st.markdown("### Update Prescription Status")
        col1, col2, col3 = st.columns(3)
        with col1:
            rx_id_update = st.number_input(
                "Prescription ID",
                min_value=1, step=1,
                key="rx_update_id"          
            )
        with col2:
            new_status = st.selectbox(
                "New Status",
                ["Pending", "Dispensed", "Expired", "Cancelled"],
                key="rx_update_status"
            )
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(" Update Status", key="rx_update_btn"):
                ok = run_action("""
                    UPDATE Prescription SET Status = ?
                    WHERE PrescriptionID = ?
                """, (new_status, rx_id_update))
                if ok:
                    st.success(f"Prescription #{rx_id_update} updated to {new_status}!")

    with tab2:
        st.markdown("### Create New Prescription")

        pat_result = run_query(
            "SELECT PatientID, FirstName + ' ' + LastName FROM Patient"
        )
        doc_result = run_query(
            "SELECT DoctorID, FirstName + ' ' + LastName FROM Doctor"
        )

        if pat_result and doc_result:
            pat_opts = {r[1]: r[0] for r in pat_result[1]}
            doc_opts = {r[1]: r[0] for r in doc_result[1]}

            col1, col2 = st.columns(2)
            with col1:
                rx_id_new = st.number_input(
                    "Prescription ID",
                    min_value=1, step=1,
                    key="rx_new_id"          
                )
                sel_pat   = st.selectbox(
                    "Select Patient",
                    list(pat_opts.keys()),
                    key="rx_new_patient"
                )
                rx_date   = st.date_input("Prescription Date", key="rx_new_date")
            with col2:
                sel_doc   = st.selectbox(
                    "Select Doctor",
                    list(doc_opts.keys()),
                    key="rx_new_doctor"
                )
                diagnosis = st.text_area(
                    "Diagnosis", height=100,
                    key="rx_new_diagnosis"
                )

            if st.button("Save Prescription", key="rx_save_btn"):
                pat_id = pat_opts[sel_pat]
                doc_id = doc_opts[sel_doc]
                ok = run_action("""
                    INSERT INTO Prescription
                    VALUES (?, ?, ?, ?, ?, 'Pending')
                """, (rx_id_new, pat_id, doc_id, rx_date, diagnosis))
                if ok:
                    st.success(f"Prescription #{rx_id_new} created successfully!")
                    st.balloons()
        else:
            st.warning("No patients or doctors found. Please add them first.")

    with tab3:
        st.markdown("### Patient Prescription History")

        pat_result = run_query(
            "SELECT PatientID, FirstName + ' ' + LastName FROM Patient"
        )
        if pat_result:
            pat_opts = {r[1]: r[0] for r in pat_result[1]}
            sel_pat  = st.selectbox(
                "Select Patient",
                list(pat_opts.keys()),
                key="rx_history_patient"
            )
            pat_id = pat_opts[sel_pat]

            if st.button("Get History", key="rx_history_btn"):
                result = run_query("""
                    SELECT p.PrescriptionID,
                           CAST(p.PrescriptionDate AS VARCHAR) AS Date,
                           p.Diagnosis,
                           p.Status,
                           m.MedicineName,
                           pi.Dosage,
                           pi.Frequency,
                           pi.DurationDays
                    FROM Prescription p, Prescription_Item pi, Medicine m
                    WHERE p.PrescriptionID = pi.PrescriptionID
                    AND   pi.MedicineID    = m.MedicineID
                    AND   p.PatientID      = ?
                """, (pat_id,))
                if result:
                    cols, rows = result
                    df = pd.DataFrame(rows, columns=cols)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No prescription history found for this patient.")
        else:
            st.warning("No patients found.")