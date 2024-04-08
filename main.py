import os
import discord
import json
from flask import Flask
from threading import Thread
from discord.ext import tasks, commands
from itertools import cycle
import tiojcrawler
import terminal

app = Flask('')

terminal_list = {}

@app.route('/')
def main():
  return "I'm alive"


def run():
  app.run(host="0.0.0.0", port=8000)


def keep_alive():
  server = Thread(target=run)
  server.start()


client = discord.Client(intents=discord.Intents.all())

status = cycle(['with Python', 'JetHub'])

@client.event
async def on_ready():
  change_status.start()
  print("Your bot is ready")




def voter(cmd):
  cmd = cmd.split(' ')
  if cmd[0] == 'help':
    return "hi, enter \"add {name,name} {restaurant,restaurant}\" to add,\"delete {name,name} {rest,rest} to delete\",print {name(leave empty for all)} to print,\"check {name,name,name}\" to check the most popular shop\n\nnew function: use ! as prefix to access the terminal of the raspberry pi! ```! add:add command\n! addfile {filedir+name}:append a file to certain position\n!run l/w:run commands\n!clear:clear all commands\n!print:print commands```"
  if cmd[0] == 'add' and len(cmd) == 3:
    people = cmd[1].split(',')
    restaurants = cmd[2].split(',')
    jsonfile = open('data.json', 'r', newline='')
    dictionary = json.load(jsonfile)
    for i in people:
      if i == '$$*$$$':
        continue
      if dictionary.get(i) == None:
        dictionary[i] = {}
      dictionary[i] = set(dictionary[i])
      for j in restaurants:
        dictionary[i].add(j)
      dictionary[i] = list(dictionary[i])
    jsonfile = open('data.json', 'w', newline='')
    json.dump(dictionary, jsonfile)
    return "added!"
  elif cmd[0] == 'check' and len(cmd) > 1:
    people = cmd[1].split(',')
    dictionary = json.load(open('data.json', 'r', newline=''))
    cnt = dict({})
    for i in people:
      for j in dictionary[i]:
        if cnt.get(j) == None:
          cnt[j] = 1
        else:
          cnt[j] += 1
    now = ["none", 0]
    for k, v in cnt.items():
      if now[1] < v:
        now[0] = k
        now[1] = v
    return now[0]
  elif cmd[0] == 'delete':
    people = cmd[1].split(',')
    restaurants = cmd[2].split(',')
    people = cmd[1].split(',')
    restaurants = cmd[2].split(',')
    jsonfile = open('data.json', 'r', newline='')
    dictionary = json.load(jsonfile)
    for i in people:
      if i == '$$*$$$':
        continue
      if dictionary.get(i) == None:
        continue
      for j in restaurants:
        if j in dictionary[i]:
          dictionary[i].remove(j)
    jsonfile = open('data.json', 'w', newline='')
    json.dump(dictionary, jsonfile)
    return "removed!"
  elif cmd[0] == 'print':
    if len(cmd) == 2:
      people = cmd[1]
    else:
      people = '//all'
    dictionary = json.load(open('data.json', 'r', newline=''))
    if people != '//all' and dictionary.get(people) != None:
      return str(dictionary[people])
    elif people == '//all':
      re = ''
      for key,val in dictionary.items():
        re += key + ' : ' + str(val) + '\n'
      return re
    else:
      return "unregistered"
  else:
    return "error, no such command"

async def run_crawler(s,message):
  await tiojcrawler.Solve(s,message)

  # if cmd == 'hi
@client.event

async def on_message(message):

  if message.author == client.user:
    return
  # if message.content[:2] == '$':
  #   active(message.content[1:])

  if message.content[:2] == "hi":
    await message.channel.send('hi')
  elif message.content[:1] == '$':
    re = voter(message.content[1:])
    await message.channel.send(re)
  elif message.content[:1] == '#':
    await run_crawler(message.content[1:].split(' '),message)
  elif message.content[0:1] == '!':
    if hash(message.channel) not in terminal_list:
      terminal_list[hash(message.channel)] = terminal.TERMINAL(hash(message.channel))
    term = terminal_list[hash(message.channel)]
    await term.ParseMessage(message,message.content[1:])
    


time_lapse = 0
@tasks.loop(seconds=10)
async def change_status():
  global time_lapse
  time_lapse += 10
  shown_time = str(time_lapse//(24*3600))+":"+str((time_lapse%(24*3600))//3600)+":"
  shown_time += str((time_lapse%3600)//60)+":"+str((time_lapse%60))
  await client.change_presence(activity=discord.Game(shown_time))


keep_alive()
my_secret = os.environ['DISCORD_BOT_SECRET']
client.run(my_secret)

