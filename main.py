import streamlit as st
import pandas as pd
from io import BytesIO
import numpy as np

# Function to upload and merge Excel sheets
def upload_and_merge_excel():
    uploaded_files = st.file_uploader("Upload Excel files", type="xlsx", accept_multiple_files=True)
    if uploaded_files:
        dfs = []
        for file in uploaded_files:
            df = pd.read_excel(file)
            dfs.append(df)
        # Concatenate all dataframes
        merged_df = pd.concat(dfs, ignore_index=True)
        return merged_df
    return None

# Function to edit the merged dataframe
def edit_data(df):
    edited_df = st.experimental_data_editor(df, num_rows="dynamic")
    return edited_df

# Main Streamlit App
def main():
    st.title("Interactive Excel Merge and Edit")

    # Upload and merge Excel files
    merged_df = upload_and_merge_excel()

    if merged_df is not None:
        st.write("Merged Data Preview:")
        st.dataframe(merged_df)

        # Allow live editing of the merged data
        edited_df = edit_data(merged_df)

        if edited_df is not None:
            st.write("Edited Data:")
            st.dataframe(edited_df)

            # Allow to download the edited file
            if st.button('Download Edited File'):
                towrite = BytesIO()
                edited_df.to_excel(towrite, index=False)
                towrite.seek(0)
                st.download_button(label="Download Excel", data=towrite, file_name="edited_data.xlsx", mime="application/vnd.ms-excel")

if __name__ == "__main__":
    main()
