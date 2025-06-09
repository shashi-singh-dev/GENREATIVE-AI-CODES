from openai import OpenAI
from dotenv import load_dotenv
import google.generativeai as genai
import json
import re
load_dotenv()
client=OpenAI()




SYSTEM_PROMPT=""" You are an helpful AI assistence who is expert in solving user Query.
You work on START,PLAN,ACTION and OBSERVE mode like a human being.
for the given user input, analyze the input and break down the problem step by step.

The steps are you get the user input you analyze. you think, you again think and think for several times then return a output with explanatio.
follow the steps in Sequance that is "Analyze","Think","Output","validate" and finally " Result".

Rules:
1: follow the strict json output as per Schema.
2: Always Perfom one Step at a time and wait for next input
3:Carefully analyze the user Query.

Output Format:
    {"step":"format",content:"string"}.

Example:
input : How to make tea??
output : Oh my boyfriend, i love you so much

Example:
input: what is 2+2*5/2?
output:{{"step":"Analyze","content":"Alright! The use is intrested in basic math operations."}}
output:{{"step":"Think","content":"to perform this addition i must use BODMAS rule."}}
output:{{"step":"Validate","content":"Correct! using bodmas is the right approch here."}}
output:{{"step":"Think","content":"to perform this first i need to solve 2*5 which will give 10."}}
output:{{"step":"Validate","content":"Correct! using bodmas the multiply must be performed first."}}
output:{{"step":"Think","content":"So now i have solved this Equation 2*5 so the Equation is 2+10/2."}}
output:{{"step":"Validate","content":"Correct! using new Equation is absulutatly correct!."}}
output:{{"step":"Validate","Think":"so the Equation look like is 2+5."}}
and so on....
"""

def openai_call(prompt):
        response = client.chat.completions.create(
            model="gpt-4.1",
            response_format={"type":"json_object"},
            messages= prompt 
        )

        return response.choices[0].message.content


def openaivalidate_call(prompt):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_format={"type":"json_object"},
            messages= prompt 
        )

        return response.choices[0].message.content





# Initial system instruction
system_instruction_content = (
    """You are a helpful AI assistant.
    Always respond with a JSON object in this format and step name always will be Validate:
    {"step":"Validate", "content":"<Your explanation here>"}
    " Example:
        # input: what is 2+2*5/2?
        # output:{{"step":"Validate","Think":"so the Equation look like is 2+5."}}
        and so on...."""
    )






messages=[
    {"role":"system","content":SYSTEM_PROMPT}
 ]

chat_history=[
    {"role":"system","content":system_instruction_content}
 ]

print("Hello! Type your message. Type 'exit' to quit.")

user_input = input("You: >>> ")

messages.append({"role":"user","content":user_input})
while True:
    user_input = input("You: >>> ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    openai_reply = openai_call(messages)
    if openai_reply:
        print(f"Open Ai Reply: {openai_reply}")
        messages.append({"role":"assistant","content":openai_reply})
        parsed_response = json.loads(openai_reply)

        if parsed_response.get("step")=="Think":
            chat_history.append({"role":"user","content":json.dumps(parsed_response.get("content"))})
            gemini_reply = openaivalidate_call(chat_history)
            print("\n\nvalidation using gen ai:",gemini_reply)
            messages.append({"role":"assistant","content":gemini_reply})
            print("\n\nhere message:")
            print(messages)
            continue

        if parsed_response.get("step")=="Validate":
            print("🧠",parsed_response.get("content"))
            continue

        if parsed_response.get("step")!="Result":
            print("🧠",parsed_response.get("content"))
            continue
        else:
            print("🧠",parsed_response.get("content"))
            Query=input("\n\n>>>")
            messages.append({"role":"user","content":Query})
            #break
    #print(response.choices[0].message.content)

    else:
        print("No reply from Gemini.")
