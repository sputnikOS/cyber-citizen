Iimport os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
      model="gpt-4",
        messages=[
                {
                          "role": "user",  "content": ""
                }
        ],
          temperature=0,
            max_tokens=1024,
              top_p=1,
                frequency_penalty=0,
                  presence_penalty=0
)
                }
        ]
)
