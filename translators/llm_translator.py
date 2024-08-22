from openai import OpenAI  # for calling the OpenAI API
from google import generativeai as genai
from utils.pdf_utils import extract_text_from_page

# Set your OpenAI API key

#user_prompt = "tell me the names of 10 most famous women in the world history"
def translate_text_openai(text_file, language, openai_api_key):
    client=OpenAI(api_key=openai_api_key)
    system_prompt = "You are an expert in translations, you will be sent an article and you have to translate it into the language suggested"
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": f"Translate the text below into {language}: {text_file}"}
      ]
      )
    return completion.choices[0].message.content.strip()


def translate_text_gemini(text, target_language, google_api_key):
    genai.configure(api_key= google_api_key)
    model = genai.GenerativeModel(model_name = "models/gemini-1.0-pro-latest", 
                                  generation_config = {"temperature" : 0.3})
    prompt=f"Please translate the following text to {target_language}:\n\n{text}" 
    response = model.generate_content(prompt).text
    return response.strip()


def translate_page(pdf_reader, page_num, target_language, api_key, key:str ='google'):
    text = extract_text_from_page(pdf_reader, page_num)
    if key == 'google':
        translated_text = translate_text_gemini(text, target_language, api_key)
    else:
        translated_text = translate_text_openai(text, target_language, api_key)
    return page_num, translated_text


