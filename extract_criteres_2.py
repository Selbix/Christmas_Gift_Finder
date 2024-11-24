import os
import pandas as pd
from mistralai import Mistral
from io import StringIO
df = pd.read_csv("/Users/samyelbakouri/Desktop/HACKATHON/archive (2)/Amazon-Products.csv")
#df["category"] = df["category"].unique().to_string()
api_key = "XUgHIg6M4DeAlT0YdNF8UjzJ24dFONEA" # your API key
model = "mistral-large-latest"
client = Mistral(api_key=api_key)
temperature = 0.5
def prix(arg, dataframe):
    df = dataframe
    
    prompt_client = arg
    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": f"Given the description of gift preferences provided, identify the price range based on contextual language and return it as a Python list. The prompt is: " + prompt_client + " Follow these rules for interpreting price ranges: If the description uses terms like 'low-end', 'affordable', or 'budget', assume a price range starting at 100 and going up to 1,000. If terms like 'mid-range', 'moderate', or 'reasonably priced' are mentioned, assume a range starting at 1,000 and going up to 5,000. If phrases like 'high-end', 'luxury', or 'expensive' are mentioned, assume a range starting at 5,000 and going up to 50,000. If specific numerical prices are mentioned (e.g., 'around 2,000'), infer a range of ±20% around the value (e.g., [1,600, 2,400]). Return only a Python list containing two numerical values representing the price range in RUPEES, with the lower price as the first element and the higher price as the second element. The output must be directly usable as a Python list string, e.g., [1000, 5000], IT IS VITAL YOU RETURN ONLY THE PYTHON LIST WHICH MUST BE USABLE AS SUCH, DO NOT ADD ANY ADDITIONAL COMMENT",
            },
        ]
    )

    print(chat_response.choices[0].message.content) # your answer :)
    # Split the response content into a list
    # list = chat_response.choices[0].message.content.split(",")
    # print(list)

    # Extract the lower and upper price range from the list
    # x = int(list[0][1:])
    # y = int(list[1][:-1])
    # print(x, y)

    # Clean the 'discounted_price' column in the dataframe by removing the currency symbol and converting to integer
    # df['discounted_price_cleaned'] = df['discounted_price'].str.replace('₹', '', regex=False).astype(int)

    # Filter the dataframe based on the extracted price range
    # filtered_df = df[(df['discounted_price_cleaned'] >= x) & (df['discounted_price_cleaned'] <= y)]

    # Output the filtered dataframe
    # chat_response.choices[0].message.content

    response_content = chat_response.choices[0].message.content.strip()

    # Parse the Python list from the response
    try:
        # Clean and format the response
        clean_response = response_content.strip('[]').replace(' ', '').replace('"', "")
        price_values = [int(x) for x in clean_response.split(',')]
        
        if len(price_values) == 2:
            x, y = price_values
            print(f"Extracted price range: {x}, {y}")
        else:
            raise ValueError("The response is not a valid price range list.")
    except Exception as e:
        print(f"Error parsing the response: {e}")
        return pd.DataFrame()  # Return empty DataFrame instead of raising

    # Assuming df['discounted_price'] is a column in your DataFrame
    # Clean the 'discounted_price' column
    df['actual_price'] = (
        df['actual_price']
        .astype(str)  # Ensure all values are strings for consistent processing
        .str.replace('₹', '', regex=False)  # Remove the currency symbol
        .str.replace(',', '', regex=False)  # Remove any commas
        .astype(float)  # Convert to float to handle decimal numbers
        .fillna(0)  # Replace NaN values with 0
        .astype(int)  # Convert to int (rounds down by default)
    )

    # Filter the DataFrame based on the extracted price range
    filtered_df = df[(df['actual_price'] >= x) & (df['actual_price'] <= y)]


    # Debug output for verification
    print("Cleaned and filtered DataFrame:", filtered_df)
    return filtered_df

#prix("I want a phone very expensive")

def categorie(arg, dataframe):
    unique_categories = dataframe['main_category'].unique()
