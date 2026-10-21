import streamlit as st
import pandas as pd
import io

st.set_page_config(
    page_title="Data Cleaning App",
    page_icon="🧹",
    layout="wide"
)

st.title(" Interactive Data Cleaning App")
st.write("Upload a CSV or Excel dataset to explore, clean, transform, and export your data.")

def get_sample_data():
    return pd.DataFrame({
        "Name": [" Alice ", "Bob", "Charlie", "Bob", None, "Eva "],
        "Age": [25, None, 30, 25, 22, 45],
        "Salary": [50000.0, 60000.0, None, 60000.0, 45000.0, 52000.0],
        "Department": ["HR", "IT", "Finance", "IT", "HR", None],
        "Join_Date": ["2022-01-10", "2021-05-23", "2020-03-15", "2021-05-23", "2023-11-01", "2019-07-19"]
    })

uploaded_file = st.sidebar.file_uploader("Upload Dataset (CSV or Excel)", type=["csv", "xlsx"])
load_sample = st.sidebar.button("Load Sample Dataset", use_container_width=True)

if uploaded_file is not None:
    if "current_file" not in st.session_state or st.session_state["current_file"] != uploaded_file.name:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.session_state["current_file"] = uploaded_file.name
            st.session_state["raw_df"] = df.copy()
            st.session_state["cleaned_df"] = df.copy()
        except Exception as e:
            st.sidebar.error(f"Error loading file: {e}")
elif load_sample:
    df = get_sample_data()
    st.session_state["current_file"] = "sample_data.csv"
    st.session_state["raw_df"] = df.copy()
    st.session_state["cleaned_df"] = df.copy()

