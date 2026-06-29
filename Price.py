import streamlit as st
from PIL import Image
import google.generativeai as genai

#Gemini API Key
GEMINI_API_KEY = st.secrets['GEMINI_API_KEY']
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

#Streamlit UI
st.set_page_config(
    page_title='AI Price Estimator',
    layout='centered'
)
st.title('AI Item Estimator')
st.write(
    'Upload an image and provide description.'
)
uploaded_file = st.file_uploader(
    'Upload Image',
    type=['jpg','jpeg','png','webp']
)
description = st.text_area(
    'Item Description',
    placeholder='Example: Used iPhone 14 Pro 256GB, excellent condition, purchased on 2023...'
)

#Price Estimation
if st.button('Estimate Price'):
    if uploaded_file is None:
        st.warning('Please upload an image.')
        st.stop()
    image = Image.open(uploaded_file)
    st.image(
        image,
        caption='Uploaded Item',
        use_container_width=True
    )

    prompt = f'''
    You are an expert product valuation specialist.

    Ananlyze the uploaded image and the user's description.

    User Description:
    {description}

    Determine:

    1. What the item appers to be.
    2. Its likely condition.
    3. Estimated price range in USD.
    4. Estimated price range in INR.
    5. Cofidence score (0-100%).
    6. Key factors affectig the valuation.
    7. A short summary.

    Return the answer in a clean markdown format.
    '''

    try:
        with st.spinner('Analyzing item and estimating value...'):
            response = model.generate_content(
                [prompt, image]
            )

        st.subheader('Estimated Value')
        st.markdown(response.text)
    except Exception as e:
        st.error(f'Error:{e}')
        