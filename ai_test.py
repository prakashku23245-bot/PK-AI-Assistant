import ollama

response = ollama.chat(
    model='phi3:mini',
    messages=[
        {'role': 'user', 'content': 'Who are you?'}
    ]
)

print(response['message']['content'])