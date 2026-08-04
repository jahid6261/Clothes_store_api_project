from ollama import Client

client = Client(host="http://host.docker.internal:11434")


def phi3(messages):
    return client.chat(
        model="phi3",
        messages=messages,
        stream=True,
    )