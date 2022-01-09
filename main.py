import discord
import os
from keep_alive import keep_alive
import requests
from random import randrange
from replit import  db
import sqlite3


ListBooks = []
usernamesDict = {}
authors = ["hoover", 'sakavic', 'dessen', 'klune', 'maas', 'chokshi', 'nelson', 'levenseller', 'alexandra+christo',
           'hodkin', 'a.+craig', 'jenkins+reid', 'rogerson', 'riordan',
           'rowell', 'sally+thorne', 'edugyan', 'mahurin', 'holly+black', 'maniscalco', 'emily henry', 'foody',
           'stiefvater', 'elle+kennedy', 'christina+lauren', 'penelope douglas', 'schwab', 'armas', 'schwab']

def getBooks():
    book = getTitle()
    return book
def userBooks(username, book):
    if username not in usernamesDict:
        usernamesDict[username] = [book]
        db[username] = [book]
        return book
    else:
        list = usernamesDict.get(username)
        for i in list:
            if i == book:
                getTitle()
            else:
                list.append(book)
                return book

def getRead(username):
   return usernamesDict.get(username)
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

client = discord.Client()


@client.event
async def on_ready():  # event when bot is ready

    print("Logged in as {0.user}".format(client))



userBool = False
username = ""
#fix
@client.event
async def on_message(message):
    global username
    global userBool
    newBook = getBooks()
    msg = message.content
    if message.content.startswith("$book"):
        if userBool == True:
            ListBooks.append(newBook)
            await message.channel.send(newBook)
        else:
            await message.channel.send("please enter your username using $user")
    if msg.startswith("$user"):
        userBool = True
        username = msg.split("$user ", 1)[1]
        ListBooks.append(newBook)
        await message.channel.send(newBook)
    if message.content.startswith("$read"):
        if len(ListBooks) > 0:
            userBooks(username, ListBooks[-1])
            ListBooks.remove(ListBooks[-1])
            await message.channel.send("book will be added to your read-list")
        else:
            await message.channel.send("Please enter username with $user")
    if message.content.startswith("$show"):
        await message.channel.send(getRead(username))
    if message.author == client.user:
        return





my_secret = os.environ['DISCORDTOKEN']

keep_alive()
client.run(my_secret)