if "cleaned_df" in st.session_state:
    if st.sidebar.button(" Reset to Original Data", use_container_width=True):
        st.session_state["cleaned_df"] = st.session_state["raw_df"].copy()
        st.rerun()

    df = st.session_state["cleaned_df"]
    raw_df = st.session_state["raw_df"]

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        " Overview & Quality",
        " Missing Values",
        " Duplicates & Text",
        " Column Management",
        " Export Cleaned Data"
    ])

    with tab1:
        st.subheader("Dataset Summary")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Rows", df.shape[0])
        m2.metric("Total Columns", df.shape[1])
        m3.metric("Missing Values", int(df.isnull().sum().sum()))
        m4.metric("Duplicate Rows", int(df.duplicated().sum()))

        st.subheader("Data Preview")
        st.dataframe(df, use_container_width=True)

        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("Missing Values by Column")
            missing_count = df.isnull().sum()
            missing_pct = (missing_count / len(df) * 100).round(2)
            missing_df = pd.DataFrame({"Missing Count": missing_count, "Percentage (%)": missing_pct})
            st.dataframe(missing_df, use_container_width=True)

        with col_right:
            st.subheader("Data Types & Non-Nulls")
            info_df = pd.DataFrame({
                "Data Type": df.dtypes.astype(str),
                "Non-Null Count": df.notnull().sum(),
                "Unique Values": df.nunique()
            })
            st.dataframe(info_df, use_container_width=True)

        st.subheader("Statistical Summary")
        st.dataframe(df.describe(include="all").fillna(""), use_container_width=True)

    with tab2:
        st.subheader("Handle Missing Values")
        action = st.radio("Choose Missing Value Action", ["Drop Missing Values", "Impute Single Column", "Bulk Imputation"], horizontal=True)

        if action == "Drop Missing Values":
            drop_mode = st.selectbox("Drop Mode", ["Drop rows with any missing values", "Drop rows where specific columns are missing", "Drop columns with missing values"])
            if drop_mode == "Drop rows with any missing values":
                if st.button("Drop All Rows with Nulls", type="primary"):
                    st.session_state["cleaned_df"] = df.dropna()
                    st.success("Dropped rows with missing values.")
                    st.rerun()
            elif drop_mode == "Drop rows where specific columns are missing":
                target_cols = st.multiselect("Select Columns to evaluate", df.columns.tolist())
                if st.button("Drop Selected Null Rows", type="primary"):
                    if target_cols:
                        st.session_state["cleaned_df"] = df.dropna(subset=target_cols)
                        st.success("Dropped selected rows.")
                        st.rerun()
                    else:
                        st.warning("Please select at least one column.")
            else:
                threshold = st.slider("Drop columns with missing percentage greater than", 0, 100, 50)
                if st.button("Drop Columns", type="primary"):
                    thresh_val = len(df) * (1 - threshold / 100)
                    st.session_state["cleaned_df"] = df.dropna(thresh=int(thresh_val), axis=1)
                    st.success("Dropped columns matching threshold.")
                    st.rerun()

        elif action == "Impute Single Column":
            col_to_impute = st.selectbox("Select Column to Impute", df.columns.tolist())
            is_numeric = pd.api.types.is_numeric_dtype(df[col_to_impute])

            if is_numeric:
                strategy = st.selectbox("Imputation Strategy", ["Mean", "Median", "Mode", "Custom Value"])
                custom_val = 0.0
                if strategy == "Custom Value":
                    custom_val = st.number_input("Enter numeric value", value=0.0)
                if st.button("Apply Imputation", type="primary"):
                    if strategy == "Mean":
                        st.session_state["cleaned_df"][col_to_impute] = df[col_to_impute].fillna(df[col_to_impute].mean())
                    elif strategy == "Median":
                        st.session_state["cleaned_df"][col_to_impute] = df[col_to_impute].fillna(df[col_to_impute].median())
                    elif strategy == "Mode":
                        mode_val = df[col_to_impute].mode()
                        if not mode_val.empty:
                            st.session_state["cleaned_df"][col_to_impute] = df[col_to_impute].fillna(mode_val[0])
                    else:
                        st.session_state["cleaned_df"][col_to_impute] = df[col_to_impute].fillna(custom_val)
                    st.success(f"Imputed column {col_to_impute}.")
                    st.rerun()
            else:
                strategy = st.selectbox("Imputation Strategy", ["Mode", "Custom String"])
                custom_str = "Missing"
                if strategy == "Custom String":
                    custom_str = st.text_input("Enter string replacement", value="Missing")
                if st.button("Apply Imputation", type="primary"):
                    if strategy == "Mode":
                        mode_val = df[col_to_impute].mode()
                        if not mode_val.empty:
                            st.session_state["cleaned_df"][col_to_impute] = df[col_to_impute].fillna(mode_val[0])
                    else:
                        st.session_state["cleaned_df"][col_to_impute] = df[col_to_impute].fillna(custom_str)
                    st.success(f"Imputed column {col_to_impute}.")
                    st.rerun()

        else:
            num_strategy = st.selectbox("Numeric Columns Strategy", ["Mean", "Median", "Zero"])
            cat_strategy = st.selectbox("Categorical Columns Strategy", ["Mode", "Missing"])
            if st.button("Apply Bulk Imputation", type="primary"):
                temp_df = df.copy()
                for col in temp_df.columns:
                    if pd.api.types.is_numeric_dtype(temp_df[col]):
                        if num_strategy == "Mean":
                            temp_df[col] = temp_df[col].fillna(temp_df[col].mean())
                        elif num_strategy == "Median":
                            temp_df[col] = temp_df[col].fillna(temp_df[col].median())
                        elif num_strategy == "Zero":
                            temp_df[col] = temp_df[col].fillna(0)
                    else:
                        if cat_strategy == "Mode":
                            col_mode = temp_df[col].mode()
                            if not col_mode.empty:
                                temp_df[col] = temp_df[col].fillna(col_mode[0])
                        elif cat_strategy == "Missing":
                            temp_df[col] = temp_df[col].fillna("Missing")
                st.session_state["cleaned_df"] = temp_df
                st.success("Bulk imputation completed.")
                st.rerun()

    with tab3:
        st.subheader("Duplicates Management")
        dup_count = int(df.duplicated().sum())
        st.write(f"Total Duplicate Rows Detected: **{dup_count}**")
        if dup_count > 0:
            if st.button("Remove All Duplicate Rows", type="primary"):
                st.session_state["cleaned_df"] = df.drop_duplicates()
                st.success("Duplicate rows removed.")
                st.rerun()
        else:
            st.info("No duplicate rows found.")

        st.divider()
        st.subheader("Text and String Cleaning")
        text_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()

        if text_cols:
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("Trim Whitespaces")
                if st.button("Trim Whitespaces on All Text Columns"):
                    temp_df = df.copy()
                    for c in text_cols:
                        temp_df[c] = temp_df[c].astype(str).str.strip().replace("nan", None)
                    st.session_state["cleaned_df"] = temp_df
                    st.success("Trimmed whitespaces.")
                    st.rerun()

            with col_b:
                st.write("Standardize Column Headers")
                if st.button("Clean Headers (Lowercase & Underscore)"):
                    temp_df = df.copy()
                    temp_df.columns = temp_df.columns.str.strip().str.lower().str.replace(" ", "_")
                    st.session_state["cleaned_df"] = temp_df
                    st.success("Standardized column headers.")
                    st.rerun()

            st.write("Change Case of a Column")
            target_text_col = st.selectbox("Select Text Column", text_cols)
            case_opt = st.selectbox("Select Case", ["lowercase", "UPPERCASE", "Title Case"])
            if st.button("Apply Case Transformation"):
                temp_df = df.copy()
                if case_opt == "lowercase":
                    temp_df[target_text_col] = temp_df[target_text_col].astype(str).str.lower()
                elif case_opt == "UPPERCASE":
                    temp_df[target_text_col] = temp_df[target_text_col].astype(str).str.upper()
                elif case_opt == "Title Case":
                    temp_df[target_text_col] = temp_df[target_text_col].astype(str).str.title()
                st.session_state["cleaned_df"] = temp_df
                st.success(f"Transformed {target_text_col} to {case_opt}.")
                st.rerun()
        else:
            st.info("No text columns found in dataset.")

    with tab4:
        st.subheader("Column Management")
        sub_c1, sub_c2 = st.columns(2)

        with sub_c1:
            st.write("Drop Columns")
            cols_to_drop = st.multiselect("Select Columns to Remove", df.columns.tolist())
            if st.button("Drop Selected Columns", type="primary"):
                if cols_to_drop:
                    st.session_state["cleaned_df"] = df.drop(columns=cols_to_drop)
                    st.success(f"Dropped columns: {cols_to_drop}")
                    st.rerun()
                else:
                    st.warning("Please select at least one column to drop.")

        with sub_c2:
            st.write("Rename Column")
            col_to_rename = st.selectbox("Select Column to Rename", df.columns.tolist())
            new_col_name = st.text_input("New Name", value=col_to_rename)
            if st.button("Rename Column"):
                if new_col_name and new_col_name != col_to_rename:
                    st.session_state["cleaned_df"] = df.rename(columns={col_to_rename: new_col_name})
                    st.success(f"Renamed {col_to_rename} to {new_col_name}.")
                    st.rerun()

        st.divider()
        st.subheader("Convert Column Data Types")
        target_convert_col = st.selectbox("Select Column to Convert", df.columns.tolist(), key="convert_col")
        target_type = st.selectbox("Select Target Type", ["int", "float", "string", "datetime"])

        if st.button("Convert Data Type"):
            temp_df = df.copy()
            try:
                if target_type == "int":
                    temp_df[target_convert_col] = pd.to_numeric(temp_df[target_convert_col], errors="coerce").astype("Int64")
                elif target_type == "float":
                    temp_df[target_convert_col] = pd.to_numeric(temp_df[target_convert_col], errors="coerce").astype(float)
                elif target_type == "string":
                    temp_df[target_convert_col] = temp_df[target_convert_col].astype(str)
                elif target_type == "datetime":
                    temp_df[target_convert_col] = pd.to_datetime(temp_df[target_convert_col], errors="coerce")
                st.session_state["cleaned_df"] = temp_df
                st.success(f"Converted {target_convert_col} to {target_type}.")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to convert column: {e}")

    with tab5:
        st.subheader("Data Cleaning Comparison")
        cmp1, cmp2, cmp3 = st.columns(3)
        cmp1.metric("Rows Change", f"{raw_df.shape[0]} → {df.shape[0]}", delta=df.shape[0] - raw_df.shape[0])
        cmp2.metric("Columns Change", f"{raw_df.shape[1]} → {df.shape[1]}", delta=df.shape[1] - raw_df.shape[1])
        cmp3.metric("Missing Values Removed", f"{int(raw_df.isnull().sum().sum())} → {int(df.isnull().sum().sum())}", delta=int(df.isnull().sum().sum()) - int(raw_df.isnull().sum().sum()))

        st.subheader("Cleaned Dataset Preview")
        st.dataframe(df, use_container_width=True)

        st.subheader("Export Cleaned Data")
        down_c1, down_c2 = st.columns(2)

        with down_c1:
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Cleaned CSV",
                data=csv_bytes,
                file_name="cleaned_data.csv",
                mime="text/csv",
                use_container_width=True
            )

        with down_c2:
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False)
            st.download_button(
                label="📥 Download Cleaned Excel",
                data=excel_buffer.getvalue(),
                file_name="cleaned_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

else:
    st.info("👈 Please upload a CSV or Excel file, or click 'Load Sample Dataset' from the sidebar to begin.")