import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# ===========================
# Basic Page Config & Styling
# ===========================
st.set_page_config(page_title="Data Cleaner & Analyzer", layout="wide")

st.markdown(
    """
    <style>
    .main-title {
        font-size: 32px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666666;
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='main-title'>📊 Data Cleaning & Analysis App</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Upload CSV or JSON → Clean → Analyze → Visualize</div>",
    unsafe_allow_html=True,
)


# ===========================
# Helper Functions
# ===========================
def load_dataset(uploaded_file: io.BytesIO) -> pd.DataFrame:
    """Load a CSV or JSON file into a pandas DataFrame with basic error handling."""
    if uploaded_file is None:
        return None

    filename = uploaded_file.name.lower()

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith(".json"):
            df = pd.read_json(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a CSV or JSON file.")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def show_missing_values(df: pd.DataFrame):
    """Show count of missing values per column."""
    st.subheader("Missing Values per Column")
    missing = df.isna().sum()
    missing_df = pd.DataFrame({"Column": missing.index, "Missing Values": missing.values})
    st.dataframe(missing_df, use_container_width=True)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Perform data cleaning: fill missing, remove duplicates, convert dtypes."""
    df_clean = df.copy()

    # Separate numeric and categorical columns
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    categorical_cols = df_clean.select_dtypes(exclude=[np.number]).columns

    # Fill numeric missing values with mean
    for col in numeric_cols:
        if df_clean[col].isna().any():
            df_clean[col] = df_clean[col].fillna(df_clean[col].mean())

    # Fill categorical missing values with mode
    for col in categorical_cols:
        if df_clean[col].isna().any():
            mode_vals = df_clean[col].mode()
            if not mode_vals.empty:
                df_clean[col] = df_clean[col].fillna(mode_vals[0])

    # Remove duplicate rows
    df_clean = df_clean.drop_duplicates().reset_index(drop=True)

    # Try to convert columns to more suitable dtypes where possible
    for col in df_clean.columns:
        # Try numeric conversion
        if df_clean[col].dtype == object:
            # Try numeric
            converted_num = pd.to_numeric(df_clean[col], errors="ignore")
            if not (converted_num.dtypes == object):
                df_clean[col] = converted_num
                continue

            # Try datetime
            converted_dt = pd.to_datetime(df_clean[col], errors="ignore", infer_datetime_format=True)
            if not (isinstance(converted_dt.dtype, pd.core.dtypes.dtypes.DatetimeTZDtype) or converted_dt.dtype == object):
                df_clean[col] = converted_dt

    return df_clean


def show_data_analysis(df: pd.DataFrame):
    """Display dataset shape, dtypes, descriptive stats, unique counts, correlations."""
    st.subheader("Data Analysis")

    # Shape
    st.markdown("**Dataset Shape**")
    st.write(f"Rows: `{df.shape[0]}`, Columns: `{df.shape[1]}`")

    # Data types
    st.markdown("**Column Data Types**")
    dtypes_df = pd.DataFrame({"Column": df.columns, "Type": df.dtypes.astype(str)})
    st.dataframe(dtypes_df, use_container_width=True)

    # Descriptive statistics
    st.markdown("**Descriptive Statistics (Numeric Columns)**")
    st.dataframe(df.describe().T, use_container_width=True)

    # Unique value counts for categorical columns
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns
    if len(categorical_cols) > 0:
        st.markdown("**Unique Value Counts (Categorical Columns)**")
        unique_counts = {col: df[col].nunique() for col in categorical_cols}
        unique_df = pd.DataFrame(
            {"Column": list(unique_counts.keys()), "Unique Values": list(unique_counts.values())}
        )
        st.dataframe(unique_df, use_container_width=True)
    else:
        st.info("No categorical columns detected for unique value counts.")

    # Correlation matrix for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number])
    if numeric_cols.shape[1] > 1:
        st.markdown("**Correlation Matrix (Numeric Columns)**")
        corr = numeric_cols.corr()
        st.dataframe(corr, use_container_width=True)
    else:
        st.info("Not enough numeric columns to compute a correlation matrix.")


def show_visualizations(df: pd.DataFrame):
    """Create histogram and bar chart based on user-selected columns."""
    st.subheader("Visualizations")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    col1, col2 = st.columns(2)

    # Histogram for numeric column
    with col1:
        st.markdown("**Histogram (Numeric Column)**")
        if numeric_cols:
            num_col = st.selectbox("Select numeric column", numeric_cols, key="hist_col")
            fig, ax = plt.subplots()
            ax.hist(df[num_col].dropna(), bins=20, edgecolor="black")
            ax.set_title(f"Histogram of {num_col}")
            ax.set_xlabel(num_col)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
        else:
            st.info("No numeric columns available for histogram.")

    # Bar chart for categorical column
    with col2:
        st.markdown("**Bar Chart (Categorical Column)**")
        if categorical_cols:
            cat_col = st.selectbox("Select categorical column", categorical_cols, key="bar_col")
            value_counts = df[cat_col].value_counts().head(20)  # limit to top 20
            fig, ax = plt.subplots()
            ax.bar(value_counts.index.astype(str), value_counts.values)
            ax.set_title(f"Value Counts of {cat_col}")
            ax.set_xlabel(cat_col)
            ax.set_ylabel("Count")
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
            st.pyplot(fig)
        else:
            st.info("No categorical columns available for bar chart.")


# ===========================
# Main App Logic
# ===========================
def main():
    st.sidebar.title("Upload Data")
    uploaded_file = st.sidebar.file_uploader("Upload CSV or JSON file", type=["csv", "json"])

    if uploaded_file is None:
        st.info("👆 Please upload a CSV or JSON file to begin.")
        return

    # Load dataset
    df = load_dataset(uploaded_file)
    if df is None or df.empty:
        st.warning("No data loaded. Please check your file.")
        return

    st.subheader("Raw Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    # Missing values overview
    show_missing_values(df)

    # Data cleaning
    st.subheader("Data Cleaning")
    if st.button("Clean Data"):
        cleaned_df = clean_data(df)
        st.success("Data cleaning completed.")
        st.subheader("Cleaned Data Preview")
        st.dataframe(cleaned_df.head(), use_container_width=True)

        # Save in session state for further analysis/visualization
        st.session_state["cleaned_df"] = cleaned_df
    else:
        st.info("Click **Clean Data** to perform cleaning before analysis.")
        if "cleaned_df" in st.session_state:
            st.subheader("Last Cleaned Data Preview")
            st.dataframe(st.session_state["cleaned_df"].head(), use_container_width=True)

    # Use cleaned data if available, else raw
    df_for_analysis = st.session_state.get("cleaned_df", df)

    # Data analysis
    show_data_analysis(df_for_analysis)

    # Visualizations
    show_visualizations(df_for_analysis)


if __name__ == "__main__":
    main()
