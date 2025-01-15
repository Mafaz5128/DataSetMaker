import streamlit as st
import pandas as pd
from io import BytesIO

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

# Function to edit data manually (edit rows and delete columns)
def edit_data(df):
    # Delete columns feature
    columns_to_delete = st.multiselect("Select columns to delete", df.columns)
    edited_df = df.drop(columns=columns_to_delete, errors='ignore')

    # Edit rows feature
    st.write("Edit rows:")
    edited_df_copy = edited_df.copy()
    
    # Loop through each row and allow user input for each column in the row
    for i in range(len(edited_df)):
        st.write(f"Row {i + 1}:")
        for col in edited_df.columns:
            edited_df_copy.at[i, col] = st.text_input(f"Edit {col} (Row {i + 1})", value=str(edited_df.at[i, col]), key=f"{col}_{i}")
    
    return edited_df_copy

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
