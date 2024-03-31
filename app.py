import streamlit as st
import pandas as pd
import os.path

from util import filter_dataframe

def get_existing_sheets():
    folder_path = 'sheets/'
    return [os.path.splitext(file)[0] for file in os.listdir(folder_path) if file.endswith('.csv')]

def save_to_excel(df):
    df.to_excel(f'sheets/{st.session_state.selected_excel}.xlsx', index=False)

def client_data_entry_form():
    st.sidebar.header("Client Data Entry Form")
    # Add form elements here, like text inputs, dropdowns, etc.
    # For example:
    client_name = st.sidebar.text_input("Name")
    company_name = st.sidebar.text_input("Company Name")
    country_cd = st.sidebar.text_input("Country Cd", value="+91")
    contact_number = st.sidebar.text_input("Contact Number")
    email = st.sidebar.text_input("Email")
    address_line1 = st.sidebar.text_input("Address Line 1")
    address_line2 = st.sidebar.text_input("Address Line 2")
    city = st.sidebar.text_input("City")
    state = st.sidebar.text_input("State")
    pin_code = st.sidebar.text_input("PIN Code")
    country = st.sidebar.text_input("Country", value="India")
    # product_cat = st.sidebar.radio("Product Category", options=["SDS","Dry Wall","Anchor"])
    st.sidebar.subheader("Product Category")
    product_categories = ["SDS", "Dry Wall", "Anchor"]  # List of product_categories
    selected_interests = st.sidebar.multiselect(label="Product Categories",
                                                options=product_categories)  # To store selected product_categories
    # Add more fields as necessary

    # Add a submit button
    if st.sidebar.button("Submit"):
        data = {
            "Name": [client_name],
            "Company Name": [company_name],
            "Country Cd": [country_cd],
            "Contact Number": [contact_number],
            "Email": [email],
            "Address Line 1": [address_line1],
            "Address Line 2": [address_line2],
            "City": [city],
            "State": [state],
            "PinCode": [pin_code],
            "Country": [country],
            "Product Category": [",".join(selected_interests)]
        }

        # if 'dataframe' not in st.session_state:
        #     st.session_state.dataframe = pd.read_csv(f'sheets/{st.session_state.selected_excel}.csv')


        df = st.session_state.dataframe
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
        st.session_state.dataframe = df
        df.to_csv(f'sheets/{st.session_state.selected_excel}.csv', index=False)



def excel_viewer():
    # Get the selected sheet name
    # selected_sheet = st.session_state.selected_excel

    if 'modify' not in st.session_state:
        st.session_state.modify = False

    df = st.session_state.dataframe
    if not st.session_state.modify:
        df = filter_dataframe(df)
    edited_df = st.data_editor(df, use_container_width=True)
    st.session_state.dataframe = edited_df
    edited_df.to_csv(f'sheets/{st.session_state.selected_excel}.csv', index=False)



    # AgGrid(df)


# Truedef save_df():


# Create Streamlit app layout
st.title("Client Data Dashboard")

# if "dataframe" not in st.session_state:
#     st.session_state.dataframe = pd.dataframe()


with st.sidebar:
    client_data_entry_form()

xlsxs = get_existing_sheets()

if "xlsxlist" not in st.session_state:
    st.session_state.xlsxlist = xlsxs

if "selected_excel" not in st.session_state:
    st.session_state.selected_excel = "client-database"

if 'dataframe' not in st.session_state:
    st.session_state.dataframe = pd.read_csv(f'sheets/{st.session_state.selected_excel}.csv', dtype={'Country Cd':'string'})

st.session_state.selected_excel = st.selectbox(label="Select Excel Sheet:", options=st.session_state.xlsxlist, index=0)

excel_viewer()
