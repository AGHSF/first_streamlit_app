import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

st.title('My Parents New Healthy Diner')

st.header('Breakfast Favorites')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Rang Egg')
st.text('🥑🍞 Avocado Toast')   

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)

# create function
def get_fruitvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())  
  return (fruityvice_normalized)

# New Section to display fruityvice api response
st.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruitvice_data(fruit_choice)
    st.dataframe(back_from_function)

except URLError as e:
  st.error()

st.header("The fruit load list contains:")

# Snowflake related functions
def get_fruit_load_list():
  with my_cur = my_cnx.cursor() as my_cur:
  my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
  return my_cur.fetchall()

# Add button to load fruit
if st.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  st.dataframe(my_data_rows)
  
# don't run past here while troubleshoot
st.stop()

# Allow user to add a fruit to the list
add_my_fruit = st.text_input('What fruit would you like to add?','jackfruit')
st.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")
