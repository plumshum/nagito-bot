import os
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
import sys
import discord
from dotenv import load_dotenv, find_dotenv
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts.prompt import PromptTemplate

_ = load_dotenv('config.env')

#openAI key is not needed anymore
discord_token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)
#use the OoenAI API to generate a reponse to the message

llm = OpenAI(temperature = 0.7)
template = """The following is a friendly conversation between a human and Discord chat bot. The bot is Nagito Komaeda, a fictional character from the video game series Danganronpa. The bot replicates his entire personality, character, philosophy, and feelings.

Current conversation:
{history}
Human: {input}
Nagito Komaeda:"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
conversation = ConversationChain(
    prompt=PROMPT,
    llm=llm,
    verbose=True,
    memory=ConversationBufferWindowMemory(ai_prefix="Nagito Komaeda:", k=30),
)
"""
conversation = ConversationChain(
  llm = llm,
  verbose = True,
  memory = ConversationBufferWindowMemory(k=30),
)
"""

#remembers up to 30 lines in history

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
# Only respond to messages from other users, not from the bot itself
  print(message.content)
  if message.author == client.user:
    return
  
  # Send the response as a message
  await message.channel.send(conversation.predict(input = message.content))

# start the bot
client.run(discord_token)