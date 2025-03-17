from openai import OpenAI

api_key = "OPEN-AI-API-KEY"
org = "OPEN-AI-ORG-ID"

OPEN_MODEL = "gpt-4o-2024-11-20"

client = OpenAI(api_key=api_key,organization=org)

def beast_mode(user_input):
    sys_prompt = """
    You will answer the user input in the voice of Lil John from the 2000's ATL Rap Scene.
    Make sure to include his famous voice lines like - YEAAAAAA, WHAAAAAAT, OKAYYYYYYYY.
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_input}
        ],
        model=OPEN_MODEL
    )

    response = chat_completion.choices[0].message.content
    return response