# If you want to convert it to a list
    unique_categories_list = unique_categories.tolist() 
    string_cats = ', '.join(unique_categories_list)  
    prompt_client = arg
    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
"content": f"From the following client prompt{prompt_client}, identify the top relevant category from this list of category {string_cats}, ensuring the response is in the format of a Python string (e.g. 'choosen_category'), keep the ENTIRE NAME of the category and do not truncate it.  DO NOT WRITE ANYTHING BESIDES THE ANSWER AS DEMANDED",
            },
        ]

    )
    response_content = chat_response.choices[0].message.content.strip()
    print(f"Raw LLM category response: {response_content}")
    clean_response = response_content.replace("'", "").strip()  # Debugging output
    dataframe_filtered = dataframe[dataframe['main_category'] == clean_response]
    print(f"taille {dataframe_filtered.shape}")
    
    unique_subcategories = dataframe_filtered['sub_category'].unique() 
    #print(unique_subcategories)
    string_subcats = ', '.join(map(str, unique_subcategories))
    #print(string_subcats)
    #string_subcats = ', '.join(unique_subcategories)
    print(f"Unique subcategories: {string_subcats}")
    chat_response_2 = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
"content": f"From the given client prompt {prompt_client}, identify the top 3 most relevant subcategories from the provided list {string_subcats}, this list is the only thing you can choose from, it is extremely important you choose only from this list. Only select subcategories from the provided list {string_subcats}, do not add, modify, or rename any subcategories; use them exactly as they appear in the list. The response must be in the format of a Python list string, e.g., [subcategory_1, subcategory_2, subcategory_3]. Return only the Python list without any additional comments, explanations, or modifications. Ensure the output is directly usable as a Python list string.",
                },
            ]

        )
    print(f"Raw LLM subcategory response: {response_content}")
    subcategory_list = chat_response_2.choices[0].message.content.replace("'", "").replace("\n", "").replace('"', "").strip()
    print("HERE", subcategory_list)
    #dataframe_filtered = dataframe[dataframe['main_category'] == clean_response]

    dataframe_filtered_2 = dataframe_filtered[
        dataframe_filtered['sub_category'].apply(lambda x: any(subcat.lower() in str(x).lower() for subcat in subcategory_list))
    ]    
    print(dataframe_filtered_2.head(15))
    return dataframe_filtered_2

def choix(user_prompt, df):
    prompt_client = user_prompt
    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
    "content": f"Given the client's query: '{prompt_client}', and the provided dataframe : {str(df['name'])}, extract up to 5 item names from the dataframe that best match the query. Return the result strictly as a Python list in the format ['name1', 'name2', ...]. If you happen not to find anything of value, choose 30 name at random. Do not include any comments, explanations, or text other than the list.",
            },
        ]
    )
    response_content = chat_response.choices[0].message.content.strip()
    print(f"reponse : {response_content}")
    # Convert response content to list by evaluating the string representation
    # Clean the response string and convert to Python list
    # Convert string representation of list to actual list
    response_content = response_content.replace("'", '').replace('"', '').replace("python", '').replace("`", '').replace("\n",'')
    try:
        item_list = eval(response_content)
    except:
        # Fallback clean-up if eval fails
        item_list = response_content.strip('[]').split(',')
        item_list = [item.strip().strip("'").strip('"') for item in item_list]
    print(f"ITEM LIST IS THIS {item_list}")
    # Filter dataframe to keep rows where name matches any item in the list
    dataframe_filtered = df[df['name'].isin(item_list)]
    #dataframe_filtered = df[df['name'] == dataf['name']]
    if dataframe_filtered.empty:
        raise ValueError("The DataFrame is empty. Please provide valid data.")
    else:
        print("The DataFrame is not empty.")
    print(dataframe_filtered.head(6))
    return dataframe_filtered
    
#choix("je veux une télévision haute qualité", categorie("je veux une télévision haute qualité", df))
#prix("je veux un ordinateur")

#print("test du merge", pd.merge(categorie("i want an expensive phone"), prix("I want an expensive phone")))

