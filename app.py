import streamlit as st

st.set_page_config(
    page_title="MediTrack Pro",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* ── Hide Streamlit's auto page links at top of sidebar ── */
    section[data-testid="stSidebar"] a[data-testid="stPageLink"] {
        display: none !important;
    }
    div[data-testid="stSidebarNav"] {
        display: none !important;
    }
    section[data-testid="stSidebar"] ul {
        display: none !important;
    }

    /* ── Main background ── */
    .stApp {
        background-color: #0f1117;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f2e 0%, #16213e 60%, #0f3460 100%);
        border-right: 1px solid #e94560;
    }
    section[data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }

    /* ── Metric cards ── */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #1a1f2e, #16213e);
        border: 1px solid #e94560;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 15px rgba(233, 69, 96, 0.15);
    }
    div[data-testid="metric-container"] label {
        color: #a0aec0 !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #e94560 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #e94560, #c62a47);
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(233, 69, 96, 0.3);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #c62a47, #a01f38);
        box-shadow: 0 6px 20px rgba(233, 69, 96, 0.5);
        transform: translateY(-1px);
    }

    /* ── Headings ── */
    h1, h2, h3 {
        color: #e94560 !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1f2e;
        border-radius: 8px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #a0aec0 !important;
        border-radius: 6px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e94560 !important;
        color: white !important;
    }

    /* ── Inputs ── */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea,
    .stSelectbox select {
        background-color: #1a1f2e !important;
        border: 1px solid #e94560 !important;
        color: #e0e0e0 !important;
        border-radius: 8px;
    }

    /* ── DataFrames ── */
    .stDataFrame {
        border-radius: 10px;
        border: 1px solid #e94560;
        overflow: hidden;
    }
    [data-testid="stDataFrame"] th {
        background-color: #e94560 !important;
        color: white !important;
    }

    /* ── Radio buttons in sidebar ── */
    section[data-testid="stSidebar"] .stRadio label {
        color: #e0e0e0 !important;
        font-size: 15px;
        padding: 8px 12px;
        border-radius: 8px;
        transition: all 0.2s;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(233, 69, 96, 0.15);
        color: #e94560 !important;
    }

    /* ── Selected radio ── */
    section[data-testid="stSidebar"] .stRadio [aria-checked="true"] + label {
        background: rgba(233, 69, 96, 0.2);
        color: #e94560 !important;
        font-weight: 600;
    }

    /* ── Divider ── */
    hr {
        border-color: #e94560 !important;
        opacity: 0.3;
    }

    /* ── Alert / info boxes ── */
    .success-box {
        background: linear-gradient(135deg, #0d2b1a, #0a3d1f);
        border-left: 4px solid #48bb78;
        padding: 12px 16px;
        border-radius: 4px;
        color: #68d391;
        margin: 8px 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #2d2000, #3d2e00);
        border-left: 4px solid #ecc94b;
        padding: 12px 16px;
        border-radius: 4px;
        color: #f6e05e;
        margin: 8px 0;
    }
    .danger-box {
        background: linear-gradient(135deg, #2d0a0a, #3d0f0f);
        border-left: 4px solid #e94560;
        padding: 12px 16px;
        border-radius: 4px;
        color: #fc8181;
        margin: 8px 0;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #1a1f2e; }
    ::-webkit-scrollbar-thumb { background: #e94560; border-radius: 3px; }

    /* ── General text ── */
    .stApp, p, span, div {
        color: #e0e0e0;
    }

    /* ── Caption ── */
    .stCaption {
        color: #718096 !important;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 24px 0 16px 0;
                border-bottom: 1px solid rgba(233,69,96,0.4);
                margin-bottom: 24px;">
        <div style="font-size: 40px; margin-bottom: 8px;">💊</div>
        <h2 style="color: #e94560 !important; margin: 0;
                   font-size: 22px; font-weight: 700;
                   letter-spacing: 1px;">MediTrack Pro</h2>
        <p style="color: rgba(255,255,255,0.5) !important;
                  font-size: 12px; margin: 4px 0 0 0;">
            Pharmacy Management System
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<p style='color: rgba(255,255,255,0.4) !important; "
        "font-size:11px; letter-spacing:2px; "
        "text-transform:uppercase; margin-bottom:8px;'>"
        "Navigation</p>",
        unsafe_allow_html=True
    )

    page = st.radio("", [
        "Dashboard",
        "Patients",
        "Doctors",
        "Medicines",
        "Prescriptions",
        "Suppliers",
        "Inventory Log",
        "Supply Orders",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center; padding: 8px 0;">
        <p style="color: rgba(255,255,255,0.25) !important;
                  font-size: 11px; margin: 0;">
            MediTrack Pro v1.0<br>
            </p>
    </div>
    """, unsafe_allow_html=True)

if   "Dashboard"     in page: from pages import dashboard;     dashboard.show()
elif "Patients"      in page: from pages import patients;      patients.show()
elif "Doctors"       in page: from pages import doctors;       doctors.show()
elif "Medicines"     in page: from pages import medicines;     medicines.show()
elif "Prescriptions" in page: from pages import prescriptions; prescriptions.show()
elif "Suppliers"     in page: from pages import suppliers;     suppliers.show()
elif "Inventory"     in page: from pages import inventory;     inventory.show()
elif "Supply Orders" in page: from pages import supply_orders; supply_orders.show()