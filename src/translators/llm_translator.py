import typing as t
import concurrent.futures
from openai import OpenAI  # for calling the OpenAI API
from google import generativeai as genai
from utils.utils import extract_text_from_page, extract_images_from_page

# Set your OpenAI API key

#user_prompt = "tell me the names of 10 most famous women in the world history"
def translate_text_openai(text:str, language:str) -> str:

    client=OpenAI() #api_key=openai_api_key
    system_prompt = "You are an expert in translations, you will be sent an article and you have to translate it into the language suggested. You have to respect the original punctuation and style."
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": f"Translate the text below into {language}: {text}"}
      ]
      )
    return completion.choices[0].message.content.strip()


def translate_text_gemini(text:str, 
                          target_language:str) -> str:
    # genai.configure(api_key= google_api_key)
    model = genai.GenerativeModel(model_name = "models/gemini-1.0-pro-latest", 
                                  generation_config = {"temperature" : 0.3})
    prompt=f"""You are an expert in translations, you will be sent an article and you have to translate it into the language suggested.
                You have to respect the original punctuation and style.

                Please translate the following text to {target_language}:\n\n{text}"""
    response = model.generate_content(prompt).text
    return response.strip()


def translate_page(pages:list,
                   page_num:int, 
                   target_language,
                   llm_to_use:str ='google') -> t.Tuple[int, str]:

    text = extract_text_from_page(pages, page_num)
    # images = extract_images_from_page(pages, page_num)
    images = []
    if llm_to_use == 'google':
        translated_text = translate_text_gemini(text, target_language)
    else:
        translated_text = translate_text_openai(text, target_language)
    return page_num, translated_text , images


def concurent_translate(pages:list,
                        target_language:str, 
                        llm_to_use:str='google') -> t.Tuple[dict[int, str], dict[int, list]]:
    """
    """
    translated_pages = {}
    images_pages = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(translate_page, 
                                   pages,
                                   page_num, 
                                   target_language,
                                   llm_to_use) 
                for page_num in range(len(pages))]
        
        for future in concurrent.futures.as_completed(futures):                
            page_num, translated_text, images = future.result()
            translated_pages[page_num] = translated_text
            images_pages[page_num] = images

    return translated_pages, images_pages