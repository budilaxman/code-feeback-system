import google.generativeai as genai
import dotenv 
from analysis import result

dotenv.load_dotenv()


def gen_feedback(analysis):
    genai.configure(api_key="AIzaSyBwP0R7cwMyQaNWP11eE8RCBnLTeHKE6rI")
    model = genai.GenerativeModel("gemini-1.0-pro")
    prompt = analysis
    prompt +="Instructions: These are the  errors that i got, give me result and approach how can i improve my code and follow those guidelines that are violated above"
    response = model.generate_content(prompt)
    return response.text



