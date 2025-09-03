import requests
import dotenv
import os
import time
dotenv.load_dotenv()
from google import genai
url = "https://api.perplexity.ai/chat/completions"
headers = {
    "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
    "Content-Type":"application/json"
}
gemini_key = os.getenv("GEMINI_API_KEY")
client = genai.Client()
def gemini(state):
    response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=f"get me all the faculty directory links of colleges in the state {state} it should in the format college name: <link>"
)
    return response.candidates[0].content.parts[0].text
def perplex(payload):
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]
states = {
    "Andhra Pradesh": True,
    "Arunachal Pradesh": True,
    "Assam": True,
    "Bihar": True,
    "Chhattisgarh": True,
    "Goa": True,
    "Gujarat": True,
    "Haryana": True,
    "Himachal Pradesh": True,
    "Jharkhand": True,
    "Karnataka": True,
    "Kerala": True,
    "Madhya Pradesh": True,
    "Maharashtra": True,
    "Manipur": True,
    "Meghalaya": True,
    "Mizoram": True,
    "Nagaland": True,
    "Odisha": False,
    "Punjab": False,
    "Rajasthan": False,
    "Sikkim": False,
    "Tamil Nadu": False,
    "Telangana": False,
    "Tripura": False,
    "Uttar Pradesh": False,
    "Uttarakhand": False,
    "West Bengal": False
}

def get_links(states):
    with open("colleges_faculty_links.txt", "a",encoding="utf-8") as f:
        for state in states:
            if not states[state]:
                payload = {
                    "model": "sonar-pro",
                    "messages":[
                        {
                        "role": "user",
                    "content": f"get me all the faculty directory links of colleges in the state {state} it should in the format college name: <link>"
                        }
                    ]
                }
                f.write(perplex(payload))
                print(f"perplexity for state {state}\n")
                f.write("\n")
                f.write(gemini(state))
                print(f"gemini for state {state}\n")
                time.sleep(5)
            


if __name__ == "__main__":
    get_links(states)



