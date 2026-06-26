import openai

client = openai.OpenAI(api_key="none", base_url="https://opencode.ai/zen/v1")

try:
    response = client.chat.completions.create(
        model="big-pickle",
        messages=[{"role": "user", "content": "hi"}],
        stream=True,
    )
    for chunk in response:
        print(chunk)
except Exception as e:
    print("ERROR:", repr(e))
