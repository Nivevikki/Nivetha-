import streamlit as st
import pandas as pd
import mysql.connector

# Database connection
connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="redbus"
)
# Create a cursor object
cursor = connection.cursor(buffered=True)
# Query to fetch the data
cursor.execute("SELECT * FROM REDBUSPROJECT")

out = cursor.fetchall()

# Convert the result to a pandas DataFrame
# Ensure to get column names
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(out, columns=columns)

# Convert Price and Star_Rating columns to numeric types, forcing any errors to NaN
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['Star_Rating'] = pd.to_numeric(df['Star_Rating'], errors='coerce')

# Debugging: Print out the DataFrame columns and the first few rows
print("DataFrame columns:", df.columns)
print("DataFrame preview:", df.head())

# Streamlit application
st.set_page_config(page_title="RedBus Data Filtering", page_icon="https://th.bing.com/th/id/OIP.6nU3XTAOJe8B07685FoXVQHaEK?w=305&h=180&c=7&r=0&o=5&dpr=2&pid=1.7", layout="wide")

# Add a background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://miro.medium.com/v2/resize:fit:828/format:webp/1*S-95TWd9jgxT87cKkZWnFg.jpeg');
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('RedBus Data Application')

# Sidebar filters
st.sidebar.title("Filters")

# Debugging: Check if 'Route_Name' is in the DataFrame columns
if 'Route_Name' in df.columns:
    Route_Name_options = df["Route_Name"].unique()
    selected_Route_Name = st.sidebar.selectbox("Select Route_Name", Route_Name_options)
else:
    st.error("The column 'Route_Name' is not in the DataFrame")

# Ensure that the DataFrame has the 'Price' column before using it
if 'Price' in df.columns:
    price_min = int(df["Price"].min())
    price_max = int(df["Price"].max())
    selected_price = st.sidebar.slider("Select Price Range", price_min, price_max, (price_min, price_max))
else:
    st.error("The column 'Price' is not in the DataFrame")

# Ensure that the DataFrame has the 'Star_Rating' column before using it
if 'Star_Rating' in df.columns:
    Star_Rating_min = float(df["Star_Rating"].min())
    Star_Rating_max = float(df["Star_Rating"].max())
    selected_Star_Rating = st.sidebar.slider("Select Star_Rating Range", Star_Rating_min, Star_Rating_max, (Star_Rating_min, Star_Rating_max))
else:
    st.error("The column 'Star_Rating' is not in the DataFrame")

# Filter button
if st.sidebar.button("Filter Data"):
    if 'Route_Name' in df.columns and 'Price' in df.columns and 'Star_Rating' in df.columns:
        filtered_df = df[
            (df["Route_Name"] == selected_Route_Name) &
            (df["Price"] >= selected_price[0]) &
            (df["Price"] <= selected_price[1]) &
            (df["Star_Rating"] >= selected_Star_Rating[0]) &
            (df["Star_Rating"] <= selected_Star_Rating[1])
        ]
        st.write(filtered_df)
else:
    st.write("Apply filters to see the data.")
