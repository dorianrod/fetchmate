import os
import openai
import logging


def ask_chatgpt(role, context_messages, engine="MySQL"):
    openai.api_key = os.getenv("OPENAPI_KEY_API")

    messages = [
        {
            "role": "system",
            "content": role,
        }
    ]
    for message in context_messages:
        messages.append({"role": "user", "content": message})

    logging.info(message)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )
    usage = completion['usage']
    response = completion.choices[0].message.content
    return response, usage
