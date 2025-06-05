import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Auto Data Cleaner", layout="wide")

st.title("📊 Auto Data Cleaning & Visualization App")

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    if 'df' not in st.session_state:
        st.session_state.df = df.copy()

    df = st.session_state.df

    # Sidebar options
    st.sidebar.title("Options")
    choice = st.sidebar.selectbox("Select an Operation", [
        "View Data Overview",
        "Check Missing Values",
        "Fill Missing Values",
        "Drop Missing Values",
        "Drop Duplicates",
        "Drop Columns",
        "Drop Rows",
        "Replace Values",
        "Rename Columns",
        "Change Data Types",
        "Generate Graphs",
        "Save File"
    ])

    if choice == "View Data Overview":
        st.subheader("🔍 Data Overview")
        st.dataframe(df)
        with st.expander("ℹ️ Data Info"):
            buffer = io.StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())
        st.write("**Shape:**", df.shape)
        st.write("**Describe:**")
        st.write(df.describe())
        st.write("**Column Types:**")
        st.write(df.dtypes)

    elif choice == "Check Missing Values":
        st.subheader("❓ Missing Values")
        st.write(df.isnull().sum())

    elif choice == "Fill Missing Values":
        st.subheader("🧪 Fill Missing Values")
        col = st.selectbox("Select column to fill", df.columns)
        method = st.radio("Select fill method", ["Custom value", "Mean", "Median", "Mode"])
        if method == "Custom value":
            value = st.text_input("Enter value to fill")
            if st.button("Fill"):
                df[col] = df[col].fillna(value)
                st.success("✅ Filled missing values with custom value")
        elif method == "Mean":
            if st.button("Fill with Mean"):
                df[col] = df[col].fillna(df[col].mean())
                st.success("✅ Filled missing values with Mean")
        elif method == "Median":
            if st.button("Fill with Median"):
                df[col] = df[col].fillna(df[col].median())
                st.success("✅ Filled missing values with Median")
        elif method == "Mode":
            if st.button("Fill with Mode"):
                df[col] = df[col].fillna(df[col].mode()[0])
                st.success("✅ Filled missing values with Mode")

    elif choice == "Drop Missing Values":
        st.subheader("🧹 Drop Rows with Missing Values")
        if st.button("Drop"):
            df.dropna(inplace=True)
            df.reset_index(drop=True, inplace=True)
            st.success("✅ Dropped missing values")

    elif choice == "Drop Duplicates":
        st.subheader("🧽 Drop Duplicate Rows")
        if st.button("Drop"):
            df.drop_duplicates(inplace=True)
            df.reset_index(drop=True, inplace=True)
            st.success("✅ Dropped duplicates")

    elif choice == "Drop Columns":
        st.subheader("🗂️ Drop Column")
        col = st.multiselect("Select columns to drop", df.columns)
        if st.button("Drop"):
            df.drop(columns=col, inplace=True)
            st.success(f"✅ Dropped columns: {col}")

    elif choice == "Drop Rows":
        st.subheader("🧾 Drop Rows")
        row_idx = st.number_input("Enter index of row to drop", min_value=0, max_value=len(df)-1)
        if st.button("Drop"):
            df.drop(index=row_idx, inplace=True)
            df.reset_index(drop=True, inplace=True)
            st.success(f"✅ Dropped row {row_idx}")

    elif choice == "Replace Values":
        st.subheader("🔄 Replace Values")
        col = st.selectbox("Select column", df.columns)
        old_val = st.text_input("Old Value")
        new_val = st.text_input("New Value")
        if st.button("Replace"):
            df[col] = df[col].replace(old_val, new_val)
            st.success("✅ Replaced values")

    elif choice == "Rename Columns":
        st.subheader("✏️ Rename Columns")
        col = st.selectbox("Select column to rename", df.columns)
        new_name = st.text_input("Enter new column name")
        if st.button("Rename"):
            df.rename(columns={col: new_name}, inplace=True)
            st.success(f"✅ Renamed {col} to {new_name}")

    elif choice == "Change Data Types":
        st.subheader("🔧 Change Data Types")
        col = st.selectbox("Select column", df.columns)
        dtype = st.selectbox("Select type", ["int", "float", "str", "bool"])
        if st.button("Convert"):
            try:
                df[col] = df[col].astype(dtype)
                st.success(f"✅ Converted {col} to {dtype}")
            except Exception as e:
                st.error(f"❌ Error: {e}")

    elif choice == "Generate Graphs":
        st.subheader("📈 Generate Graphs")

        graph_type = st.selectbox("Select graph type", [
            "Line Plot", "Bar Plot", "Histogram", "Box Plot",
            "Scatter Plot", "Heatmap", "Pair Plot", "Count Plot", "Violin Plot"
        ])

        # Variable initialization based on graph type
        if graph_type in ["Line Plot", "Bar Plot", "Scatter Plot", "Violin Plot", "Box Plot"]:
            x_col = st.selectbox("Select X-axis", df.columns)
            y_col = st.selectbox("Select Y-axis", df.columns)
        elif graph_type in ["Histogram", "Count Plot"]:
            x_col = st.selectbox("Select Column", df.columns)
            y_col = None
        elif graph_type == "Pair Plot":
            cols = st.multiselect("Select multiple columns", df.columns)
            x_col = y_col = None
        else:
            x_col = y_col = None

        if st.button("Generate"):
            try:
                # Set style for better plots
                plt.style.use('default')
                
                if graph_type == "Line Plot":
                    fig, ax = plt.subplots(figsize=(12, 6))
                    sns.lineplot(data=df, x=x_col, y=y_col, ax=ax)
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)

                elif graph_type == "Bar Plot":
                    fig, ax = plt.subplots(figsize=(12, 6))
                    sns.barplot(data=df, x=x_col, y=y_col, ax=ax)
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)

                elif graph_type == "Histogram":
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.histplot(df[x_col], kde=True, ax=ax)
                    plt.tight_layout()
                    st.pyplot(fig)

                elif graph_type == "Box Plot":
                    fig, ax = plt.subplots(figsize=(12, 6))
                    sns.boxplot(data=df, x=x_col, y=y_col, ax=ax)
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)

                elif graph_type == "Scatter Plot":
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)

                elif graph_type == "Violin Plot":
                    fig, ax = plt.subplots(figsize=(12, 6))
                    sns.violinplot(data=df, x=x_col, y=y_col, ax=ax)
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)

                elif graph_type == "Heatmap":
                    fig, ax = plt.subplots(figsize=(12, 8))
                    numeric_df = df.select_dtypes(include=['number'])
                    if not numeric_df.empty:
                        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax, fmt='.2f')
                        plt.tight_layout()
                        st.pyplot(fig)
                    else:
                        st.warning("⚠️ No numeric columns found for correlation heatmap.")

                elif graph_type == "Pair Plot":
                    if len(cols) < 2:
                        st.warning("⚠️ Please select at least 2 columns.")
                    else:
                        fig = sns.pairplot(df[cols])
                        st.pyplot(fig)

                elif graph_type == "Count Plot":
                    fig, ax = plt.subplots(figsize=(12, 6))
                    sns.countplot(data=df, x=x_col, ax=ax)
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)

                else:
                    st.warning("⚠️ Invalid graph type or insufficient columns selected.")

            except Exception as e:
                st.error(f"❌ Error generating graph: {e}")
    
    elif choice == "Save File":
        st.subheader("💾 Save Cleaned Data")
        filename = st.text_input("Enter filename (without extension)", value="cleaned_data")
        if st.button("Download CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{filename}.csv",
                mime="text/csv"
            )

    # Always show current dataframe at the bottom
    st.subheader("📊 Current Data")
    st.dataframe(df)
    st.write(f"**Current Shape:** {df.shape}")