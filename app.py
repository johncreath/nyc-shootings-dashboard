import streamlit as st
import pandas as pd

st.set_page_config(page_title="NYC Shootings Dashboard", layout="wide")

st.title("NYC Shootings Dashboard")

st.write("If you can see this, Streamlit is working.")

from src.load_data import load_data

df = load_data()

st.write(df.head())