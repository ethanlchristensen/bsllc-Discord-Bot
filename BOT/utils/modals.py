import os
import time
import discord
from discord.ui import Modal
from discord import ui as UI
from discordwebhook import Discord
from utils.openaiprompter import OpenAIPrompter


class OpenAIPasswordInputModal(Modal):
    def __init__(self, prompt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_item(
            UI.TextInput(
                label="Enter the password to use this command",
                style=discord.TextStyle.short,
            )
        )
        self.prompt = prompt
        self.prompter = OpenAIPrompter()
        self.marcus = Discord(url=os.getenv("MARCUS"))
        self.marcus_id = int(os.getenv("MARCUS_ID"))

    async def on_submit(self, interaction: discord.Interaction):
        
        await interaction.response.defer()
        
        username = interaction.user.global_name
        
        chat_history = interaction.client.globals.get("chat_history")
        
        if chat_history.get(username):
            chat_history_text = ""
            
            for message in chat_history[username]:
                chat_history_text += f"Name {username}: {message[0]}\nMarcus (you): {message[1]}\n"
            
            print(chat_history_text)
        else:
            chat_history_text = "NO CHAT HISTORY YET"
        
        original_response = self.prompter.complete(prompt=f"CHAT HISTORY:\n{chat_history_text}\n User Question: " + self.prompt, password=self.children[0].value)
        
        if original_response:
            if username in chat_history:
                chat_history[username].append((self.prompt, original_response.content))
                
                if len(chat_history[username]) > 5:
                    chat_history[username].pop(0)
            else:
                chat_history[username] = [(self.prompt, original_response.content)]
            
            response = original_response.content.split(" ")
    
            full_response = f"{interaction.user.global_name}: {self.prompt}\n\n"

            message = await interaction.followup.send(content=full_response)
                
            for word in response:
                full_response += word + " "
                await message.edit(content=full_response)
                time.sleep(0.075)
        else:
            await interaction.followup.send(content="ERROR")
        
        # if self.marcus_id:
        #     webhooks = await interaction.guild.webhooks()

        # await interaction.response.defer()

        # # update marcus to response where the command was called
        # if self.marcus_id:
        #     for webhook in webhooks:
        #         if webhook.id == self.marcus_id:
        #             await webhook.edit(channel=interaction.channel)

        # password = self.children[0].value

        # try:
        #     marcus_should_say = self.prompter.complete(
        #         prompt=self.prompt, password=password
        #     )

        #     if marcus_should_say is not None:
        #         await interaction.followup.send(content=self.prompt)
        #         self.marcus.post(content=marcus_should_say.content)
        #     else:
        #         await interaction.followup.send(content="ERROR")
        # except Exception as exception:
        #     print(f"[ERROR] /chat: {exception}")
        #     await interaction.followup.send(content="ERROR")