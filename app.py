import streamlit as st
import pandas as pd
from mistralai import Mistral
import extract_criteres_2 as ec

# Set page config and custom CSS
st.set_page_config(page_title="Christmas Gift Finder 🎄")

# Custom CSS for Christmas theme
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0c3823 0%, #165e3b 100%);
    }
    .stTitle {
        color: #e8172c !important;
        text-align: center;
        font-size: 3rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .stButton>button {
        background-color: #e8172c;
        color: white;
        border-radius: 20px;
        padding: 10px 25px;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 15px;
        border: 2px solid #165e3b;
    }
    
    /* Enhanced snow effect */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: 1000;
        background-image: 
            radial-gradient(8px 8px at 100px 50px, rgba(255, 255, 255, 0.9) 1px, transparent 1px),
            radial-gradient(6px 6px at 200px 150px, rgba(255, 255, 255, 0.85) 1px, transparent 1px),
            radial-gradient(7px 7px at 300px 250px, rgba(255, 255, 255, 0.9) 1px, transparent 1px),
            radial-gradient(5px 5px at 400px 350px, rgba(255, 255, 255, 0.85) 1px, transparent 1px),
            radial-gradient(6px 6px at 500px 100px, rgba(255, 255, 255, 0.9) 1px, transparent 1px);
        animation: snow 15s linear infinite;
    }

    @keyframes snow {
        0% { background-position: 0px 0px, 0px 0px, 0px 0px, 0px 0px, 0px 0px; }
        100% { background-position: 500px 1000px, 400px 800px, 300px 600px, 200px 400px, 100px 300px; }
    }
            
    /* Enhanced snowflake animation */
    .snowflake {
        position: fixed;
        background: white;
        border-radius: 50%;
        opacity: 0.9;
        animation: snowfall 15s linear infinite;
        box-shadow: 0 0 5px rgba(255, 255, 255, 0.8);
    }

    .snowflake:nth-child(2n) {
        width: 8px;
        height: 8px;
        animation-duration: 12s;
    }

    .snowflake:nth-child(3n) {
        width: 6px;
        height: 6px;
        animation-duration: 18s;
    }

    .snowflake:nth-child(4n) {
        width: 7px;
        height: 7px;
        animation-duration: 20s;
    }

    @keyframes snowfall {
        0% {
            transform: translateY(-100px) translateX(0) rotate(0deg);
        }
        50% {
            transform: translateY(50vh) translateX(100px) rotate(180deg);
        }
        100% {
            transform: translateY(100vh) translateX(0) rotate(360deg);
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize LLM client
api_key #insert API key
model = "mistral-large-latest"
client = Mistral(api_key=api_key)
temperature = 0.5
df = pd.read_csv("path to amazon-products.csv")


def filter_into_output(df_filtered, nbr_resultats, user_prompt):
    # [Keep the existing function implementation]
    api_key = "XUgHIg6M4DeAlT0YdNF8UjzJ24dFONEA"
    model = "mistral-small-latest"
    top_n_products = df_filtered.sort_values(by="ratings", ascending=False).head(nbr_resultats)
    columns_to_keep = ["link", "image", "name", "actual_price"]
    df = top_n_products[columns_to_keep]
    client = Mistral(api_key=api_key)
    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": f"Given this data frame {df}, write me a phrase explaining how the products are related to the gift desired in the original user prompt {user_prompt}, without estimating the price. Assume the role of a helpful store counselor by considering the suitability, appeal, or purpose of the products in relation to the described gift need.",
            },
        ]
    )
    return (chat_response.choices[0].message.content, df)

# App header with Christmas decorations
st.markdown("# 🎄 Christmas Gift Finder 🎁")
st.markdown("### Let the holiday magic help you find the perfect gift! ✨")

# Styled slider
st.markdown("#### 🎯 How many gift suggestions would you like?")
n = st.slider("", min_value=1, max_value=50, value=8)

# Styled form
with st.form(key='gift_finder_form', clear_on_submit=False):
    st.markdown("#### 🎅 What kind of person are you shopping for?")
    user_prompt = st.text_input("", placeholder="Describe your perfect gift or the person you are gifting it to...")
    submit_button = st.form_submit_button("🔍 Find Magical Gifts")

