import streamlit as st
import requests
import json
import pandas as pd

# Function to generate item description using Claude3 API from RapidAPI
def generate_description(item_name):
    url = "https://open-ai21.p.rapidapi.com/claude3"
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": f"Generate a brief description for the following item: {item_name}"
            }
        ],
        "web_access": False
    }
    headers = {
        "x-rapidapi-key": "16f5c159b3msh21dadd8bef46b22p1b1c30jsnfe4d1c6a1411",  # Replace with your actual RapidAPI key
        "x-rapidapi-host": "open-ai21.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    try:
        # Print the full response to inspect its structure
        response_data = response.json()
        st.write(response_data)  # Streamlit way of displaying the response
        
        # Adjust this part based on the actual structure of the response
        if 'choices' in response_data:
            return response_data['choices'][0]['message']['content']
        else:
            return response_data.get('content', 'No content available')  # Fallback if 'choices' is not found

    except Exception as e:
        return f"Error: {str(e)}"

# Initialize session state to store inventory
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['Item', 'Quantity', 'Description'])

# Streamlit app
st.title('AI-Powered Inventory Management System')

# Input fields for new item
new_item = st.text_input('Enter new item name')
quantity = st.number_input('Enter quantity', min_value=1, value=1)

if st.button('Add Item'):
    if new_item:
        description = generate_description(new_item)
        new_row = pd.DataFrame({'Item': [new_item], 'Quantity': [quantity], 'Description': [description]})
        st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
        st.success(f'Added {new_item} to inventory!')
    else:
        st.warning('Please enter an item name.')

# Display inventory
st.subheader('Current Inventory')
st.dataframe(st.session_state.inventory)

# Export inventory to CSV including description
if not st.session_state.inventory.empty:
    csv = st.session_state.inventory.to_csv(index=False)
    st.download_button(
        label="Download Inventory as CSV",
        data=csv,
        file_name="inventory.csv",
        mime="text/csv",
    )

