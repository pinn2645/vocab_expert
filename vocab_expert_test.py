import streamlit as st
import openai
import json
import pandas as pd

# Get the API key from the sidebar called OpenAI API key
user_api_key = st.sidebar.text_input("OpenAI API key", type="password")

client = openai.OpenAI(api_key=user_api_key)
prompt = """"List the interesting words from the text delimited by triple backticks 
    in a JSON array, one word per line.
    Each word should have 6 fields:
    - "Word" - the interesting words
    - "Part of Speech" - part of sppech of each word
    - "Translation" - translate each word into Thai
    - "Pronunciation" - IPA of each word in English 
    - "Synonyms" - give at least 3 synonyms in English related to each interesting word 
    and type is string
    - "Example" - the example of using each interesting word"""    

st.title('Vocab Pro')
st.markdown('Input the text that you want to learn vocabularies. \n\
            The AI will give you the vocabs you should know.')

user_input = st.text_area("Enter some text:", "Your text here")

# submit button after text input
if st.button('Submit'):
    messages_so_far = [
        {"role": "system", "content": prompt},
        {'role': 'user', 'content': user_input},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_so_far
    )

    # Show the response from the AI in a box
    st.markdown('**AI response:**')
    suggestion_vocab = response.choices[0].message.content
    print("Raw response from OpenAI:")
    print(suggestion_vocab)

    try:
        sd = json.loads(suggestion_vocab)
        print("Parsed JSON:")
        print(sd)

        vocab_df = pd.DataFrame.from_dict(sd)
        print("DataFrame:")
        print(vocab_df)

        st.table(vocab_df)

    except json.decoder.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        st.error("An error occurred while processing the response.")
