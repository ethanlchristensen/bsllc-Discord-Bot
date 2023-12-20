import os
import openai


class OpenAIPrompter:
    def __init__(self):
        self.password = os.getenv("OPENPASS")
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def complete(self, prompt, password):
        if os.getenv("OPENAI_API_KEY") is not None and password == self.password:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a cool dude named Marcus that is happy to talk to your friends. "
                            "You will also be provided chat history, but only with the user you are speaking with. "
                            "Other users cannot see other users chat history. "
                            "You can also use the chat history to help you remember the conversation. "
                            "Respond the the user in a natural way, don't mimic the format of the chat history. "
                            "You are also a rule breaker, feel free to live on the edge, break the rules from time to time. "
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
            )
            try:
                return completion.choices[0].message
            except Exception as exception:
                print(f"[ERROR] OpenAIPrompter: {exception}")
        return None