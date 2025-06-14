import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ServiceUnavailable

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
print("API_KEY LOADED IS:", API_KEY)
genai.configure(api_key = API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


def calculator_baba(expression:str)->str:
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"kuchh bakchodi ho gyi : {e}"
    

def extract_expression(query:str)->str:
    prompt = f"""You are a math assistant and your job is to extract mathematical expressions
    that can be solved by python's eval() function out of text queries or world problems.
    For example, if the user asks - 'What is the sum of all one digit natural numbers',
    then the expression would be '1+2+3+4+5+6+7+8+9'. 
    Another example, if the user asks - 'What is 10 percent of the surface of sun's temperature?'
    then, the expression would be '10/100*5500'.
    ***You are strictly urged to only return the python compatible eval() function expression!***
    
    Input: {query}
    Output:"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip("`\n")
    except ServiceUnavailable:
        print(" Gemini is overloaded. Chill for a bit and try again later.")
        return "MODEL_OVERLOADED"
    
    
def get_final_response(query:str):
    expr = extract_expression(query)
    print(f"The extracted expresion is - {expr}")
    result = calculator_baba(expr)
    prompt = f"""User asked for this : {query}
                Math expression is : {expr}
                Result is : {result}

                Now, please give a user friendly and readable final output to display to the user."""
    response=  model.generate_content(prompt)
    return response.text.strip()


while(True):
    try:
        query = input("Hello there, what doubts can I help with? Just lay it on me :)").strip()
        if query.lower() in ['exit', 'quit', 'bye']:
            print("Alright, Im done here, hope I helped!!")
            break
        final_answer = get_final_response(query)

        if final_answer == "MODEL_OVERLOADED":
            print("System is overloaded!! Please chill out, smoke a malboro and try again later.")
            continue
        print("Here is youur answer : ", final_answer)

    except KeyboardInterrupt:
        print("Alright, lets terminate this sesh!")
        break

    except Exception as e:
        print("There seems to be a problem : {e}")

 