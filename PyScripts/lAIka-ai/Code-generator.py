

import openai
import os

openai.api_key = ""
def generate_code():
  try:

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",  "content": "generate a HTTP request to the server"
            }
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content.strip()
  except Exception as e:
      print(f"An error occurred: {str(e)}")
      return None

if __name__ == "__main__":
  response = generate_code()
  print(response)
