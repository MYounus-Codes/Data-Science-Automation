import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.ion()  # Enable interactive mode
sns.set(style='darkgrid')

def load_file():
    while True:
        try:
            file_name = input("📂 Enter the CSV file name (with .csv): ")
            df = pd.read_csv(file_name)
            print("✅ File loaded successfully!\n")
            return df
        except Exception as e:
            print(f"❌ Error: {e}. Please try again.\n")

def display_menu():
    print("""
========= 🔍 DATA CLEANING & VISUALIZATION MENU =========
1. View Data Info
2. Describe Data Statistics
3. Show Data Shape
4. List Column Names
5. View Head
6. View Tail
7. Show Data Types
8. Show Null Value Table
9. Show Total Null Values
10. Fill Missing Values (Custom Input)
11. Drop Rows with Missing Values
12. Drop Duplicates
13. Drop Column
14. Drop Row by Index
15. Replace Specific Values
16. Rename Column
17. Change Data Type of Column
18. Sort Data by Column
19. Filter Rows by Column Value
20. Save Data (CSV/Excel)
21. Plot Graphs (Matplotlib & Seaborn)
22. Exit
==========================================================
""")

def fill_missing(df):
    value = input("Enter the value to fill missing data with (string or number): ")
    try:
        value = eval(value)  # allow numeric inputs like 0, 1.0, etc.
    except:
        pass  # keep as string
    df = df.fillna(value)
    print("✅ Missing values filled.\n")
    return df

def drop_missing(df):
    df = df.dropna()
    print("✅ Rows with missing values dropped.\n")
    return df

def drop_duplicates(df):
    df = df.drop_duplicates()
    print("✅ Duplicate rows dropped.\n")
    return df

def drop_column(df):
    col = input("Enter column name to drop: ")
    if col in df.columns:
        df = df.drop(columns=[col])
        print(f"✅ Column '{col}' dropped.\n")
    else:
        print("❌ Column not found.")
    return df

def drop_row(df):
    try:
        idx = int(input("Enter row index to drop: "))
        df = df.drop(index=idx)
        print(f"✅ Row at index {idx} dropped.\n")
    except Exception as e:
        print(f"❌ Error: {e}")
    return df

def replace_values(df):
    col = input("Column name: ")
    old = input("Old value: ")
    new = input("New value: ")
    df[col] = df[col].replace(old, new)
    print(f"✅ Replaced '{old}' with '{new}' in column '{col}'.\n")
    return df

def rename_column(df):
    print("Current columns:", list(df.columns))
    old = input("Old column name: ")
    new = input("New column name: ")
    df = df.rename(columns={old: new})
    print(f"✅ Renamed '{old}' to '{new}'.\n")
    return df

def change_dtype(df):
    col = input("Column to change type: ")
    dtype = input("New type (int, float, str, bool): ")
    try:
        df[col] = df[col].astype(dtype)
        print(f"✅ Changed '{col}' to {dtype}.\n")
    except Exception as e:
        print(f"❌ Error: {e}")
    return df

def sort_data(df):
    col = input("Sort by column: ")
    if col in df.columns:
        df = df.sort_values(by=col)
        print(f"✅ Data sorted by '{col}'.\n")
    else:
        print("❌ Column not found.")
    return df

def filter_rows(df):
    col = input("Column to filter by: ")
    val = input("Value to filter for: ")
    try:
        val = eval(val)
    except:
        pass
    if col in df.columns:
        filtered = df[df[col] == val]
        print(f"✅ {len(filtered)} rows match the filter.")
        print(filtered.head())
    else:
        print("❌ Column not found.")
    return df

def save_file(df):
    fmt = input("Save as (csv/xlsx): ").lower()
    name = input("File name (without extension): ")
    try:
        if fmt == 'csv':
            df.to_csv(name + '.csv', index=False)
        elif fmt == 'xlsx':
            df.to_excel(name + '.xlsx', index=False)
        else:
            print("❌ Unsupported format.")
            return
        print("✅ File saved successfully.\n")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

def plot_graph(df):
    print("\n📊 Choose Plot Type:")
    print("1. Histogram\n2. Line Plot\n3. Bar Plot\n4. Box Plot\n5. Pairplot\n6. Heatmap (correlation matrix)")
    choice = input("Enter your choice: ")

    try:
        if choice == '1':
            col = input("Column to plot histogram: ")
            df[col].plot.hist()
        elif choice == '2':
            x = input("X-axis column: ")
            y = input("Y-axis column: ")
            df.plot(x=x, y=y)
        elif choice == '3':
            x = input("X-axis: ")
            y = input("Y-axis: ")
            sns.barplot(x=x, y=y, data=df)
        elif choice == '4':
            col = input("Column for box plot: ")
            sns.boxplot(y=col, data=df)
        elif choice == '5':
            sns.pairplot(df.select_dtypes(include=['float', 'int']))
        elif choice == '6':
            sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
        else:
            print("❌ Invalid choice.")
            return
        plt.title("📈 Graph Output")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"❌ Error generating plot: {e}")

def main():
    df = load_file()

    while True:
        display_menu()
        choice = input("🔢 Enter your choice (1–22): ").strip()

        if choice == '1':
            print(df.info())
        elif choice == '2':
            print(df.describe(include='all'))
        elif choice == '3':
            print(df.shape)
        elif choice == '4':
            print(df.columns)
        elif choice == '5':
            print(df.head())
        elif choice == '6':
            print(df.tail())
        elif choice == '7':
            print(df.dtypes)
        elif choice == '8':
            print(df.isnull())
        elif choice == '9':
            print(df.isnull().sum())
        elif choice == '10':
            df = fill_missing(df)
        elif choice == '11':
            df = drop_missing(df)
        elif choice == '12':
            df = drop_duplicates(df)
        elif choice == '13':
            df = drop_column(df)
        elif choice == '14':
            df = drop_row(df)
        elif choice == '15':
            df = replace_values(df)
        elif choice == '16':
            df = rename_column(df)
        elif choice == '17':
            df = change_dtype(df)
        elif choice == '18':
            df = sort_data(df)
        elif choice == '19':
            df = filter_rows(df)
        elif choice == '20':
            save_file(df)
        elif choice == '21':
            plot_graph(df)
        elif choice == '22' or choice.lower() == 'exit':
            print("👋 Exiting. Goodbye!")
            break
        else:
            print("❌ Invalid input, try again.\n")

        print("--------------------------------------------------")

if __name__ == "__main__":
    main()
