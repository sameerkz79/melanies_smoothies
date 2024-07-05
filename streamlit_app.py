# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
#new section to display fruityvice nutrition information
import requests 
import pandas as pd



# Write directly to the app
st.title("Example Streamlit App :cup_with_straw:")
st.write(
    """Choose the fruits that you want in your custom Smoothie.
    """
)

#option = st.selectbox(
 #   "What is your favorite fruit?",
  #  ("Banana", "Strawberries", "Peaches"))

#st.write("You selected:", option)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be", name_on_order)


# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function.
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()


ingredients_list = st.multiselect(
    "choose upto 5 ingredients:",
    my_dataframe,max_selections=5)



if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    
    ingredients_string= ''

    for fruit_chosen in ingredients_list:
        ingredients_string = ingredients_string + fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        #st.text(fruityvice_response.json())
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit Order')

    

    #if ingredients_string:
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
    
        st.success('Your Smoothie is ordered! ' + name_on_order + '!',icon="✅")