# Search and display products
if submit_button:
    if user_prompt:
        with st.spinner("🎄 Our elves are searching for the perfect gifts..."):
            # [Keep the existing processing logic]
            filtered_df_cat = ec.categorie(user_prompt, df)
            assert filtered_df_cat.empty == False, "Please enter a more detailed description : we were unable to find a gift with this description"
            filtered_df = filtered_df_cat
            filtered_df_one_choice = ec.choix(user_prompt, filtered_df)
            filtered_df['actual_price'] = (
                filtered_df['actual_price']
                .astype(str)
                .str.replace('₹', '', regex=False)
                .str.replace(',', '', regex=False)
                .astype(float)
                .fillna(0)
                .astype(int)
            )
            filtered_df['discount_price'] = (
                filtered_df['discount_price']
                .astype(str)
                .str.replace('₹', '', regex=False)
                .str.replace(',', '', regex=False)
                .astype(float)
                .fillna(0)
                .astype(int)
            )
            filtered_df['discount_price'] = (
                filtered_df['discount_price']
                .astype(str)
                .str.replace('₹', '', regex=False)
                .str.replace(',', '', regex=False)
                .astype(float)
                .fillna(0)
                .astype(int)
            )
            filtered_df_one_choice['actual_price'] = (
                filtered_df_one_choice['actual_price']
                .astype(str)
                .str.replace('₹', '', regex=False)
                .str.replace(',', '', regex=False)
                .astype(float)
                .fillna(0)
                .astype(int)
            )
            filtered_df_one_choice['discount_price'] = (
                filtered_df_one_choice['discount_price']
                .astype(str)
                .str.replace('₹', '', regex=False)
                .str.replace(',', '', regex=False)
                .astype(float)
                .fillna(0)
                .astype(int)
            )
            filtered_df_one_choice['discount_price'] = (
                filtered_df_one_choice['discount_price']
                .astype(str)
                .str.replace('₹', '', regex=False)
                .str.replace(',', '', regex=False)
                .astype(float)
                .fillna(0)
                .astype(int)
            )
            response_message, filtered_df_poubelle = filter_into_output(filtered_df, n, user_prompt)
            filtered_df = filtered_df.sample(n=n).reset_index(drop=True)
            
            # Styled results
            st.markdown("### 🎁 Here are your gift suggestions:")
            st.markdown(f"*{response_message}*")
            if not filtered_df_one_choice.empty:
                    st.markdown(""" 
                    <div style="background-color: rgba(232, 23, 44, 0.1); 
                                border: 2px solid #e8172c; 
                                border-radius: 10px; 
                                padding: 20px; 
                                margin: 20px 0;">
                        <h3 style="color: white;">🎅 We have found the perfect gift for you:</h3>
                        <p style="color: white;">{}</p>
                        <p style="color: white;">🎯 Price: ₹{}</p>
                        <p style="color: white;">⭐ Rating: {}</p>
                        <p style="color: white;">🚨 Discounted Price: ₹{}</p>
                        <a href="{}" style="color: white; text-decoration: underline;">Click here to buy</a>
                    </div>
                    """.format(
                        filtered_df_one_choice['name'].values[0],
                        format(filtered_df_one_choice['actual_price'].values[0], '.2f'),
                        filtered_df_one_choice['ratings'].values[0],
                        format(filtered_df_one_choice['discount_price'].values[0], '.2f'),
                        filtered_df_one_choice['link'].values[0]
                    ), unsafe_allow_html=True)
                    
                    st.image(filtered_df_one_choice['image'].values[0], width=200)
            st.markdown("### 🎁 Other gift suggestions:")        
            if not filtered_df.empty:
                # Create columns for better layout
                cols = st.columns(2)
                for idx, row in filtered_df.head(n).iterrows():
                    with cols[idx % 2]:
                        st.markdown("---")
                        if pd.notnull(row["image"]) and row["image"].strip():
                            st.image(row["image"], width=200)
                        st.markdown(f"""
                            <a href="{row['link']}" style="color: white; text-decoration: none; font-weight: bold;">
                            🏷️ {row['name']}</a>
                            """, unsafe_allow_html=True)
                        st.markdown(f"💰 Price: ₹{format((row['actual_price']), '.2f')}")
                        st.markdown(f"⭐ Rating: {row['ratings']}")
                        st.markdown(f"🚨🤑 Discounted Price : ₹{format((row['discount_price']), '.2f')}")
            else:
                st.error("🎅 Oops! Our elves couldn't find any matching gifts.")
    else:
        st.warning("🎄 Please tell us what you're looking for!")

# Footer
st.markdown("---")
st.markdown("### 🎄 Happy Holiday Shopping! 🎁")
