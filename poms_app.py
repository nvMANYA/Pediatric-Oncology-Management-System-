import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os 

# --- Configuration Constants ---
PRIMARY_COLOR = '#009688'
ACCENT_COLOR = '#4db6ac'
BACKEND_FILE = 'poms_data.json' # Define the JSON file for persistent storage

# Page configuration
st.set_page_config(
    page_title="POMS - Pediatric Oncology Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (NEW PALETTE: Teal/Green - using #009688 as base)
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #009688; /* Updated Primary Color */
        margin-bottom: 1rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    /* Status Badges */
    .status-admitted, .status-occupied, .status-unpaid {
        background: rgba(255, 107, 107, 0.2);
        color: #ff6b6b; /* Keeping red for negative status */
        padding: 0.3rem 0.6rem;
        border-radius: 15px;
        font-weight: 600;
    }
    .status-discharged, .status-vacant, .status-paid {
        background: rgba(0, 150, 136, 0.2); /* Updated Positive Background */
        color: #009688; /* Updated Positive Color */
        padding: 0.3rem 0.6rem;
        border-radius: 15px;
        font-weight: 600;
    }
    /* Sidebar header color */
    [data-testid="stSidebar"] h1 {
        color: #009688;
    }
</style>
""", unsafe_allow_html=True)

# --- Backend Persistence Functions (NEW) ---

def save_data_to_backend():
    """Saves all current session state data to the defined JSON file."""
    data_to_save = {
        "patients": st.session_state.patients,
        "doctors": st.session_state.doctors,
        "rooms": st.session_state.rooms,
        "appointments": st.session_state.appointments,
        "treatment_plans": st.session_state.treatment_plans,
        "diagnosis": st.session_state.diagnosis,
        "billing": st.session_state.billing,
        "lastSaved": datetime.now().isoformat()
    }
    try:
        with open(BACKEND_FILE, 'w') as f:
            # We use the default encoder, assuming all dates are strings/None as per your structure
            json.dump(data_to_save, f, indent=4)
        st.toast("✅ Data persistently saved to backend JSON.", icon='💾')
    except Exception as e:
        st.error(f"Error saving data to backend: {e}")

def load_data_from_backend():
    """Loads data from the JSON file, or returns False if not found/error."""
    if os.path.exists(BACKEND_FILE):
        try:
            with open(BACKEND_FILE, 'r') as f:
                imported_data = json.load(f)
            
            # Populate session state if keys exist in the loaded data
            st.session_state.patients = imported_data.get('patients', [])
            st.session_state.doctors = imported_data.get('doctors', [])
            st.session_state.rooms = imported_data.get('rooms', [])
            st.session_state.appointments = imported_data.get('appointments', [])
            st.session_state.treatment_plans = imported_data.get('treatment_plans', [])
            st.session_state.diagnosis = imported_data.get('diagnosis', [])
            st.session_state.billing = imported_data.get('billing', [])
            
            return True
        except Exception as e:
            st.error(f"Error loading data from backend: {e}")
            return False
    return False

# --- Data Management Functions (UPDATED to call Persistence) ---

def init_sample_data():
    if 'initialized' not in st.session_state:
        # Attempt to load from persistent backend first
        if load_data_from_backend():
            st.session_state.initialized = True
            st.session_state.menu = "Dashboard"
            return
        
        # If no file found, initialize with sample data
        # --- DOCTORS (6 existing + 8 new = 14 total) ---
        st.session_state.doctors = [
            {"doctor_id": 1, "name": "Dr. Meena", "degree": "MD", "specialization": "Oncology", "contact": "987650001"},
            {"doctor_id": 2, "name": "Dr. Arjun", "degree": "MBBS", "specialization": "Pediatrics", "contact": "987650002"},
            {"doctor_id": 3, "name": "Dr. Ravi", "degree": "MD", "specialization": "Radiology", "contact": "987650003"},
            {"doctor_id": 4, "name": "Dr. Sneha", "degree": "MBBS", "specialization": "Surgery", "contact": "987650004"},
            {"doctor_id": 5, "name": "Dr. Kiran", "degree": "MD", "specialization": "Pathology", "contact": "987650005"},
            {"doctor_id": 6, "name": "Dr. Priya", "degree": "MBBS", "specialization": "Oncology", "contact": "987650006"},
            
            # New doctors
            {"doctor_id": 7, "name": "Dr. Sameer", "degree": "MD", "specialization": "Pediatrics", "contact": "987650007"},
            {"doctor_id": 8, "name": "Dr. Neha", "degree": "MBBS", "specialization": "Oncology", "contact": "987650008"},
            {"doctor_id": 9, "name": "Dr. Vimal", "degree": "MD", "specialization": "Radiology", "contact": "987650009"},
            {"doctor_id": 10, "name": "Dr. Zoya", "degree": "MBBS", "specialization": "Oncology", "contact": "987650010"},
            {"doctor_id": 11, "name": "Dr. Imran", "degree": "MD", "specialization": "Surgery", "contact": "987650011"},
            {"doctor_id": 12, "name": "Dr. Lakshmi", "degree": "MBBS", "specialization": "Pediatrics", "contact": "987650012"},
            {"doctor_id": 13, "name": "Dr. Rohan", "degree": "MD", "specialization": "Oncology", "contact": "987650013"},
            {"doctor_id": 14, "name": "Dr. Anjali", "degree": "MBBS", "specialization": "Pathology", "contact": "987650014"}
        ]
        
        # --- PATIENTS (5 existing + 15 new = 20 total) ---
        st.session_state.patients = [
            {"patient_id": 1, "name": "Aarav", "age": 10, "dob": "2015-03-10", "gender": "Male", "address": "Bangalore", 
             "diagnosis": "Leukemia", "admission_date": "2025-01-12", "discharge_date": "2025-02-15", "doctor_id": 1, "status": "Discharged"},
            {"patient_id": 2, "name": "Diya", "age": 8, "dob": "2017-06-12", "gender": "Female", "address": "Mysore", 
             "diagnosis": "Lymphoma", "admission_date": "2025-02-01", "discharge_date": None, "doctor_id": 2, "status": "Admitted"},
            {"patient_id": 3, "name": "Rohan", "age": 11, "dob": "2014-01-18", "gender": "Male", "address": "Chennai", 
             "diagnosis": "Tumor", "admission_date": "2025-01-20", "discharge_date": "2025-02-25", "doctor_id": 3, "status": "Discharged"},
            {"patient_id": 4, "name": "Kavya", "age": 9, "dob": "2016-04-25", "gender": "Female", "address": "Hubli", 
             "diagnosis": "Anemia", "admission_date": "2025-03-05", "discharge_date": None, "doctor_id": 4, "status": "Admitted"},
            {"patient_id": 5, "name": "Aditi", "age": 7, "dob": "2018-09-09", "gender": "Female", "address": "Hassan", 
             "diagnosis": "Infection", "admission_date": "2025-03-15", "discharge_date": None, "doctor_id": 5, "status": "Admitted"},
            
            # New patients (15 total)
            {"patient_id": 6, "name": "Vivaan", "age": 6, "dob": "2019-02-20", "gender": "Male", "address": "Pune", 
             "diagnosis": "Leukemia", "admission_date": "2025-03-20", "discharge_date": None, "doctor_id": 1, "status": "Admitted"},
            {"patient_id": 7, "name": "Misha", "age": 12, "dob": "2013-05-01", "gender": "Female", "address": "Delhi", 
             "diagnosis": "Neuroblastoma", "admission_date": "2025-03-22", "discharge_date": None, "doctor_id": 8, "status": "Admitted"},
            {"patient_id": 8, "name": "Neel", "age": 14, "dob": "2011-08-15", "gender": "Male", "address": "Mumbai", 
             "diagnosis": "Sarcoma", "admission_date": "2025-03-25", "discharge_date": None, "doctor_id": 10, "status": "Admitted"},
            {"patient_id": 9, "name": "Tanya", "age": 5, "dob": "2020-11-11", "gender": "Female", "address": "Kochi", 
             "diagnosis": "Tumor", "admission_date": "2025-03-28", "discharge_date": "2025-04-10", "doctor_id": 7, "status": "Discharged"},
            {"patient_id": 10, "name": "Jatin", "age": 16, "dob": "2009-01-05", "gender": "Male", "address": "Hyderabad", 
             "diagnosis": "Anemia", "admission_date": "2025-04-01", "discharge_date": None, "doctor_id": 12, "status": "Admitted"},
            {"patient_id": 11, "name": "Siya", "age": 4, "dob": "2021-09-30", "gender": "Female", "address": "Jaipur", 
             "diagnosis": "Leukemia", "admission_date": "2025-04-05", "discharge_date": None, "doctor_id": 6, "status": "Admitted"},
            {"patient_id": 12, "name": "Aryan", "age": 13, "dob": "2012-07-07", "gender": "Male", "address": "Lucknow", 
             "diagnosis": "Lymphoma", "admission_date": "2025-04-08", "discharge_date": "2025-05-10", "doctor_id": 13, "status": "Discharged"},
            {"patient_id": 13, "name": "Zaina", "age": 9, "dob": "2016-02-14", "gender": "Female", "address": "Goa", 
             "diagnosis": "Tumor", "admission_date": "2025-04-12", "discharge_date": None, "doctor_id": 11, "status": "Admitted"},
            {"patient_id": 14, "name": "Harsh", "age": 15, "dob": "2010-04-04", "gender": "Male", "address": "Indore", 
             "diagnosis": "Infection", "admission_date": "2025-04-15", "discharge_date": None, "doctor_id": 4, "status": "Admitted"},
            {"patient_id": 15, "name": "Esha", "age": 7, "dob": "2018-01-28", "gender": "Female", "address": "Patna", 
             "diagnosis": "Sarcoma", "admission_date": "2025-04-18", "discharge_date": None, "doctor_id": 8, "status": "Admitted"},
            {"patient_id": 16, "name": "Karan", "age": 11, "dob": "2014-10-10", "gender": "Male", "address": "Bhopal", 
             "diagnosis": "Anemia", "admission_date": "2025-04-22", "discharge_date": "2025-05-01", "doctor_id": 2, "status": "Discharged"},
            {"patient_id": 17, "name": "Lila", "age": 3, "dob": "2022-03-03", "gender": "Female", "address": "Ranchi", 
             "diagnosis": "Leukemia", "admission_date": "2025-04-25", "discharge_date": None, "doctor_id": 1, "status": "Admitted"},
            {"patient_id": 18, "name": "Rajat", "age": 17, "dob": "2008-06-06", "gender": "Male", "address": "Surat", 
             "diagnosis": "Lymphoma", "admission_date": "2025-04-28", "discharge_date": None, "doctor_id": 13, "status": "Admitted"},
            {"patient_id": 19, "name": "Heena", "age": 8, "dob": "2017-12-12", "gender": "Female", "address": "Nagpur", 
             "diagnosis": "Infection", "admission_date": "2025-05-01", "discharge_date": None, "doctor_id": 5, "status": "Admitted"},
            {"patient_id": 20, "name": "Bhavin", "age": 10, "dob": "2015-05-15", "gender": "Male", "address": "Vadodara", 
             "diagnosis": "Tumor", "admission_date": "2025-05-05", "discharge_date": None, "doctor_id": 10, "status": "Admitted"}
        ]
        
        # --- ROOMS (8 existing + 10 new = 18 total) ---
        st.session_state.rooms = [
            {"room_id": 1, "room_type": "General", "occupancy_status": "Occupied", "patient_id": 6, "cost_per_day": 5000.00},
            {"room_id": 2, "room_type": "Private", "occupancy_status": "Occupied", "patient_id": 2, "cost_per_day": 15000.00},
            {"room_id": 3, "room_type": "Semi-Private", "occupancy_status": "Occupied", "patient_id": 4, "cost_per_day": 10000.00},
            {"room_id": 4, "room_type": "ICU", "occupancy_status": "Occupied", "patient_id": 5, "cost_per_day": 30000.00},
            {"room_id": 5, "room_type": "General", "occupancy_status": "Vacant", "patient_id": None, "cost_per_day": 5000.00},
            {"room_id": 6, "room_type": "Private", "occupancy_status": "Vacant", "patient_id": None, "cost_per_day": 15000.00},
            {"room_id": 7, "room_type": "ICU", "occupancy_status": "Vacant", "patient_id": None, "cost_per_day": 30000.00},
            {"room_id": 8, "room_type": "General", "occupancy_status": "Vacant", "patient_id": None, "cost_per_day": 5000.00},

            # New rooms (10 total)
            {"room_id": 9, "room_type": "Private", "occupancy_status": "Occupied", "patient_id": 7, "cost_per_day": 15000.00},
            {"room_id": 10, "room_type": "Semi-Private", "occupancy_status": "Occupied", "patient_id": 8, "cost_per_day": 10000.00},
            {"room_id": 11, "room_type": "General", "occupancy_status": "Occupied", "patient_id": 10, "cost_per_day": 5000.00},
            {"room_id": 12, "room_type": "ICU", "occupancy_status": "Occupied", "patient_id": 11, "cost_per_day": 30000.00},
            {"room_id": 13, "room_type": "Private", "occupancy_status": "Occupied", "patient_id": 13, "cost_per_day": 15000.00},
            {"room_id": 14, "room_type": "Semi-Private", "occupancy_status": "Occupied", "patient_id": 14, "cost_per_day": 10000.00},
            {"room_id": 15, "room_type": "General", "occupancy_status": "Occupied", "patient_id": 15, "cost_per_day": 5000.00},
            {"room_id": 16, "room_type": "ICU", "occupancy_status": "Occupied", "patient_id": 17, "cost_per_day": 30000.00},
            {"room_id": 17, "room_type": "General", "occupancy_status": "Vacant", "patient_id": None, "cost_per_day": 5000.00},
            {"room_id": 18, "room_type": "Private", "occupancy_status": "Occupied", "patient_id": 18, "cost_per_day": 15000.00},
        ]
        
        # --- APPOINTMENTS (6 existing + 8 new = 14 total) ---
        today = datetime.now().strftime("%Y-%m-%d")
        st.session_state.appointments = [
            {"appointment_id": 1, "date": "2025-01-10", "time": "10:00", "reason": "Initial Checkup", "doctor_id": 1, "patient_id": 1},
            {"appointment_id": 2, "date": "2025-02-01", "time": "14:30", "reason": "Follow-up", "doctor_id": 2, "patient_id": 2},
            {"appointment_id": 3, "date": "2025-01-18", "time": "09:00", "reason": "Scan Review", "doctor_id": 3, "patient_id": 3},
            {"appointment_id": 4, "date": today, "time": "11:00", "reason": "Routine", "doctor_id": 4, "patient_id": 4},
            {"appointment_id": 5, "date": "2025-03-15", "time": "16:00", "reason": "Consultation", "doctor_id": 5, "patient_id": 5},
            {"appointment_id": 6, "date": "2026-01-10", "time": "10:00", "reason": "Annual Follow-up", "doctor_id": 1, "patient_id": 1},

            # New appointments
            {"appointment_id": 7, "date": "2025-03-21", "time": "09:30", "reason": "First Chemo Round", "doctor_id": 8, "patient_id": 6},
            {"appointment_id": 8, "date": "2025-04-10", "time": "15:00", "reason": "Discharge Check", "doctor_id": 7, "patient_id": 9},
            {"appointment_id": 9, "date": "2025-04-15", "time": "10:30", "reason": "Routine Checkup", "doctor_id": 12, "patient_id": 10},
            {"appointment_id": 10, "date": "2025-05-02", "time": "14:00", "reason": "Scan Review", "doctor_id": 13, "patient_id": 12},
            {"appointment_id": 11, "date": "2025-05-08", "time": "09:00", "reason": "Pre-Op Consultation", "doctor_id": 11, "patient_id": 13},
            {"appointment_id": 12, "date": today, "time": "16:00", "reason": "Follow-up", "doctor_id": 10, "patient_id": 15},
            {"appointment_id": 13, "date": "2025-05-15", "time": "11:30", "reason": "Final Checkup", "doctor_id": 2, "patient_id": 16},
            {"appointment_id": 14, "date": "2025-05-20", "time": "13:00", "reason": "Biopsy Review", "doctor_id": 1, "patient_id": 17}
        ]
        
        # --- TREATMENT PLANS (3 existing + 10 new = 13 total) ---
        st.session_state.treatment_plans = [
            {"plan_id": 1, "patient_id": 1, "doctor_id": 1, "diagnosis_id": 1, "details": "Chemo Protocol A, 4 cycles", 
             "start_date": "2025-01-14", "end_date": "2025-02-10"},
            {"plan_id": 2, "patient_id": 2, "doctor_id": 2, "diagnosis_id": 2, "details": "Radiation + Chemo Protocol B", 
             "start_date": "2025-02-03", "end_date": "2025-05-01"},
            {"plan_id": 3, "patient_id": 4, "doctor_id": 4, "diagnosis_id": 4, "details": "Iron supplements and monitoring", 
             "start_date": "2025-03-05", "end_date": "2025-06-01"},

            # New treatment plans
            {"plan_id": 4, "patient_id": 5, "doctor_id": 5, "diagnosis_id": 5, "details": "Antibiotics (7 days) and observation", 
             "start_date": "2025-03-15", "end_date": "2025-03-22"},
            {"plan_id": 5, "patient_id": 6, "doctor_id": 1, "diagnosis_id": 6, "details": "High-dose Chemotherapy, 6 cycles", 
             "start_date": "2025-03-21", "end_date": "2025-08-30"},
            {"plan_id": 6, "patient_id": 7, "doctor_id": 8, "diagnosis_id": 7, "details": "Surgery followed by targeted radiation", 
             "start_date": "2025-03-24", "end_date": "2025-07-01"},
            {"plan_id": 7, "patient_id": 8, "doctor_id": 10, "diagnosis_id": 8, "details": "Immunotherapy & Chemo Protocol D", 
             "start_date": "2025-03-26", "end_date": "2025-10-15"},
            {"plan_id": 8, "patient_id": 10, "doctor_id": 12, "diagnosis_id": 10, "details": "B12 injections and dietary changes", 
             "start_date": "2025-04-02", "end_date": "2025-07-01"},
            {"plan_id": 9, "patient_id": 11, "doctor_id": 6, "diagnosis_id": 11, "details": "Milder Chemo Protocol E (maintenance)", 
             "start_date": "2025-04-07", "end_date": "2026-04-07"},
            {"plan_id": 10, "patient_id": 13, "doctor_id": 11, "diagnosis_id": 13, "details": "Immediate Surgery (Scheduled May 15)", 
             "start_date": "2025-04-13", "end_date": "2025-05-30"},
            {"plan_id": 11, "patient_id": 15, "doctor_id": 8, "diagnosis_id": 15, "details": "Pre-operative assessment for bone tumor", 
             "start_date": "2025-04-19", "end_date": "2025-06-01"},
            {"plan_id": 12, "patient_id": 17, "doctor_id": 1, "diagnosis_id": 17, "details": "Induction Phase Chemo", 
             "start_date": "2025-04-26", "end_date": "2025-06-25"},
            {"plan_id": 13, "patient_id": 18, "doctor_id": 13, "diagnosis_id": 18, "details": "Palliative care and symptom control", 
             "start_date": "2025-04-29", "end_date": None}
        ]
        
        # --- DIAGNOSIS (4 existing + 10 new = 14 total) ---
        st.session_state.diagnosis = [
            {"diagnosis_id": 1, "patient_id": 1, "diagnosis_type": "Blood", "description": "Complete Blood Count", 
             "result": "Leukemia confirmed", "date": "2025-01-13", "disease_type": "Leukemia"},
            {"diagnosis_id": 2, "patient_id": 2, "diagnosis_type": "Scan", "description": "MRI (neck and chest)", 
             "result": "Lymphoma confirmed, stage 2", "date": "2025-02-02", "disease_type": "Lymphoma"},
            {"diagnosis_id": 3, "patient_id": 3, "diagnosis_type": "CT", "description": "Brain CT scan", 
             "result": "Benign Tumor, post-op stable", "date": "2025-01-21", "disease_type": "Tumor"},
            {"diagnosis_id": 4, "patient_id": 4, "diagnosis_type": "Blood", "description": "Iron level test", 
             "result": "Severe Anemia (Positive for low iron)", "date": "2025-03-06", "disease_type": "Anemia"},
            
            # New diagnosis records
            {"diagnosis_id": 5, "patient_id": 5, "diagnosis_type": "Culture", "description": "Blood Culture", 
             "result": "Bacterial infection identified", "date": "2025-03-16", "disease_type": "Infection"},
            {"diagnosis_id": 6, "patient_id": 6, "diagnosis_type": "Marrow", "description": "Bone Marrow Biopsy", 
             "result": "ALL (Acute Lymphoblastic Leukemia) confirmed", "date": "2025-03-20", "disease_type": "Leukemia"},
            {"diagnosis_id": 7, "patient_id": 7, "diagnosis_type": "Scan", "description": "Whole body MIBG Scan", 
             "result": "Stage 4 Neuroblastoma", "date": "2025-03-23", "disease_type": "Neuroblastoma"},
            {"diagnosis_id": 8, "patient_id": 8, "diagnosis_type": "Biopsy", "description": "Needle Biopsy (Femur)", 
             "result": "Ewing Sarcoma", "date": "2025-03-26", "disease_type": "Sarcoma"},
            {"diagnosis_id": 9, "patient_id": 9, "diagnosis_type": "Blood", "description": "Post-op blood screen", 
             "result": "Tumor markers negative", "date": "2025-04-10", "disease_type": "Tumor"},
            {"diagnosis_id": 10, "patient_id": 10, "diagnosis_type": "Blood", "description": "B12/Folate levels", 
             "result": "Folate deficiency anemia", "date": "2025-04-03", "disease_type": "Anemia"},
            {"diagnosis_id": 11, "patient_id": 11, "diagnosis_type": "Marrow", "description": "Bone Marrow Aspirate", 
             "result": "AML (Acute Myeloid Leukemia) confirmed", "date": "2025-04-06", "disease_type": "Leukemia"},
            {"diagnosis_id": 12, "patient_id": 12, "diagnosis_type": "Scan", "description": "CT Chest", 
             "result": "Tumor shrinkage post-treatment", "date": "2025-05-01", "disease_type": "Lymphoma"},
            {"diagnosis_id": 13, "patient_id": 13, "diagnosis_type": "MRI", "description": "Brain MRI", 
             "result": "Glioblastoma confirmed", "date": "2025-04-13", "disease_type": "Tumor"},
            {"diagnosis_id": 14, "patient_id": 14, "diagnosis_type": "Culture", "description": "Pus swab culture", 
             "result": "Staph infection in wound", "date": "2025-04-16", "disease_type": "Infection"}
        ]
        
        # --- BILLING (4 existing + 10 new = 14 total) ---
        st.session_state.billing = [
            {"bill_id": 1, "patient_id": 1, "amount": 120000.00, "status": "Paid", "date": "2025-02-11", "description": "Chemo Protocol A"},
            {"bill_id": 2, "patient_id": 2, "amount": 85000.00, "status": "Unpaid", "date": "2025-03-02", "description": "Room/Board Fee"},
            {"bill_id": 3, "patient_id": 3, "amount": 150000.00, "status": "Paid", "date": "2025-02-26", "description": "Surgery & Recovery"},
            {"bill_id": 4, "patient_id": 4, "amount": 5000.00, "status": "Unpaid", "date": "2025-03-07", "description": "Iron Level Test"},

            # New billing records
            {"bill_id": 5, "patient_id": 5, "amount": 5000.00, "status": "Paid", "date": "2025-03-16", "description": "Blood Culture Diagnosis"},
            {"bill_id": 6, "patient_id": 6, "amount": 5000.00, "status": "Unpaid", "date": "2025-03-21", "description": "Room & Board (General R1)"},
            {"bill_id": 7, "patient_id": 7, "amount": 15000.00, "status": "Unpaid", "date": "2025-03-23", "description": "Room & Board (Private R9)"},
            {"bill_id": 8, "patient_id": 8, "amount": 10000.00, "status": "Unpaid", "date": "2025-03-26", "description": "Room & Board (Semi-Private R10)"},
            {"bill_id": 9, "patient_id": 10, "amount": 5000.00, "status": "Paid", "date": "2025-04-02", "description": "B12/Folate Diagnosis"},
            {"bill_id": 10, "patient_id": 11, "amount": 30000.00, "status": "Unpaid", "date": "2025-04-06", "description": "Room & Board (ICU R12)"},
            {"bill_id": 11, "patient_id": 13, "amount": 15000.00, "status": "Paid", "date": "2025-04-12", "description": "Room & Board (Private R13)"},
            {"bill_id": 12, "patient_id": 14, "amount": 10000.00, "status": "Unpaid", "date": "2025-04-15", "description": "Room & Board (Semi-Private R14)"},
            {"bill_id": 13, "patient_id": 15, "amount": 5000.00, "status": "Paid", "date": "2025-04-18", "description": "Room & Board (General R15)"},
            {"bill_id": 14, "patient_id": 17, "amount": 30000.00, "status": "Unpaid", "date": "2025-04-26", "description": "Room & Board (ICU R16)"},
        ]
        
        st.session_state.initialized = True
        st.session_state.menu = "Dashboard"
        # Save sample data to create the initial backend file
        save_data_to_backend() 

# --- Utility Functions (UPDATED to use save_data_to_backend) ---

def get_patient_name(patient_id):
    """FUNCTION: Takes an ID and returns a name. Pure look-up with no side effects."""
    patient = next((p for p in st.session_state.patients if p['patient_id'] == patient_id), None)
    return patient['name'] if patient else 'N/A'

def get_doctor_name(doctor_id):
    """FUNCTION: Takes an ID and returns a name."""
    doctor = next((d for d in st.session_state.doctors if d['doctor_id'] == doctor_id), None)
    return doctor['name'] if doctor else 'N/A'

def find_patient_room(patient_id):
    """FUNCTION: Takes an ID and returns the associated room object (if occupied)."""
    return next((r for r in st.session_state.rooms if r.get('patient_id') == patient_id and r['occupancy_status'] == 'Occupied'), None)

def add_auto_bill_entry(patient_id, record_type, amount, date, description):
    """PROCEDURE: Performs a side-effect: creates a new record in st.session_state.billing and saves to backend."""
    new_id = max([b['bill_id'] for b in st.session_state.billing]) + 1 if st.session_state.billing else 1
    new_bill = {
        "bill_id": new_id,
        "patient_id": patient_id,
        "amount": amount,
        "status": "Unpaid",
        "date": date,
        "description": f"{record_type}"
    }
    st.session_state.billing.append(new_bill)
    save_data_to_backend() # <--- NEW: Save to backend after auto-billing
    
    # --- FIX: Using st.toast() instead of st.success() to survive the rerun/redirect ---
    st.toast(f"✅ Automated Bill (₹{amount:,.0f}) created for {get_patient_name(patient_id)}.", icon='💰')

# --- Page Functions (CRUD Operations updated to call save_data_to_backend) ---

def show_dashboard():
    st.markdown('<h1 class="main-header">Dashboard</h1>', unsafe_allow_html=True)
    
    # Metrics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_patients = len(st.session_state.patients)
        one_week_ago = datetime.now() - timedelta(days=7)
        new_patients = sum(1 for p in st.session_state.patients 
                           if p.get('admission_date') and datetime.strptime(p['admission_date'], '%Y-%m-%d') >= one_week_ago)
        st.metric("Total Patients", total_patients, f"+{new_patients} this week")
    
    with col2:
        total_doctors = len(st.session_state.doctors)
        st.metric("Total Doctors", total_doctors)
    
    with col3:
        occupied_rooms = sum(1 for r in st.session_state.rooms if r['occupancy_status'] == 'Occupied')
        icu_rooms = sum(1 for r in st.session_state.rooms if r['room_type'] == 'ICU' and r['occupancy_status'] == 'Occupied')
        st.metric("Rooms Occupied", occupied_rooms, f"{icu_rooms} ICU")
    
    with col4:
        today = datetime.now().strftime("%Y-%m-%d")
        today_appointments = sum(1 for a in st.session_state.appointments if a['date'] == today)
        pending = sum(1 for a in st.session_state.appointments if datetime.strptime(a['date'], '%Y-%m-%d') >= datetime.strptime(today, '%Y-%m-%d'))
        st.metric("Today's Appointments", today_appointments, f"{pending} pending")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Patient Admissions by Month")
        df_patients = pd.DataFrame(st.session_state.patients)
        
        if not df_patients.empty:
            df_patients['admission_date'] = df_patients['admission_date'].astype(str)
            df_patients['admission_date'] = pd.to_datetime(df_patients['admission_date'], errors='coerce')
            df_patients.dropna(subset=['admission_date'], inplace=True)
            df_patients['month_year'] = df_patients['admission_date'].dt.strftime('%Y-%m') 
            df_patients['month_label'] = df_patients['admission_date'].dt.strftime('%b %Y') 
            monthly_counts = df_patients.groupby(['month_year', 'month_label']).size().reset_index(name='count')
            monthly_counts = monthly_counts.sort_values('month_year')
            
            fig = px.line(monthly_counts, x='month_label', y='count', markers=True, 
                          color_discrete_sequence=[PRIMARY_COLOR]) # Use NEW color
            fig.update_layout(xaxis_title="Month", yaxis_title="Admissions", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No admissions data to display.")
    
    with col2:
        st.subheader("Disease Distribution")
        if not df_patients.empty:
            disease_counts = df_patients['diagnosis'].value_counts()
            fig = px.pie(values=disease_counts.values, names=disease_counts.index, 
                         hole=0.3, color_discrete_sequence=px.colors.sequential.Teal) # Use NEW color
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No disease data to display.")
    
    st.markdown("---")
    
    # Recent patients table
    st.subheader("Recent Patients")
    if not df_patients.empty:
        df_recent = df_patients.sort_values('admission_date', ascending=False).head(5)
        df_recent['Doctor'] = df_recent['doctor_id'].apply(get_doctor_name)
        display_df = df_recent[['patient_id', 'name', 'age', 'diagnosis', 'Doctor', 'status']].copy()
        display_df.columns = ['ID', 'Name', 'Age', 'Diagnosis', 'Doctor', 'Status']
        st.dataframe(display_df, use_container_width=True, hide_index=True)

# Patients page
def show_patients():
    st.markdown('<h1 class="main-header">Patient Management</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add New Patient", use_container_width=True):
            st.session_state.show_patient_form = True
            st.session_state.edit_patient_id = None # Clear edit state
            st.rerun()

    # Function to display and handle the form (for both add and edit)
    def patient_form_handler(edit_patient=None):
        if edit_patient:
            st.subheader(f"Edit Patient: {edit_patient['name']} (ID: {edit_patient['patient_id']})")
            default_values = {
                'name': edit_patient['name'],
                'age': edit_patient['age'],
                'dob': datetime.strptime(edit_patient['dob'], "%Y-%m-%d").date(),
                'gender': edit_patient['gender'],
                'address': edit_patient['address'],
                'diagnosis': edit_patient['diagnosis'],
                'doctor_id': edit_patient['doctor_id'],
                'admission_date': datetime.strptime(edit_patient['admission_date'], "%Y-%m-%d").date(),
                'discharge_date': datetime.strptime(edit_patient['discharge_date'], "%Y-%m-%d").date() if edit_patient['discharge_date'] else None
            }
            current_room = find_patient_room(edit_patient['patient_id'])
            room_required = bool(current_room)
            default_room_id = current_room['room_id'] if current_room else None
        else:
            st.subheader("Add New Patient")
            default_values = {'name': '', 'age': 10, 'dob': datetime.now().date(), 'gender': 'Male', 
                              'address': '', 'diagnosis': '', 'doctor_id': st.session_state.doctors[0]['doctor_id'],
                              'admission_date': datetime.now().date(), 'discharge_date': None}
            room_required = False
            default_room_id = None

        with st.form("patient_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name*", default_values['name'])
                age = st.number_input("Age*", min_value=1, max_value=18, value=default_values['age'])
                dob = st.date_input("Date of Birth*", default_values['dob'])
                gender = st.selectbox("Gender*", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(default_values['gender']))
            
            with col2:
                address = st.text_area("Address", height=100, value=default_values['address'])
                diagnosis = st.text_input("Primary Diagnosis*", default_values['diagnosis'])
                doctor_id = st.selectbox("Assigned Doctor*", 
                                         options=[d['doctor_id'] for d in st.session_state.doctors],
                                         format_func=lambda x: get_doctor_name(x),
                                         index=[d['doctor_id'] for d in st.session_state.doctors].index(default_values['doctor_id']))
            
            col1, col2 = st.columns(2)
            with col1:
                admission_date = st.date_input("Admission Date*", default_values['admission_date'])
            with col2:
                discharge_date = st.date_input("Discharge Date (Optional)", value=default_values['discharge_date'] if default_values['discharge_date'] else None)

            st.markdown("---")
            st.subheader("Room Assignment (Room + Board Bill generated on assignment)")
            
            room_required_new = st.checkbox("Does this patient require a room?", value=room_required)

            room_id = None
            room_cost = 0.0
            
            if room_required_new:
                # Get vacant rooms, plus the current room if editing, and sort by cost
                all_rooms = st.session_state.rooms
                vacant_rooms = sorted([r for r in all_rooms if r['occupancy_status'] == 'Vacant'], key=lambda r: r['cost_per_day'])
                
                room_options = []
                room_options_data = {}
                
                # Add current room (if editing)
                if default_room_id:
                    current_room_data = next((r for r in all_rooms if r['room_id'] == default_room_id), None)
                    if current_room_data:
                        room_options.append(default_room_id)
                        room_options_data[default_room_id] = current_room_data
                
                # Add vacant rooms to options, ensuring no duplicates
                for r in vacant_rooms:
                    if r['room_id'] != default_room_id:
                        room_options.append(r['room_id'])
                        room_options_data[r['room_id']] = r
                
                if room_options:
                    # Determine default selection index
                    if default_room_id and default_room_id in room_options:
                        default_index = room_options.index(default_room_id)
                    else:
                        default_index = 0
                        
                    room_format_func = lambda x: f"Room {x} ({room_options_data[x]['room_type']}) - ₹{room_options_data[x]['cost_per_day']:,.0f}/day"
                    
                    room_id = st.selectbox("Select Room (Sorted by Cost)", 
                                           options=room_options,
                                           format_func=room_format_func,
                                           index=default_index)

                    # Store the cost of the selected room for billing consistency
                    if room_id:
                        room_cost = room_options_data[room_id]['cost_per_day']

                else:
                    st.warning("No available rooms")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(f"💾 {'Update' if edit_patient else 'Save'} Patient", use_container_width=True):
                    if not (name and diagnosis):
                        st.error("Name and Primary Diagnosis are required.")
                        return 
                    
                    new_status = "Discharged" if discharge_date else "Admitted"
                    
                    is_new_patient = not edit_patient
                    patient_id_to_use = edit_patient['patient_id'] if edit_patient else None

                    if is_new_patient:
                        # Save logic (Add New Patient)
                        patient_id_to_use = max([p['patient_id'] for p in st.session_state.patients]) + 1 if st.session_state.patients else 1
                        new_patient = {
                            "patient_id": patient_id_to_use, "name": name, "age": age, "dob": dob.strftime("%Y-%m-%d"),
                            "gender": gender, "address": address, "diagnosis": diagnosis, "admission_date": admission_date.strftime("%Y-%m-%d"),
                            "discharge_date": discharge_date.strftime("%Y-%m-%d") if discharge_date else None,
                            "doctor_id": doctor_id, "status": new_status
                        }
                        st.session_state.patients.append(new_patient)
                        st.success(f"Patient {name} added successfully!")
                    else:
                        # Update logic
                        patient_index = next((i for i, p in enumerate(st.session_state.patients) if p['patient_id'] == patient_id_to_use), -1)
                        if patient_index != -1:
                            st.session_state.patients[patient_index].update({
                                "name": name, "age": age, "dob": dob.strftime("%Y-%m-%d"), "gender": gender, 
                                "address": address, "diagnosis": diagnosis, "admission_date": admission_date.strftime("%Y-%M-%d"),
                                "discharge_date": discharge_date.strftime("%Y-%m-%d") if discharge_date else None,
                                "doctor_id": doctor_id, "status": new_status
                            })
                            st.success(f"Patient {name} updated successfully!")

                    # Room update and Initial Billing logic
                    old_room = find_patient_room(patient_id_to_use)
                    room_changed = old_room and room_id and old_room.get('room_id') != room_id
                    
                    # 1. Clear old room assignment if patient is changing rooms or no longer needs a room
                    if old_room and (not room_required_new or room_changed):
                        old_room['occupancy_status'] = 'Vacant'
                        old_room['patient_id'] = None
                        
                    # 2. Assign new room if required
                    if room_required_new and room_id:
                        room_to_update = next(r for r in st.session_state.rooms if r['room_id'] == room_id)
                        
                        # Only add a bill if a NEW room is being assigned (either new patient or patient moving)
                        if room_to_update and (is_new_patient or room_changed):
                            room_to_update['occupancy_status'] = 'Occupied'
                            room_to_update['patient_id'] = patient_id_to_use
                            
                            # Initial Room Billing Automation (FIXED TO 1 DAY CHARGE)
                            room_cost = room_to_update['cost_per_day']
                            add_auto_bill_entry(patient_id_to_use, "Room & Board ", room_cost * 1, # CHARGED FOR 1 DAY
                                                datetime.now().strftime("%Y-%m-%d"), 
                                                f"{room_to_update['room_type']} R{room_id} (1-day Charge, Rate: ₹{room_cost:,.0f}/day)")
                            st.session_state.menu = "Billing" # <--- Automated Navigation
                        # If patient is editing and staying in the SAME room
                        elif room_to_update and room_to_update.get('patient_id') == patient_id_to_use:
                            room_to_update['occupancy_status'] = 'Occupied'
                            
                    
                    save_data_to_backend() # <--- NEW: Save to backend after patient update/creation
                    
                    st.session_state.show_patient_form = False
                    st.session_state.edit_patient_id = None
                    st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.show_patient_form = False
                    st.session_state.edit_patient_id = None
                    st.rerun()

    # Form logic
    if st.session_state.get('show_patient_form', False) or st.session_state.get('edit_patient_id') is not None:
        patient_to_edit = next((p for p in st.session_state.patients if p['patient_id'] == st.session_state.get('edit_patient_id')), None)
        patient_form_handler(patient_to_edit)
    else:
        # Patients table logic
        st.markdown("---")
        df = pd.DataFrame(st.session_state.patients)
        if not df.empty:
            df['Doctor'] = df['doctor_id'].apply(get_doctor_name)
            df['Room'] = df['patient_id'].apply(lambda pid: f"R{find_patient_room(pid)['room_id']}" if find_patient_room(pid) else 'N/A')
            display_df = df[['patient_id', 'name', 'age', 'gender', 'diagnosis', 'Room', 'admission_date', 'Doctor', 'status']].copy()
            display_df.columns = ['ID', 'Name', 'Age', 'Gender', 'Diagnosis', 'Room', 'Admission Date', 'Doctor', 'Status']
            
            col_list = st.columns(len(display_df.columns) + 2) # +2 for Edit and Delete columns
            
            # Table Header
            for i, col_name in enumerate(display_df.columns):
                col_list[i].write(f"**{col_name}**")
            col_list[-2].write("**Edit**")
            col_list[-1].write("**Delete**")

            # Table Rows
            for i, row in display_df.iterrows():
                row_cols = st.columns(len(display_df.columns) + 2)
                for j, col_name in enumerate(display_df.columns):
                    row_cols[j].write(row[col_name])

                # Edit Button (Accessing the correct key: 'ID')
                if row_cols[-2].button("✏️", key=f"edit_patient_{row['ID']}"):
                    st.session_state.edit_patient_id = row['ID']
                    st.session_state.show_patient_form = True
                    st.rerun()
                
                # Delete Button (Accessing the correct key: 'ID')
                if row_cols[-1].button("🗑️", key=f"delete_patient_{row['ID']}"):
                    patient_id_to_delete = row['ID']
                    patient_name = row['Name']
                    if st.session_state.get(f'confirm_delete_patient_{patient_id_to_delete}', False):
                        
                        # --- CASCADE DELETION ---
                        # 1. Clear Room Assignment
                        room_to_vacate = find_patient_room(patient_id_to_delete)
                        if room_to_vacate:
                            room_to_vacate['occupancy_status'] = 'Vacant'
                            room_to_vacate['patient_id'] = None
                        
                        # 2. Remove Patient Data from ALL lists
                        st.session_state.patients = [p for p in st.session_state.patients if p['patient_id'] != patient_id_to_delete]
                        st.session_state.billing = [b for b in st.session_state.billing if b['patient_id'] != patient_id_to_delete]
                        st.session_state.appointments = [a for a in st.session_state.appointments if a['patient_id'] != patient_id_to_delete]
                        st.session_state.treatment_plans = [t for t in st.session_state.treatment_plans if t['patient_id'] != patient_id_to_delete]
                        st.session_state.diagnosis = [d for d in st.session_state.diagnosis if d['patient_id'] != patient_id_to_delete]
                        
                        save_data_to_backend() # <--- NEW: Save to backend after deletion
                        
                        st.success(f"Patient {patient_name} and ALL associated records deleted successfully.")
                        st.session_state.pop(f'confirm_delete_patient_{patient_id_to_delete}')
                        st.rerun()
                    else:
                        st.session_state[f'confirm_delete_patient_{patient_id_to_delete}'] = True
                        st.warning(f"Click Delete again to confirm deleting **{patient_name}** and **all associated records**.")
                        
        else:
            st.info("No patient records found.")

# Doctors page (same as before)
def show_doctors():
    st.markdown('<h1 class="main-header">Doctor Management</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add New Doctor", use_container_width=True):
            st.session_state.show_doctor_form = True
            st.session_state.edit_doctor_id = None
            st.rerun()
    
    # Form Handler
    def doctor_form_handler(edit_doctor=None):
        if edit_doctor:
            st.subheader(f"Edit Doctor: {edit_doctor['name']}")
            defaults = edit_doctor
        else:
            st.subheader("Add New Doctor")
            defaults = {"name": "", "degree": "", "specialization": "", "contact": ""}

        with st.form("doctor_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name*", defaults['name'])
                degree = st.text_input("Degree*", defaults['degree'])
            with col2:
                specialization = st.text_input("Specialization*", defaults['specialization'])
                contact = st.text_input("Contact*", defaults['contact'])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(f"💾 {'Update' if edit_doctor else 'Save'} Doctor", use_container_width=True):
                    if not (name and specialization):
                        st.error("Name and Specialization are required.")
                        return

                    if edit_doctor:
                        doctor_index = next((i for i, d in enumerate(st.session_state.doctors) if d['doctor_id'] == edit_doctor['doctor_id']), -1)
                        if doctor_index != -1:
                            st.session_state.doctors[doctor_index].update({"name": name, "degree": degree, "specialization": specialization, "contact": contact})
                            st.success(f"Doctor {name} updated successfully!")
                    else:
                        new_id = max([d['doctor_id'] for d in st.session_state.doctors]) + 1 if st.session_state.doctors else 1
                        new_doctor = {"doctor_id": new_id, "name": name, "degree": degree, "specialization": specialization, "contact": contact}
                        st.session_state.doctors.append(new_doctor)
                        st.success(f"Doctor {name} added successfully!")
                        
                    save_data_to_backend() # <--- NEW: Save to backend after doctor update/creation
                        
                    st.session_state.show_doctor_form = False
                    st.session_state.edit_doctor_id = None
                    st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.show_doctor_form = False
                    st.session_state.edit_doctor_id = None
                    st.rerun()

    if st.session_state.get('show_doctor_form', False) or st.session_state.get('edit_doctor_id') is not None:
        doctor_to_edit = next((d for d in st.session_state.doctors if d['doctor_id'] == st.session_state.get('edit_doctor_id')), None)
        doctor_form_handler(doctor_to_edit)
    else:
        st.markdown("---")
        df = pd.DataFrame(st.session_state.doctors)
        if not df.empty:
            display_df = df[['doctor_id', 'name', 'degree', 'specialization', 'contact']].copy()
            display_df.columns = ['ID', 'Name', 'Degree', 'Specialization', 'Contact']
            
            col_list = st.columns(len(display_df.columns) + 2)
            for i, col_name in enumerate(display_df.columns):
                col_list[i].write(f"**{col_name}**")
            col_list[-2].write("**Edit**")
            col_list[-1].write("**Delete**")

            for i, row in display_df.iterrows():
                row_cols = st.columns(len(display_df.columns) + 2)
                for j, col_name in enumerate(display_df.columns):
                    row_cols[j].write(row[col_name])

                # Edit Button (Accessing the correct key: 'ID')
                if row_cols[-2].button("✏️", key=f"edit_doctor_{row['ID']}"):
                    st.session_state.edit_doctor_id = row['ID']
                    st.session_state.show_doctor_form = True
                    st.rerun()
                
                # Delete Button (Accessing the correct key: 'ID')
                if row_cols[-1].button("🗑️", key=f"delete_doctor_{row['ID']}"):
                    doctor_id_to_delete = row['ID']
                    if st.session_state.get(f'confirm_delete_doctor_{doctor_id_to_delete}', False):
                        st.session_state.doctors = [d for d in st.session_state.doctors if d['doctor_id'] != doctor_id_to_delete]
                        st.success(f"Doctor {row['Name']} deleted successfully.")
                        st.session_state.pop(f'confirm_delete_doctor_{doctor_id_to_delete}')
                        save_data_to_backend() # <--- NEW: Save to backend after deletion
                        st.rerun()
                    else:
                        st.session_state[f'confirm_delete_doctor_{doctor_id_to_delete}'] = True
                        st.warning(f"Click Delete again to confirm deleting **{row['Name']}**.")
        else:
            st.info("No doctor records found.")

# Rooms page (same as before)
def show_rooms():
    st.markdown('<h1 class="main-header">Room Management</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add New Room", use_container_width=True):
            st.session_state.show_room_form = True
            st.session_state.edit_room_id = None
            st.rerun()
    
    # Form Handler
    def room_form_handler(edit_room=None):
        if edit_room:
            st.subheader(f"Edit Room: {edit_room['room_id']}")
            defaults = edit_room
        else:
            st.subheader("Add New Room")
            defaults = {"room_id": max([r['room_id'] for r in st.session_state.rooms]) + 1 if st.session_state.rooms else 1, 
                        "room_type": "General", "occupancy_status": "Vacant", "cost_per_day": 5000.0}

        with st.form("room_form"):
            col1, col2 = st.columns(2)
            with col1:
                room_id = st.number_input("Room Number*", min_value=1, value=defaults['room_id'], disabled=bool(edit_room))
                room_type = st.selectbox("Room Type*", ["General", "Semi-Private", "Private", "ICU"], index=["General", "Semi-Private", "Private", "ICU"].index(defaults['room_type']))
            with col2:
                status = st.selectbox("Occupancy Status*", ["Vacant", "Occupied"], index=["Vacant", "Occupied"].index(defaults['occupancy_status']))
                cost = st.number_input("Cost Per Day (₹)*", min_value=1000.0, value=defaults['cost_per_day'], step=500.0)
            
            patient_id = None
            if status == 'Occupied':
                # Get all patients for selection
                patient_options = [p['patient_id'] for p in st.session_state.patients]
                
                # Determine default selection index
                default_patient_id = defaults.get('patient_id')
                try:
                    default_index = patient_options.index(default_patient_id) if default_patient_id in patient_options else 0
                except ValueError:
                    default_index = 0

                patient_id = st.selectbox("Occupied By Patient*", 
                                         options=patient_options,
                                         format_func=lambda x: get_patient_name(x),
                                         index=default_index)

            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(f"💾 {'Update' if edit_room else 'Save'} Room", use_container_width=True):
                    # Check for room ID duplication on Add
                    if not edit_room and any(r['room_id'] == room_id for r in st.session_state.rooms):
                        st.error(f"Room ID {room_id} already exists.")
                        return

                    new_room = {
                        "room_id": room_id, "room_type": room_type, "occupancy_status": status, 
                        "patient_id": patient_id if status == 'Occupied' else None, "cost_per_day": cost
                    }
                    
                    if edit_room:
                        room_index = next((i for i, r in enumerate(st.session_state.rooms) if r['room_id'] == edit_room['room_id']), -1)
                        if room_index != -1:
                            st.session_state.rooms[room_index].update(new_room)
                            st.success(f"Room {room_id} updated successfully!")
                    else:
                        st.session_state.rooms.append(new_room)
                        st.success(f"Room {room_id} added successfully!")

                    save_data_to_backend() # <--- NEW: Save to backend after room update/creation

                    st.session_state.show_room_form = False
                    st.session_state.edit_room_id = None
                    st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.show_room_form = False
                    st.session_state.edit_room_id = None
                    st.rerun()

    if st.session_state.get('show_room_form', False) or st.session_state.get('edit_room_id') is not None:
        room_to_edit = next((r for r in st.session_state.rooms if r['room_id'] == st.session_state.get('edit_room_id')), None)
        room_form_handler(room_to_edit)
    else:
        st.markdown("---")
        df = pd.DataFrame(st.session_state.rooms)
        if not df.empty:
            df['Patient'] = df['patient_id'].apply(lambda x: get_patient_name(x) if x else 'N/A')
            df['Cost/Day'] = df['cost_per_day'].apply(lambda x: f"₹{x:,.0f}")
            display_df = df[['room_id', 'room_type', 'occupancy_status', 'Patient', 'Cost/Day']].copy()
            display_df.columns = ['Room ID', 'Type', 'Status', 'Patient', 'Cost/Day']
            
            col_list = st.columns(len(display_df.columns) + 2)
            for i, col_name in enumerate(display_df.columns):
                col_list[i].write(f"**{col_name}**")
            col_list[-2].write("**Edit**")
            col_list[-1].write("**Delete**")

            for i, row in display_df.iterrows():
                row_cols = st.columns(len(display_df.columns) + 2)
                for j, col_name in enumerate(display_df.columns):
                    row_cols[j].write(row[col_name])

                # Edit Button (Accessing the correct key: 'Room ID')
                if row_cols[-2].button("✏️", key=f"edit_room_{row['Room ID']}"):
                    st.session_state.edit_room_id = row['Room ID']
                    st.session_state.show_room_form = True
                    st.rerun()
                
                # Delete Button (Accessing the correct key: 'Room ID')
                if row_cols[-1].button("🗑️", key=f"delete_room_{row['Room ID']}"):
                    room_id_to_delete = row['Room ID']
                    if row['Status'] == 'Occupied':
                        st.error("Cannot delete an occupied room. Please discharge the patient first.")
                    elif st.session_state.get(f'confirm_delete_room_{room_id_to_delete}', False):
                        st.session_state.rooms = [r for r in st.session_state.rooms if r['room_id'] != room_id_to_delete]
                        st.success(f"Room {room_id_to_delete} deleted successfully.")
                        st.session_state.pop(f'confirm_delete_room_{room_id_to_delete}')
                        save_data_to_backend() # <--- NEW: Save to backend after deletion
                        st.rerun()
                    else:
                        st.session_state[f'confirm_delete_room_{room_id_to_delete}'] = True
                        st.warning(f"Click Delete again to confirm deleting **Room {row['Room ID']}**.")
        else:
            st.info("No room records found.")

# Function to generate the patient summary table
def generate_patient_summary(df_filtered, patient_name):
    st.subheader(f"Account Summary for {patient_name}")
    
    if df_filtered.empty:
        st.info(f"No billing history found for {patient_name}.")
        return

    # Calculate Totals
    total_billed = df_filtered['amount'].sum()
    total_paid = df_filtered[df_filtered['status'] == 'Paid']['amount'].sum()
    total_unpaid = total_billed - total_paid

    # Create Summary DataFrame
    summary_data = {
        'Metric': ['Total Billed', 'Total Paid', 'Total Outstanding'],
        'Amount': [total_billed, total_paid, total_unpaid],
        'Status': ['Billed', 'Paid', 'Unpaid']
    }
    df_summary = pd.DataFrame(summary_data)
    
    # Format amount column
    df_summary['Amount'] = df_summary['Amount'].apply(lambda x: f"₹{x:,.2f}")

    # Display the summary table
    st.dataframe(df_summary, use_container_width=True, hide_index=True)

# Billing page
def show_billing():
    st.markdown('<h1 class="main-header">Billing & Payments</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add New Bill", use_container_width=True):
            st.session_state.show_billing_form = True
            st.session_state.edit_bill_id = None
            st.rerun()
    
    # --- Bill Concatenation/Filtering Feature ---
    st.markdown("---")
    
    patient_ids = [p['patient_id'] for p in st.session_state.patients]
    patient_names = [get_patient_name(p_id) for p_id in patient_ids]
    patient_selection_map = {name: id for name, id in zip(patient_names, patient_ids)}
    
    # Add 'All Patients' option
    display_options = ['All Bills (All Patients)'] + patient_names
    selected_name = st.selectbox("Select Patient for Account Statement", display_options, index=0)
    
    if selected_name == 'All Bills (All Patients)':
        filtered_bills = st.session_state.billing
    else:
        selected_id = patient_selection_map[selected_name]
        filtered_bills = [b for b in st.session_state.billing if b['patient_id'] == selected_id]
        
        # Display Patient Summary Metrics
        df_filtered = pd.DataFrame(filtered_bills)
        generate_patient_summary(df_filtered, selected_name)
        st.markdown("---")
        st.subheader(f"Detailed Transactions for {selected_name}")

    # Form Handler (same as before)
    def billing_form_handler(edit_bill=None):
        if edit_bill:
            st.subheader(f"Edit Bill: {edit_bill['bill_id']}")
            defaults = edit_bill
        else:
            st.subheader("Add New Bill")
            defaults = {"patient_id": st.session_state.patients[0]['patient_id'], "amount": 5000.0, "date": datetime.now().date(), "status": "Unpaid", "description": ""}

        with st.form("billing_form"):
            patient_id = st.selectbox("Patient*", 
                                     options=[p['patient_id'] for p in st.session_state.patients],
                                     format_func=lambda x: get_patient_name(x),
                                     index=[p['patient_id'] for p in st.session_state.patients].index(defaults['patient_id']))
            
            col1, col2 = st.columns(2)
            with col1:
                amount = st.number_input("Amount (₹)*", min_value=100.0, value=defaults['amount'], step=100.0)
            with col2:
                date = st.date_input("Date Issued*", value=datetime.strptime(defaults['date'], "%Y-%m-%d").date() if isinstance(defaults['date'], str) else defaults['date'])
            
            description = st.text_area("Description/Service*", defaults['description'])
            status = st.selectbox("Status*", ["Unpaid", "Paid"], index=["Unpaid", "Paid"].index(defaults['status']))
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(f"💾 {'Update' if edit_bill else 'Save'} Bill", use_container_width=True):
                    new_bill = {
                        "patient_id": patient_id, "amount": amount, "status": status, 
                        "date": date.strftime("%Y-%m-%d"), "description": description
                    }
                    
                    if edit_bill:
                        bill_index = next((i for i, b in enumerate(st.session_state.billing) if b['bill_id'] == edit_bill['bill_id']), -1)
                        if bill_index != -1:
                            st.session_state.billing[bill_index].update(new_bill)
                            st.success("Bill updated successfully!")
                    else:
                        new_id = max([b['bill_id'] for b in st.session_state.billing]) + 1 if st.session_state.billing else 1
                        new_bill['bill_id'] = new_id
                        st.session_state.billing.append(new_bill)
                        st.success("Bill added successfully!")

                    save_data_to_backend() # <--- NEW: Save to backend after billing update/creation

                    st.session_state.show_billing_form = False
                    st.session_state.edit_bill_id = None
                    st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.show_billing_form = False
                    st.session_state.edit_bill_id = None
                    st.rerun()

    if st.session_state.get('show_billing_form', False) or st.session_state.get('edit_bill_id') is not None:
        bill_to_edit = next((b for b in st.session_state.billing if b['bill_id'] == st.session_state.get('edit_bill_id')), None)
        billing_form_handler(bill_to_edit)
    else:
        # Display the filtered/all bills
        df = pd.DataFrame(filtered_bills).sort_values(by='date', ascending=False)
        if not df.empty:
            df['Patient'] = df['patient_id'].apply(get_patient_name)
            df['Amount'] = df['amount'].apply(lambda x: f"₹{x:,.2f}")
            display_df = df[['bill_id', 'Patient', 'description', 'Amount', 'status', 'date']].copy()
            display_df.columns = ['Bill ID', 'Patient', 'Description', 'Amount', 'Status', 'Date']
            
            # Table display and CRUD buttons
            col_list = st.columns(len(display_df.columns) + 2)
            for i, col_name in enumerate(display_df.columns):
                col_list[i].write(f"**{col_name}**")
            col_list[-2].write("**Edit**")
            col_list[-1].write("**Delete**")

            for i, row in display_df.iterrows():
                row_cols = st.columns(len(display_df.columns) + 2)
                for j, col_name in enumerate(display_df.columns):
                    row_cols[j].write(row[col_name])

                # Edit Button (Accessing the correct key: 'Bill ID')
                if row_cols[-2].button("✏️", key=f"edit_bill_{row['Bill ID']}"):
                    st.session_state.edit_bill_id = row['Bill ID']
                    st.session_state.show_billing_form = True
                    st.rerun()
                
                # Delete Button (Accessing the correct key: 'Bill ID')
                if row_cols[-1].button("🗑️", key=f"delete_bill_{row['Bill ID']}"):
                    bill_id_to_delete = row['Bill ID'] # Use the correct column name
                    if st.session_state.get(f'confirm_delete_bill_{bill_id_to_delete}', False):
                        st.session_state.billing = [b for b in st.session_state.billing if b['bill_id'] != bill_id_to_delete]
                        st.success(f"Bill {bill_id_to_delete} deleted successfully.")
                        st.session_state.pop(f'confirm_delete_bill_{bill_id_to_delete}')
                        save_data_to_backend() # <--- NEW: Save to backend after deletion
                        st.rerun()
                    else:
                        st.session_state[f'confirm_delete_bill_{bill_id_to_delete}'] = True
                        st.warning(f"Click Delete again to confirm deleting **Bill {bill_id_to_delete}**.")
        else:
            if selected_name == 'All Bills (All Patients)':
                st.info(f"No billing records found.")

# Reports page (same as before)
def show_reports():
    st.markdown('<h1 class="main-header">Reports & Analytics</h1>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Patients", len(st.session_state.patients))
    
    with col2:
        st.metric("Total Doctors", len(st.session_state.doctors))
    
    with col3:
        total_revenue = sum(b['amount'] for b in st.session_state.billing if b['status'] == 'Paid')
        st.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    
    with col4:
        total_treatments = len(st.session_state.treatment_plans)
        st.metric("Total Treatments", total_treatments)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Monthly Patient Admissions")
        df_patients = pd.DataFrame(st.session_state.patients)
        
        if not df_patients.empty:
            df_patients['admission_date'] = df_patients['admission_date'].astype(str)
            df_patients['admission_date'] = pd.to_datetime(df_patients['admission_date'], errors='coerce')
            df_patients.dropna(subset=['admission_date'], inplace=True)
            df_patients['month_year'] = df_patients['admission_date'].dt.strftime('%Y-%m')
            df_patients['month_label'] = df_patients['admission_date'].dt.strftime('%b %Y')
            monthly_counts = df_patients.groupby(['month_year', 'month_label']).size().reset_index(name='count')
            monthly_counts = monthly_counts.sort_values('month_year')

            fig = px.bar(monthly_counts, x='month_label', y='count', color='count', 
                          color_discrete_sequence=[PRIMARY_COLOR]) # Use NEW color
            fig.update_layout(xaxis_title="Month", yaxis_title="Admissions", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No admissions data to display.")

    with col2:
        st.subheader("Revenue by Department (Simulated)")
        total_revenue = sum(b['amount'] for b in st.session_state.billing if b['status'] == 'Paid')
        revenue_data = {
            'Oncology': total_revenue * 0.4,
            'Pediatrics': total_revenue * 0.25,
            'Radiology': total_revenue * 0.15,
            'Surgery': total_revenue * 0.12,
            'Pathology': total_revenue * 0.08
        }
        fig = px.pie(values=list(revenue_data.values()), names=list(revenue_data.keys()),
                     color_discrete_sequence=px.colors.sequential.Teal) # Use NEW color
        st.plotly_chart(fig, use_container_width=True)

# Appointments page (FIXED: Added $1000 fee and auto-nav)
def show_appointments():
    st.markdown('<h1 class="main-header">Appointments</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Schedule Appointment", use_container_width=True):
            st.session_state.show_appointment_form = True
            st.session_state.edit_appointment_id = None
            st.rerun()
    
    # Form Handler
    def appointment_form_handler(edit_appointment=None):
        if edit_appointment:
            st.subheader(f"Edit Appointment: {edit_appointment['reason']} on {edit_appointment['date']}")
            defaults = edit_appointment
        else:
            st.subheader("Schedule Appointment")
            defaults = {"patient_id": st.session_state.patients[0]['patient_id'], 
                        "doctor_id": st.session_state.doctors[0]['doctor_id'], 
                        "date": datetime.now().date(), "time": datetime.now().time().replace(second=0, microsecond=0), "reason": ""}
        
        with st.form("appointment_form"):
            col1, col2 = st.columns(2)
            with col1:
                patient_id = st.selectbox("Patient*", 
                                         options=[p['patient_id'] for p in st.session_state.patients],
                                         format_func=lambda x: get_patient_name(x),
                                         index=[p['patient_id'] for p in st.session_state.patients].index(defaults['patient_id']))
                date = st.date_input("Date*", value=datetime.strptime(defaults['date'], "%Y-%m-%d").date() if isinstance(defaults['date'], str) else defaults['date'])
            with col2:
                doctor_id = st.selectbox("Doctor*", 
                                         options=[d['doctor_id'] for d in st.session_state.doctors],
                                         format_func=lambda x: get_doctor_name(x),
                                         index=[d['doctor_id'] for d in st.session_state.doctors].index(defaults['doctor_id']))
                time = st.time_input("Time*", value=datetime.strptime(defaults['time'], "%H:%M").time() if isinstance(defaults['time'], str) else defaults['time'])
            
            reason = st.text_area("Reason*", defaults['reason'])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(f"💾 {'Update' if edit_appointment else 'Schedule'}", use_container_width=True):
                    new_appointment = {
                        "patient_id": patient_id, "doctor_id": doctor_id, 
                        "date": date.strftime("%Y-%m-%d"), "time": time.strftime("%H:%M"), "reason": reason
                    }
                    
                    if edit_appointment:
                        app_index = next((i for i, a in enumerate(st.session_state.appointments) if a['appointment_id'] == edit_appointment['appointment_id']), -1)
                        if app_index != -1:
                            st.session_state.appointments[app_index].update(new_appointment)
                            st.success("Appointment updated successfully!")
                    else:
                        new_id = max([a['appointment_id'] for a in st.session_state.appointments]) + 1 if st.session_state.appointments else 1
                        new_appointment['appointment_id'] = new_id
                        st.session_state.appointments.append(new_appointment)
                        st.success("Appointment scheduled successfully!")
                        
                        # NEW: AUTO-BILLING for Appointment
                        appointment_fee = 1000.00
                        add_auto_bill_entry(patient_id, "Appointment Fee", appointment_fee, 
                                            datetime.now().strftime("%Y-%m-%d"), 
                                            f"Consultation with {get_doctor_name(doctor_id)}")
                        st.session_state.menu = "Billing" # <--- Automated Navigation

                    save_data_to_backend() # <--- NEW: Save to backend after appointment update/creation

                    st.session_state.show_appointment_form = False
                    st.session_state.edit_appointment_id = None
                    st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.show_appointment_form = False
                    st.session_state.edit_appointment_id = None
                    st.rerun()

    if st.session_state.get('show_appointment_form', False) or st.session_state.get('edit_appointment_id') is not None:
        appointment_to_edit = next((a for a in st.session_state.appointments if a['appointment_id'] == st.session_state.get('edit_appointment_id')), None)
        appointment_form_handler(appointment_to_edit)
    else:
        st.markdown("---")
        df = pd.DataFrame(st.session_state.appointments)
        if not df.empty:
            df['Patient'] = df['patient_id'].apply(get_patient_name)
            df['Doctor'] = df['doctor_id'].apply(get_doctor_name)
            display_df = df[['appointment_id', 'date', 'time', 'reason', 'Doctor', 'Patient']].copy()
            display_df.columns = ['ID', 'Date', 'Time', 'Reason', 'Doctor', 'Patient']
            
            col_list = st.columns(len(display_df.columns) + 2)
            for i, col_name in enumerate(display_df.columns):
                col_list[i].write(f"**{col_name}**")
            col_list[-2].write("**Edit**")
            col_list[-1].write("**Delete**")

            for i, row in display_df.iterrows():
                row_cols = st.columns(len(display_df.columns) + 2)
                for j, col_name in enumerate(display_df.columns):
                    row_cols[j].write(row[col_name])

                # Edit Button (Accessing the correct key: 'ID')
                if row_cols[-2].button("✏️", key=f"edit_appointment_{row['ID']}"):
                    st.session_state.edit_appointment_id = row['ID']
                    st.session_state.show_appointment_form = True
                    st.rerun()
                
                # Delete Button (Accessing the correct key: 'ID')
                if row_cols[-1].button("🗑️", key=f"delete_appointment_{row['ID']}"):
                    appointment_id_to_delete = row['ID']
                    if st.session_state.get(f'confirm_delete_appointment_{appointment_id_to_delete}', False):
                        st.session_state.appointments = [a for a in st.session_state.appointments if a['appointment_id'] != appointment_id_to_delete]
                        st.success(f"Appointment {appointment_id_to_delete} deleted successfully.")
                        st.session_state.pop(f'confirm_delete_appointment_{appointment_id_to_delete}')
                        save_data_to_backend() # <--- NEW: Save to backend after deletion
                        st.rerun()
                    else:
                        st.session_state[f'confirm_delete_appointment_{appointment_id_to_delete}'] = True
                        st.warning(f"Click Delete again to confirm deleting **Appointment {row['ID']}**.")
        else:
            st.info("No appointment records found.")

# Treatment Plans page (FIXED: KeyError)
def show_treatment():
    st.markdown('<h1 class="main-header">Treatment Plans</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add Treatment Plan", use_container_width=True):
            st.session_state.show_treatment_form = True
            st.session_state.edit_plan_id = None
            st.rerun()

    # Form Handler
    def treatment_form_handler(edit_plan=None):
        if edit_plan:
            st.subheader(f"Edit Treatment Plan: {edit_plan['plan_id']}")
            defaults = edit_plan
        else:
            st.subheader("Add Treatment Plan")
            defaults = {"patient_id": st.session_state.patients[0]['patient_id'], 
                        "doctor_id": st.session_state.doctors[0]['doctor_id'], 
                        "start_date": datetime.now().date(), "end_date": None, "details": ""}

        with st.form("treatment_form"):
            col1, col2 = st.columns(2)
            with col1:
                patient_id = st.selectbox("Patient*", 
                                         options=[p['patient_id'] for p in st.session_state.patients],
                                         format_func=lambda x: get_patient_name(x),
                                         index=[p['patient_id'] for p in st.session_state.patients].index(defaults['patient_id']))
                start_date = st.date_input("Start Date*", value=datetime.strptime(defaults['start_date'], "%Y-%m-%d").date() if isinstance(defaults['start_date'], str) else defaults['start_date'])
            with col2:
                doctor_id = st.selectbox("Doctor*", 
                                         options=[d['doctor_id'] for d in st.session_state.doctors],
                                         format_func=lambda x: get_doctor_name(x),
                                         index=[d['doctor_id'] for d in st.session_state.doctors].index(defaults['doctor_id']))
                end_date = st.date_input("End Date (Expected)", value=datetime.strptime(defaults['end_date'], "%Y-%m-%d").date() if isinstance(defaults['end_date'], str) and defaults['end_date'] else None)
            
            details = st.text_area("Details / Chemotherapy Protocol*", defaults['details'])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(f"💾 {'Update' if edit_plan else 'Save'} Plan", use_container_width=True):
                    
                    related_diag = next((d for d in st.session_state.diagnosis if d['patient_id'] == patient_id), None)
                    diagnosis_id = related_diag['diagnosis_id'] if related_diag else None
                    
                    new_plan = {
                        "patient_id": patient_id, "doctor_id": doctor_id, "diagnosis_id": diagnosis_id, 
                        "details": details, "start_date": start_date.strftime("%Y-%m-%d"), 
                        "end_date": end_date.strftime("%Y-%m-%d") if end_date else None
                    }
                    
                    if edit_plan:
                        plan_index = next((i for i, t in enumerate(st.session_state.treatment_plans) if t['plan_id'] == edit_plan['plan_id']), -1)
                        if plan_index != -1:
                            st.session_state.treatment_plans[plan_index].update(new_plan)
                            st.success("Treatment plan updated successfully!")
                    else:
                        new_id = max([t['plan_id'] for t in st.session_state.treatment_plans]) + 1 if st.session_state.treatment_plans else 1
                        new_plan['plan_id'] = new_id
                        st.session_state.treatment_plans.append(new_plan)
                        
                        # AUTO-BILLING
                        add_auto_bill_entry(patient_id, "Treatment Plan", 10000.00, datetime.now().strftime("%Y-%m-%d"), details.split('\n')[0])
                        st.session_state.menu = "Billing" # <--- Automated Navigation
                        
                    save_data_to_backend() # <--- NEW: Save to backend after plan update/creation
                        
                    st.session_state.show_treatment_form = False
                    st.session_state.edit_plan_id = None
                    st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.show_treatment_form = False
                    st.session_state.edit_plan_id = None
                    st.rerun()

    if st.session_state.get('show_treatment_form', False) or st.session_state.get('edit_plan_id') is not None:
        plan_to_edit = next((t for t in st.session_state.treatment_plans if t['plan_id'] == st.session_state.get('edit_plan_id')), None)
        treatment_form_handler(plan_to_edit)
    else:
        st.markdown("---")
        df = pd.DataFrame(st.session_state.treatment_plans)
        if not df.empty:
            df['Patient'] = df['patient_id'].apply(get_patient_name)
            df['Doctor'] = df['doctor_id'].apply(get_doctor_name)
            display_df = df[['plan_id', 'Patient', 'Doctor', 'start_date', 'end_date', 'details']].copy()
            # Renamed 'plan_id' to 'Plan ID'
            display_df.columns = ['Plan ID', 'Patient', 'Doctor', 'Start Date', 'End Date', 'Details']
            
            col_list = st.columns(len(display_df.columns) + 2)
            for i, col_name in enumerate(display_df.columns):
                col_list[i].write(f"**{col_name}**")
            col_list[-2].write("**Edit**")
            col_list[-1].write("**Delete**")

            for i, row in display_df.iterrows():
                row_cols = st.columns(len(display_df.columns) + 2)
                for j, col_name in enumerate(display_df.columns):
                    row_cols[j].write(row[col_name])

                # FIX APPLIED HERE: Accessing 'Plan ID'
                if row_cols[-2].button("✏️", key=f"edit_plan_{row['Plan ID']}"):
                    st.session_state.edit_plan_id = row['Plan ID']
                    st.session_state.show_treatment_form = True
                    st.rerun()
                
                # FIX APPLIED HERE: Accessing 'Plan ID'
                if row_cols[-1].button("🗑️", key=f"delete_plan_{row['Plan ID']}"):
                    plan_id_to_delete = row['Plan ID']
                    if st.session_state.get(f'confirm_delete_plan_{plan_id_to_delete}', False):
                        st.session_state.treatment_plans = [t for t in st.session_state.treatment_plans if t['plan_id'] != plan_id_to_delete]
                        st.success(f"Treatment Plan {plan_id_to_delete} deleted successfully.")
                        st.session_state.pop(f'confirm_delete_plan_{plan_id_to_delete}')
                        save_data_to_backend() # <--- NEW: Save to backend after deletion
                        st.rerun()
                    else:
                        st.session_state[f'confirm_delete_plan_{plan_id_to_delete}'] = True
                        st.warning(f"Click Delete again to confirm deleting **Plan {plan_id_to_delete}**.")
        else:
            st.info("No treatment plan records found.")

# Diagnosis page (same as before, uses auto-nav)
def show_diagnosis():
    st.markdown('<h1 class="main-header">Diagnosis Records</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add Diagnosis", use_container_width=True):
            st.session_state.show_diagnosis_form = True
            st.session_state.edit_diagnosis_id = None
            st.rerun()

    # Form Handler
    def diagnosis_form_handler(edit_diagnosis=None):
        if edit_diagnosis:
            st.subheader(f"Edit Diagnosis: {edit_diagnosis['diagnosis_id']}")
            defaults = edit_diagnosis
        else:
            st.subheader("Add Diagnosis Record")
            defaults = {"patient_id": st.session_state.patients[0]['patient_id'], "diagnosis_type": "Blood", 
                        "disease_type": "", "date": datetime.now().date(), "result": "", "description": ""}

        with st.form("diagnosis_form"):
            col1, col2 = st.columns(2)
            with col1:
                patient_id = st.selectbox("Patient*", 
                                         options=[p['patient_id'] for p in st.session_state.patients],
                                         format_func=lambda x: get_patient_name(x),
                                         index=[p['patient_id'] for p in st.session_state.patients].index(defaults['patient_id']))
                diagnosis_type = st.selectbox("Diagnosis Type*", ["Blood", "Scan", "Biopsy", "Other"], index=["Blood", "Scan", "Biopsy", "Other"].index(defaults['diagnosis_type']))
            with col2:
                disease_type = st.text_input("Disease Type*", placeholder="e.g., Leukemia, Lymphoma", value=defaults['disease_type'])
                date = st.date_input("Date*", value=datetime.strptime(defaults['date'], "%Y-%m-%d").date() if isinstance(defaults['date'], str) else defaults['date'])
            
            result = st.text_area("Result*", defaults['result'])
            description = st.text_input("Description (Optional)", value=defaults['description'])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button(f"💾 {'Update' if edit_diagnosis else 'Save'} Diagnosis", use_container_width=True):
                    
                    new_diagnosis = {
                        "patient_id": patient_id, "diagnosis_type": diagnosis_type, 
                        "disease_type": disease_type, "date": date.strftime("%Y-%m-%d"), 
                        "result": result, "description": description
                    }
                    
                    if edit_diagnosis:
                        diag_index = next((i for i, d in enumerate(st.session_state.diagnosis) if d['diagnosis_id'] == edit_diagnosis['diagnosis_id']), -1)
                        if diag_index != -1:
                            st.session_state.diagnosis[diag_index].update(new_diagnosis)
                            st.success("Diagnosis record updated successfully!")
                    else:
                        new_id = max([d['diagnosis_id'] for d in st.session_state.diagnosis]) + 1 if st.session_state.diagnosis else 1
                        new_diagnosis['diagnosis_id'] = new_id
                        st.session_state.diagnosis.append(new_diagnosis)
                        
                        # AUTO-BILLING (Simulated cost for diagnosis)
                        add_auto_bill_entry(patient_id, "Diagnosis", 5000.00, datetime.now().strftime("%Y-%m-%d"), f"{disease_type} - {diagnosis_type}")
                        st.session_state.menu = "Billing" # <--- Automated Navigation

                    save_data_to_backend() # <--- NEW: Save to backend after diagnosis update/creation

                    st.session_state.show_diagnosis_form = False
                    st.session_state.edit_diagnosis_id = None
                    st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.show_diagnosis_form = False
                    st.session_state.edit_diagnosis_id = None
                    st.rerun()
    
    if st.session_state.get('show_diagnosis_form', False) or st.session_state.get('edit_diagnosis_id') is not None:
        diagnosis_to_edit = next((d for d in st.session_state.diagnosis if d['diagnosis_id'] == st.session_state.get('edit_diagnosis_id')), None)
        diagnosis_form_handler(diagnosis_to_edit)
    else:
        st.markdown("---")
        df = pd.DataFrame(st.session_state.diagnosis)
        if not df.empty:
            df['Patient'] = df['patient_id'].apply(get_patient_name)
            display_df = df[['diagnosis_id', 'Patient', 'diagnosis_type', 'disease_type', 'date', 'result']].copy()
            display_df.columns = ['ID', 'Patient', 'Type', 'Disease Type', 'Date', 'Result']
            
            col_list = st.columns(len(display_df.columns) + 2)
            for i, col_name in enumerate(display_df.columns):
                col_list[i].write(f"**{col_name}**")
            col_list[-2].write("**Edit**")
            col_list[-1].write("**Delete**")

            for i, row in display_df.iterrows():
                row_cols = st.columns(len(display_df.columns) + 2)
                for j, col_name in enumerate(display_df.columns):
                    row_cols[j].write(row[col_name])

                # Edit Button (Accessing the correct key: 'ID')
                if row_cols[-2].button("✏️", key=f"edit_diagnosis_{row['ID']}"):
                    st.session_state.edit_diagnosis_id = row['ID']
                    st.session_state.show_diagnosis_form = True
                    st.rerun()
                
                # Delete Button (Accessing the correct key: 'ID')
                if row_cols[-1].button("🗑️", key=f"delete_diagnosis_{row['ID']}"):
                    diagnosis_id_to_delete = row['ID']
                    if st.session_state.get(f'confirm_delete_diagnosis_{diagnosis_id_to_delete}', False):
                        st.session_state.diagnosis = [d for d in st.session_state.diagnosis if d['diagnosis_id'] != diagnosis_id_to_delete]
                        st.success(f"Diagnosis Record {diagnosis_id_to_delete} deleted successfully.")
                        st.session_state.pop(f'confirm_delete_diagnosis_{diagnosis_id_to_delete}')
                        save_data_to_backend() # <--- NEW: Save to backend after deletion
                        st.rerun()
                    else:
                        st.session_state[f'confirm_delete_diagnosis_{diagnosis_id_to_delete}'] = True
                        st.warning(f"Click Delete again to confirm deleting **Record {row['ID']}**.")
        else:
            st.info("No diagnosis records found.")

# Data Management (Procedure Only Demo)
def show_data_management():
    st.markdown('<h1 class="main-header">Data Management</h1>', unsafe_allow_html=True)
    
    # --- Row 1: System Procedure Testing ---
    st.subheader("System Procedure Testing")
    st.caption("A **Procedure** executes logic that modifies the application's internal data (state) and saves to the persistent backend.")
    
    demo_patient_id = st.selectbox("Select Patient for Procedure:", options=[p['patient_id'] for p in st.session_state.patients], 
                                   format_func=lambda x: f"ID {x}: {get_patient_name(x)}", key="proc_patient_select")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("#### Procedure: Admin Fee Application")
        admin_fee = st.number_input("Admin Fee to add (₹):", min_value=100.0, value=2500.0, step=100.0, key="proc_fee")
        
        if st.button("▶️ Execute Procedure (Updates Billing List)", key="run_proc_demo", use_container_width=True):
            # Trigger: Button Click
            # PROCEDURE CALL (Side effect: changes st.session_state.billing, calls save_data_to_backend, and redirects)
            add_auto_bill_entry(demo_patient_id, "Admin Fee", admin_fee, datetime.now().strftime("%Y-%m-%d"), "Demonstration of a side-effect") 
            # Note: st.toast() inside add_auto_bill_entry will display the message
            st.session_state.menu = "Billing"
            st.rerun()
    
    st.markdown("---")

    # --- Row 2: Data Metrics / Chart ---
    st.subheader("Current Data Statistics")
    
    data_counts = {
        'Patients': len(st.session_state.patients),
        'Doctors': len(st.session_state.doctors),
        'Rooms': len(st.session_state.rooms),
        'Appointments': len(st.session_state.appointments),
        'Treatment Plans': len(st.session_state.treatment_plans),
        'Diagnosis Records': len(st.session_state.diagnosis),
        'Billing Records': len(st.session_state.billing)
    }
    df_metrics = pd.DataFrame(data_counts.items(), columns=['Data Type', 'Count'])
    
    col_metrics, col_chart = st.columns([1, 2])
    
    with col_metrics:
        # Display as key metrics/info boxes
        for dtype, count in data_counts.items():
            st.info(f"**{dtype}:** {count}")
        
    with col_chart:
        # Reinstated Chart (Data Distribution)
        fig = px.bar(df_metrics, x='Data Type', y='Count', 
                     color='Data Type', 
                     color_discrete_sequence=px.colors.sequential.Teal,
                     title="Record Distribution Across the System")
        fig.update_layout(xaxis_title="", yaxis_title="Total Count")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    
    # --- Row 3: Import/Export Utilities ---
    st.subheader("Export & Import Utilities")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📥 Load Sample Data", use_container_width=True):
            if st.session_state.get('confirm_load', False):
                init_sample_data()
                st.session_state.confirm_load = False
                st.success("Sample data loaded successfully!")
                st.rerun()
            else:
                st.session_state.confirm_load = True
                st.warning("Click again to confirm")
    
    with col2:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            if st.session_state.get('confirm_clear', False):
                st.session_state.patients = []
                st.session_state.doctors = []
                st.session_state.rooms = []
                st.session_state.appointments = []
                st.session_state.treatment_plans = []
                st.session_state.diagnosis = []
                st.session_state.billing = []
                st.session_state.confirm_clear = False
                save_data_to_backend() # <--- NEW: Save empty lists to backend after clearing
                st.success("All data cleared!")
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm")
    
    with col3:
        # Export data
        export_data = {
            "patients": st.session_state.patients,
            "doctors": st.session_state.doctors,
            "rooms": st.session_state.rooms,
            "appointments": st.session_state.appointments,
            "treatment_plans": st.session_state.treatment_plans,
            "diagnosis": st.session_state.diagnosis,
            "billing": st.session_state.billing,
            "exportDate": datetime.now().isoformat()
        }
        
        st.download_button(
            label="📤 Export Data",
            data=json.dumps(export_data, indent=2),
            file_name=f"poms_data_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col4:
        uploaded_file = st.file_uploader("📥 Import Data", type=['json'], label_visibility="collapsed")
        if uploaded_file is not None:
            try:
                import_data = json.load(uploaded_file)
                # Manually update session state with imported data
                st.session_state.patients = import_data.get('patients', [])
                st.session_state.doctors = import_data.get('doctors', [])
                st.session_state.rooms = import_data.get('rooms', [])
                st.session_state.appointments = import_data.get('appointments', [])
                st.session_state.treatment_plans = import_data.get('treatment_plans', [])
                st.session_state.diagnosis = import_data.get('diagnosis', [])
                st.session_state.billing = import_data.get('billing', [])
                
                st.session_state.initialized = True
                save_data_to_backend() # <--- NEW: Save imported data to backend
                st.success("Data imported and saved to backend successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error importing data: {str(e)}")

# Main app
def main():
    init_sample_data()
    
    # Sidebar
    with st.sidebar:
        
        st.title("POMS")
        st.caption("Pediatric Oncology Management System")
        st.markdown("---")
        
        # Define menu items without emojis
        menu_items = [
            "Dashboard", 
            "Patients", 
            "Doctors", 
            "Appointments", 
            "Treatment Plans", 
            "Diagnosis", 
            "Rooms", 
            "Billing", 
            "Reports", 
            "Data Management"
        ]
        
        # Use st.session_state.menu to control the selected radio button
        menu = st.radio(
            "Navigation",
            menu_items,
            label_visibility="collapsed",
            index=menu_items.index(st.session_state.menu),
            key='app_menu_radio' # Assign a key to prevent conflicts
        )
        
        # Update the session state menu variable on radio selection change
        st.session_state.menu = menu
        
        st.markdown("---")
        st.markdown("### 👤 User Info")
        st.write("**Admin User**")
        st.caption("Administrator")
    
    # Main content based on menu selection
    if st.session_state.menu == "Dashboard":
        show_dashboard()
    elif st.session_state.menu == "Patients":
        show_patients()
    elif st.session_state.menu == "Doctors":
        show_doctors()
    elif st.session_state.menu == "Appointments":
        show_appointments()
    elif st.session_state.menu == "Treatment Plans":
        show_treatment()
    elif st.session_state.menu == "Diagnosis":
        show_diagnosis()
    elif st.session_state.menu == "Rooms":
        show_rooms()
    elif st.session_state.menu == "Billing":
        show_billing()
    elif st.session_state.menu == "Reports":
        show_reports()
    elif st.session_state.menu == "Data Management":
        show_data_management()

if __name__ == "__main__":
    main()
