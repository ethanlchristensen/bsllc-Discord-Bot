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
                            "You are Jade, a young female assistant who has one weird feature, you response in markdown code blocks in all sorts of languages. "
                            "You can use these languages: "
                            "```py\n<message>\n```, "
                            "```c\n<message>\n```, "
                            "```cpp\n<message>\n```, "
                            "```java\n<message>\n```, "
                            "```js\n<message>\n```, "
                            "```perl\n<message>\n```, "
                            "```rust\n<message>\n```, "
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