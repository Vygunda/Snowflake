import streamlit as st
from snowflake.snowpark.functions import col,when_matched

# Write directly to the app
st.title("Pending Smoothie orders :cup_with_straw:")
st.write(
    """Orders that need to be filled.
    """
)

# name_on_order = st.text_input("Name on the smoothie")
# st.write("The name on the smoothie will be ", name_on_order)


cnx=st.connection("snowflake")
session = cnx.session()
#my_dataframe1 = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#st.dataframe(data=my_dataframe, use_container_width=True)
if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted=st.button('Submit')
    if submitted:
        #st.success('Someone clicked the button', icon = '👍')
    
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        
        try:
            og_dataset.merge(edited_dataset
                         , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )
        except:
            st.write('Something went wrong')
else:
    st.success('No pending orders',icon = '👍')
           
    



























