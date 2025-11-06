
# 🏥 POMS: Pediatric Oncology Management System

## 🌟 Project Overview

The Pediatric Oncology Management System (**POMS**) is a specialized digital platform designed to streamline the administrative and clinical data management workflows within a pediatric cancer ward. Built using Python and Streamlit, POMS centralizes records for patients, doctors, room assignments, treatment plans, diagnosis results, and billing. The system is designed to provide real-time reporting and maintain data integrity through controlled access and automated procedural logic.

## ✨ Features and Functionalities

POMS provides the following core capabilities, structured around the hospital's operational needs:

  * **Dashboard:** Provides key performance indicators (KPIs) like total patients, rooms occupied, and current appointments.
  * **Patient Management (CRUD):** Complete control over patient records, including admission, discharge, and assignment of an attending doctor.
  * **Clinical Records:** Dedicated modules for managing **Appointments**, **Diagnosis Records**, and **Treatment Plans**.
  * **Resource Management:** Tracks hospital **Rooms** (General, Private, ICU) and their current occupancy status.
  * **Billing & Finance:** Allows viewing patient account summaries and outstanding bills, supporting the **Paid/Unpaid** status update.
  * **System Procedure Testing:** Includes a dedicated screen in **Data Management** to demonstrate the automatic generation of bills (Procedure logic).

## 🛠️ Technical Stack

| Category | Component | Role |
| :--- | :--- | :--- |
| **Frontend/App Framework** | **Python** / **Streamlit** | Core application logic and user interface framework. |
| **Data Handling** | **Pandas** | Data structuring, manipulation, and processing. |
| **Visualization** | **Plotly Express** | Generating interactive charts for dashboards and reports. |
| **Database (Conceptual)** | **Python Lists/Dicts (Session State)** | Simulating the Relational Schema and persistent data storage. |

## 🚀 Setup and Run Instructions

### Prerequisites

1.  **Python:** Ensure you have Python 3.8+ installed.
2.  **Required Libraries:** Streamlit is the main framework.

### Installation

1.  **Save the Code:** Save the provided Python code as a file named `poms_app.py` (or any name, e.g., `hello2.py`).

2.  **Install Dependencies:** Open your terminal or command prompt and install the required libraries:

    ```bash
    pip install streamlit pandas plotly
    ```

### Running the Application

1.  Navigate to the directory where you saved the Python file.

2.  Run the application using the Streamlit command:

    ```bash
    streamlit run poms_app.py
    ```

3.  The application will automatically open in your web browser, loaded with the initial sample data.

## 💾 Conceptual Database Schema

The system relies on seven interconnected tables.

| Entity | Primary Key (PK) | Foreign Keys (FK) | Key Attributes |
| :--- | :--- | :--- | :--- |
| **Patient** | `patient_id` | `doctor_id` | name, diagnosis, admission\_date, status |
| **Doctor** | `doctor_id` | N/A | name, specialization |
| **Room** | `room_id` | `patient_id` (Unique) | room\_type, cost\_per\_day, occupancy\_status |
| **Appointment** | `appointment_id` | `patient_id`, `doctor_id` | date, time, reason |
| **Diagnosis** | `diagnosis_id` | `patient_id` | disease\_type, result |
| **Treatment\_Plan** | `plan_id` | `patient_id`, `doctor_id`, `diagnosis_id` | details, start\_date, end\_date |
| **Billing** | `bill_id` | `patient_id` | amount, status (Paid/Unpaid), description |

## 🔑 Key Database Logic Modeled in Python

The core database functionalities are modeled in Python functions:

| Logic Type | Modeled Function | Description in Code |
| :--- | :--- | :--- |
| **Procedure/Trigger** | `add_auto_bill_entry()` | Inserts a new row into the `Billing` list (side effect) and updates the UI instantly. |
| **Function** | `get_patient_name()` | Retrieves a single name string from the Patient list based on an ID. |
| **Cascade Delete** | Logic within `show_patients()` | Ensures that deleting a patient automatically removes associated records in Billing, Appointments, Treatment Plans, and clears their Room assignment. |
