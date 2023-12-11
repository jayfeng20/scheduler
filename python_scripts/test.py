from openai import OpenAI
import os  
import calendar

key = os.environ.get("OPENAI_API_KEY")
os.environ.get("OPENAI_API_KEY")
client = OpenAI(
  api_key=key,
)


system_message = """
You are a concise and precise assistant. You find the most reasonable time slot(s) to assign this task, 
taking timezone and work-life balance into consideration. Feel free to break it into chunks.
Your output is in the form of a json object with only 1 field that's named 'slot' with its content in the form of 
'00(Hour from 0 to 24) XX(Month)/XX(day)/XXXX(Year) - 00(Hour):00(Minute) XX(Month)/XX(day)/XXXX(Year)'
"""

user_message = "Can you please find the best time slot(s) for me to do the following task?" + \
"""

"""


completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  response_format={ "type": "json_object" },
  
  
  messages=[
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_message}
  ],
  max_tokens=4,
  n=1,
  top_p=0.3 # TODO: need finetuning

)

print(completion.choices[0].message)