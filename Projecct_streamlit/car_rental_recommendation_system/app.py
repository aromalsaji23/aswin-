import streamlit as st
import pandas as pd

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv('ex_car_rental_data.csv')

df = load_data()

# App title with background image
st.markdown("""
    <style>
    .main {
        background-image: url('https://wallpapercrafter.com/th800/14002-car-sunset-night-movement-speed-4k.jpg');
        background-size: cover;
        background-position: center;
        padding: 30px;
        color: white;  /* Change text color for better readability */
        font-family: 'Dancing Script', cursive;
    }
    </style>
""", unsafe_allow_html=True)

# Set the main page layout
st.title('Car Rental Recommendation System')

# Dataset display option
if st.checkbox('Show Available Cars Dataset'):
    st.dataframe(df)

# User inputs for recommendation
st.sidebar.header('User Preferences')
category = st.sidebar.selectbox("Select Car Category", df['Category'].unique())
fuel_type = st.sidebar.selectbox("Select Fuel Type", df['Fuel Type'].unique())
num_seats = st.sidebar.slider("Number of Seats", min_value=int(df['Number of Seats'].min()), max_value=int(df['Number of Seats'].max()), step=1)
air_conditioning = st.sidebar.selectbox("Air Conditioning", df['Air Conditioning'].unique())
budget = st.sidebar.number_input("Enter your budget (INR)", min_value=0)

# Recommendation button
if st.sidebar.button("Recommend Cars"):
    # Filter dataset based on user inputs
    filtered_df = df[
        (df['Category'] == category) &
        (df['Fuel Type'] == fuel_type) &
        (df['Number of Seats'] == num_seats) &
        (df['Air Conditioning'] == air_conditioning) &
        (df['Price Per Day (INR)'] <= budget)
    ]

    # Display results
    st.subheader('Recommended Cars')
    if not filtered_df.empty:
        st.write("Cars matching your preferences:")
        # Create a list of recommended cars
        recommended_cars = filtered_df[['Car Name', 'Price Per Day (INR)', 'Category', 'Fuel Type', 'Number of Seats', 'Air Conditioning', 'Features']].values.tolist()
        
        # Display detailed information for each car
        for car in recommended_cars:
            st.markdown(f"""
                - <span style='font-size: 24px; font-weight: bold;'>{car[0]}</span>
                - **Price**: ₹{car[1]} per day
                - **Category**: {car[2]}
                - **Fuel Type**: {car[3]}
                - **Number of Seats**: {car[4]}
                - **Air Conditioning**: {car[5]}
                - **Features**: {car[6]}
            """, unsafe_allow_html=True)  # Enable unsafe HTML to render the size change
    else:
        st.write("No cars match your preferences.")
