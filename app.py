import streamlit as st
import pandas as pd
import pyodbc

st.set_page_config(layout="wide")
st.title("รายงาน EA")

server_name = '10.1.55.58\DATAMART'
database_name = 'DB_EA'
username = 'sa'
password = 'P@$$w0rd'

conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)

AppStatue = pd.read_sql("SELECT distinct AppStatus FROM ea_monitor", conn)
ConStatue = pd.read_sql("SELECT distinct ContractStatus,ContractStatusId FROM ea_monitor where ContractStatus <> '' order by ContractStatusId", conn)
Flow = pd.read_sql("SELECT distinct Flow FROM ea_monitor where Flow <> ''", conn)
StrarBucketName = pd.read_sql("SELECT distinct StrarBucketName,StrarBucketId FROM ea_monitor where StrarBucketName <> '' order by StrarBucketId", conn)
CurrentBucketName = pd.read_sql("SELECT distinct CurrentBucketName,CurrentBucketId FROM ea_monitor where CurrentBucketName <> '' order by CurrentBucketId", conn)
conn.close()

params = []
col1, col2, col3 = st.columns(3)

with col1:
   ApplicationStatus = st.multiselect("สถานะ Application", AppStatue['AppStatus'].unique())
with col2:
   ContractStatus = st.multiselect("สถานะ Contract", ConStatue['ContractStatus'].unique())
with col3:
    FlowStatus = st.multiselect("Flow", Flow['Flow'].unique())

col1, col2 = st.columns(2)
with col1:
    StrarBucketName = st.multiselect("Bucket ณ สิ้นเดือนที่แล้ว", StrarBucketName['StrarBucketName'].unique())
with col2:
    CurrentBucketName = st.multiselect("Bucket ณ ปัจจุบัน", CurrentBucketName['CurrentBucketName'].unique())

Contract_filter = st.checkbox("สร้างสัญญาแล้ว")

conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}'
conn = pyodbc.connect(conn_str)

query = "SELECT * FROM ea_monitor WHERE 1=1"

if ApplicationStatus:
    query += f" AND AppStatus IN ({', '.join(['?'] * len(ApplicationStatus))})"
    params.extend(ApplicationStatus)

if ContractStatus:
    query += f" AND ContractStatus IN ({', '.join(['?'] * len(ContractStatus))})"
    params.extend(ContractStatus)

if FlowStatus:
    query += f" AND Flow IN ({', '.join(['?'] * len(FlowStatus))})"
    params.extend(FlowStatus)

if StrarBucketName:
    query += f" AND StrarBucketName IN ({', '.join(['?'] * len(StrarBucketName))})"
    params.extend(StrarBucketName)

if CurrentBucketName:
    query += f" AND CurrentBucketName IN ({', '.join(['?'] * len(CurrentBucketName))})"
    params.extend(CurrentBucketName)

if Contract_filter:
    query += " AND ContractNo <> ''"

df = pd.read_sql(query, conn, params=params)

# def apply_color(val):
#     if val == 'ค้าง 1 งวด':
#         return 'background-color: green;'
#     elif val == 'ค้าง 2 งวด':
#         return 'background-color: red;'


# Apply the style function to your DataFrame and display it
# styled_df = df.style.applymap(apply_color, subset=['CurrentBucketName'])
st.dataframe(df, height=1000)

st.markdown("""
    <style>
        div[data-widget-id="stDataFrame"] div[class^="stDataFrame"] {
            width: 1500px !important;
        }
    </style>
""", unsafe_allow_html=True)

conn.close()
