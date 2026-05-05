import pyodbc
import streamlit as st

def get_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=rameeshatariq\\SQLSERVER;"
            "DATABASE=MediTrackPro;"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def run_query(query, params=None):
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if cursor.description is None:
            conn.close()
            return None

        columns = [col[0] for col in cursor.description]
        rows    = [tuple(row) for row in cursor.fetchall()]
        conn.close()
        return columns, rows
    except Exception as e:
        st.error(f"Query error: {e}")
        try: conn.close()
        except: pass
        return None

def run_action(query, params=None):
    conn = get_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Action error: {e}")
        try: conn.close()
        except: pass
        return False

def run_scalar(query, params=None):
    """Use this for single value queries like COUNT(*), MAX() etc."""
    conn = get_connection()
    if conn is None:
        return 0
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        row = cursor.fetchone()
        conn.close()
        return row[0] if row and row[0] is not None else 0
    except Exception as e:
        st.error(f"Scalar query error: {e}")
        try: conn.close()
        except: pass
        return 0