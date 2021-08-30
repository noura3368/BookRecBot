import discord
import os
from keep_alive import keep_alive

import requests
from random import randrange
authors = ["hoover", 'sakavic', 'dessen', 'klune', 'maas', 'chokshi', 'nelson', 'levenseller', 'alexandra+christo', 'hodkin', 'a.+craig', 'jenkins+reid', 'rogerson', 'riordan',
          'rowell', 'sally+thorne', 'edugyan', 'mahurin', 'holly+black', 'maniscalco', 'emily henry', 'foody', 'stiefvater', 'elle+kennedy', 'christina+lauren', 'penelope douglas', 'schwab', 'armas']


def getTitle():
   randomauthor = randrange(len(authors))
   authorpicked = authors[randomauthor]
   link = 'https://www.googleapis.com/books/v1/volumes?q=inauthor:' + authorpicked + '&printType=books&langRestrict=en&key=AIzaSyAwuZrfSl8Nm4szFuVV6pxu2Z9hkWQpDkM'
   response = requests.get(link)
   books = response.json()
   titles = []
   volumeInfo = []
   for i in books:
       if isinstance(books[i], list):
           for dictionaries in books[i]:
               for keys in dictionaries:
                   if(keys == 'volumeInfo'):
                       titles.append(dictionaries[keys].get('title'))
                       volumeInfo.append(dictionaries[keys])
   count = 0
   number = randrange(len(titles))
   String = titles[number]

   for value in volumeInfo[number]:
       if value == "authors":
           for aut in volumeInfo[number][value]:
             if count == 0:
                String+= " by: " + aut
                count+=1
             else:
                String+= ", " + aut
   return String




client = discord.Client()
@client.event
async def on_ready(): #event when bot is ready
   print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
   if message.author == client.user:
       return
   if message.content.startswith("$book"):
       await message.channel.send(getTitle())


my_secret = os.environ['DISCORDTOKEN']

keep_alive()
client.run(my_secret)