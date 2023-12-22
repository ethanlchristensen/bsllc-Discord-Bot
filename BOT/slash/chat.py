import time
import discord
from utils.modals import OpenAIPasswordInputModal
from utils.openaiprompter import OpenAIPrompter


class Chat:
    """
    Description: adds two numbers.
    """

    def __init__(self, tree, guild, kwargs=None):
        """
        Description: Constructor.
        """
        
        prompter = OpenAIPrompter()

        @tree.command(
            name="chat",
            description="chat with Jade",
            guild=discord.Object(id=guild),
        )
        async def chat(interaction, message: str):
            """
            /chat command
            """

            await interaction.response.defer()
        
            username = interaction.user.global_name
            
            chat_history = interaction.client.globals.get("chat_history")
            
            if chat_history.get(username):
                chat_history_text = ""
                
                for past_message in chat_history[username]:
                    chat_history_text += f"{username}: {past_message[0]}\Jade: {past_message[1]}\n"
                
                print(chat_history_text)
            else:
                chat_history_text = "NO CHAT HISTORY YET"
            
            original_response = prompter.complete(prompt=f"CHAT HISTORY:\n{chat_history_text}\nEND CHAT HISTORY\nUser Question: " + message + "\nJade: ", password="awesomeisethan")
            
            if original_response:
                if username in chat_history:
                    chat_history[username].append((message, original_response.content))
                    
                    if len(chat_history[username]) > 5:
                        chat_history[username].pop(0)
                else:
                    chat_history[username] = [(message, original_response.content)]
                
                # response = original_response.content.split(" ")
        
                full_response = f"{interaction.user.global_name}: {message}\n\n" + original_response.content

                message = await interaction.followup.send(content=full_response)
                    
                # for word in response:
                #     full_response += word + " "
                #     await message.edit(content=full_response)
                #     time.sleep(0.01)
            else:
                await interaction.followup.send(content="ERROR")
            
            
            # modal = OpenAIPasswordInputModal(prompt=message, title="Chat Password")

            # await interaction.response.send_modal(modal)