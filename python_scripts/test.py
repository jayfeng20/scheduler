from openai import OpenAI
import os  
import calendar

key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(
  api_key=key,
)

system_message = """
You are a concise and precise assistant. You find the most reasonable time slot(s) to assign this task, 
taking timezone and work-life balance into consideration. Feel free to break it into chunks.
Your output is in the form of a json object with 2 fields named "start_time" and "end_time" whose contents are 
arrays of equal lengths of python datetime objects. They represent the time slot(s) you chose to schedule the task.
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