import google.generativeai as genai
import re

def genai_call(prompt):
    API_KEY = "AIzaSyB_aBJqtL3B4s52Y6tIXIJ17Kn_ripK-7I"
    system_instruction_content = " just give ans only and only releted to python nothing else"
    genai.configure(api_key=API_KEY)

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt_content = prompt

        #response = model.generate_content(prompt_content)
        response = model.generate_content(
        contents=[
            {"role": "user", "parts": [system_instruction_content]}, 
            {"role": "user", "parts": [prompt_content]}              
        ]
        )

        return response.text

    except Exception as e:
        print(f"An error occurred: {e}")


prompt=input(">")
response= genai_call(prompt)
print(response)









def talk_to_gemini(message_history):
    API_KEY = "AIzaSyB_aBJqtL3B4s52Y6tIXIJ17Kn_ripK-7I" 
    
    genai.configure(api_key=API_KEY)

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  
        response = model.generate_content(message_history)
        
        # print("\n--- Gemini's Raw Reply ---")
        # print(response.text)
        raw_text=response.text
        cleaned_text = re.sub(r"^```(?:json)?\s*|```$", "", raw_text, flags=re.MULTILINE).strip()
        return cleaned_text

    except Exception as e:
        print(f"\nAn unexpected error happened: {e}")
        return None
    





system_instruction_content = """YOu are an ai expert, you just need to validate the ans of open ai is correct or not?
        You are an helpful AI assistence who is expert in d to validating the result of open ai is correct or not?.
        for the given user input, you just need to validate like this in below example.
        The steps are you get the user input you think and validate the result.
        follow the steps in Sequance that is "Analyze","Think","Output","validate" and finally " Result".

        Rules:
        1: follow the strict json output as per Schema.
        2: Always Perfom one Step at a time and wait for next input
        3:Carefully analyze the user Query.;

        Output Format:
            {"step":"format",content:"string"}.

        Example:

        Example:
        input: what is 2+2*5/2?
         output:{{"step":"Analyze","content":"Alright! The use is intrested in basic math operations."}}
         output:{{"step":"Think","content":"to perform this addition i must use BODMAS rule."}}
        output:{{"step":"Validate","content":"Correct! the open ai response is right hhere using bodmas is the right approch here."}}
        and so on....
        """


chat_conversation = [
    {"role": "user", "parts": [{"text": system_instruction_content}]}
]

print("Hello! Type your message. Type 'exit' to quit.")

while True:
    user_input = input("You: >>> ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    chat_conversation.append({"role": "user", "parts": [{"text": user_input}]})

    gemini_reply = talk_to_gemini(chat_conversation)

    if gemini_reply:
        print(f"Gemini: {gemini_reply}")
        chat_conversation.append({"role": "model", "parts": [{"text": gemini_reply}]})
    else:
        print("No reply from Gemini.")
