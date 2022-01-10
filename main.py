import discord
import os
from keep_alive import keep_alive
import requests
from random import randrange
from replit import db

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

ListBooks = []

authors = ["hoover", 'sakavic', 'dessen', 'klune', 'maas', 'chokshi', 'nelson', 'levenseller', 'alexandra+christo',
           'hodkin', 'a.+craig', 'jenkins+reid', 'rogerson', 'riordan',
           'rowell', 'sally+thorne', 'edugyan', 'mahurin', 'holly+black', 'maniscalco', 'emily henry', 'foody',
           'stiefvater', 'elle+kennedy', 'christina+lauren', 'penelope douglas', 'schwab', 'armas', 'schwab', 'king', 'rowling', 'McQuiston', 'hibbert', 'heather+cocks', 'hoang', 'brandon+sanderson', 'bardugo']

def getBooks():
    book = getTitle()
    return book

def getRead(username):
  string = ''
  count = 1
  try: 
    for i in db[username]:
      string += str(count) + '. ' + i + ',\n'
      count+=1  
    return string[:-2]
  except KeyError:
    return False;

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
                    if (keys == 'volumeInfo'):
                        titles.append(dictionaries[keys].get('title'))
                        volumeInfo.append(dictionaries[keys])
    count = 0
    number = randrange(len(titles))
    String = titles[number]

    for value in volumeInfo[number]:
        if value == "authors":
            for aut in volumeInfo[number][value]:
                if count == 0:
                    String += " by: " + aut
                    count += 1
                else:
                    String += ", " + aut
    return String

@client.event
async def on_ready():  # event when bot is ready
    print("Logged in as {0.user}".format(client))

@client.event
async def on_member_join(member):
  guild = client.get_guild(875833944564707329)
  await member.send(f'Welcome to the {guild.name}, {member.name}! Here are some instructions: \n\n$user-username: Before using the other functionalities of the bot, please use $user followed by your username to log into your account. \n$book: will recommend a book to you. \n$read: will add the currently recommended book to your read-list and the bot will NOT recommend this book to you anymore.\n $delete-index: will delete the book from your read-list.\n$logged: will return the currently logged in user\n$show: will return a list of books that you have previously read')

#client = discord.Client()

def update_Books(username, book):

  if username in db.keys():
    try:
      user = db[username]
      user.append(book)
      db[username] = user
    except: 
      db[username] = [book]
  else:
    db[username] = [book]

def delete_Books(username, bookIndex):
  user = db[username]
  bookIndex = int(bookIndex) - 1
  if len(user) > bookIndex:
    book = user[bookIndex]
    del user[bookIndex]
    db[username] = user
  return book

def checkUser(username):
  if username in db.keys():
    return False
  else:
    return True


userBool = False
username = ""

@client.event
async def on_message(message):
    global username
    global userBool
    newBook = getBooks()
    msg = message.content
    if client.user.mentioned_in(message):
        await message.channel.send("Welcome to Noura's Book Recommendation Bot! Here are the instructions:\n\n$user-username: Before using the other functionalities of the bot, please use $user followed by your username to log into your account. \n$book: will recommend a book to you. \n$read: will add the currently recommended book to your read-list and the bot will NOT recommend this book to you anymore.\n $delete-index: will delete the book from your read-list.\n$logged: will return the currently logged in user\n$show: will return a list of books that you have previously read")

    if msg.startswith("$user"):
      try:
        username = msg.split("$user ", 1)[1]
        await message.channel.send("Are you a new user?\nPlease send '$yes' or '$no'")
      except IndexError:
        await message.channel.send("Please enter your username using $user")

    
    if msg.startswith("$yes"):
      if checkUser(username) == False:
        await message.channel.send("This username is already taken, please use $user and input a new user name")
      else:
            userBool = True
            ListBooks.append(newBook)
            await message.channel.send(newBook)
    
    if msg.startswith("$no"):
        userBool = True
        ListBooks.append(newBook)
        await message.channel.send(newBook)

    if message.content.startswith("$book"):
        if userBool == True:
            ListBooks.append(newBook)
            await message.channel.send(newBook)
        else:
            await message.channel.send("Please enter your username using $user")
  
    if message.content.startswith("$read"):
      if userBool == True:
        if len(ListBooks) > 0:
            update_Books(username, ListBooks[-1])
            ListBooks.remove(ListBooks[-1])
            await message.channel.send("Book will be added to your read-list")
        else:
            await message.channel.send("Please enter username with $user")
      else:
        await message.channel.send("Please enter your username using $user")
    
    if message.content.startswith("$show"):
      if userBool == True:
        if not getRead(username):
           await message.channel.send("Read-list is empty.")
        else:
          await message.channel.send(getRead(username))
          await message.channel.send("\nUse $delete followed by the book number to delete a book from the list.")
      else:
        await message.channel.send("Please enter your username using $user")
    
    if message.content.startswith("$delete"):
      if userBool == True:
        index=msg.split("$delete ", 1)[1]
        book = delete_Books(username, index)
        ListBooks.append(book)
        await message.channel.send(book + " has been deleted.")
      else:
        await message.channel.send("Please enter your username using $user")
    
    if message.content.startswith("$logged"):
      if userBool == True: 
        await message.channel.send(username + " is currently logged in.")
      else:
        await message.channel.send("Please enter your username using $user")
    
    if message.author == client.user:
        return


my_secret = os.environ['DISCORDTOKEN']

keep_alive()
client.run(my_secret)