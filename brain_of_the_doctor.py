import os
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")

import base64
def encode_image(image_path):
#    image_path="acne.jpg"
    image_file=open(image_path,"rb")
    return base64.b64encode(image_file.read()).decode('utf-8')


from groq import Groq

query="is there something worng in my face"
model="meta-llama/llama-4-scout-17b-16e-instruct"

def analyze_img_wit_query(query, model, encoded_image):
    client=Groq()
    messages=[
        {
            "role":"user",
            "content": [
                {
                    "type":"text",
                    "text":query
                },
                {
                    "type":"image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }]
    chat_completion=client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content