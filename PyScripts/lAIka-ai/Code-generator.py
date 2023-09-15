import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
      model="gpt-4",
        messages=[
                {
                          "role": "user",
                                "content": "Write a Python function that takes as input a file path to an image, loads the image into memory as a numpy array, then crops the rows and columns around the perimeter if they are darker than a threshold value. Use the mean value of rows and columns to decide if they should be marked for deletion."
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
