#pragma once
import subprocess
from const import *
import os

class TERMINAL:
		def __init__(self,ID:int):
				self.name = ID
				self.dict = CONST_DIR
				self.GetAuthorizedList()
				self.database = f"{CONST_DIR}/{self.name}"
				os.system(f"mkdir {self.database}")
				self.shfile = self.database+f"/{self.name}.sh"
				self.batfile = self.database+f"/{self.name}.bat"
				print(self.shfile,self.batfile)
				open(self.shfile,'w').close()
				open(self.batfile,'w').close()

		def GetAuthorizedList(self):
				self.users = {}
				print("authorized list:")
				with open(f"{self.dict}/authorized_list.txt","r",encoding="utf-8") as f:
						for line in f:
								line = line.split(',')
								print(line)
								if len(line) != 2:
									continue
								self.users[int(line[0])] = int(line[1])
				for key,val in self.users.items():
					print(key,val)

		def Clear(self):
				with open(self.shfile,'w',encoding="utf-8") as f:
						f.write('')
				with open(self.batfile,'w',encoding="utf-8") as f:
						f.write('')
				return 0

		def AddCommand(self,s:str):
				if s == "setcourse":
						s = f"cd {self.database}"
				with open(self.shfile,'a',encoding="utf-8") as f:
						f.writelines(s+'\n')
				with open(self.batfile,'a',encoding="utf-8") as f:
						f.writelines(s+'\n')
				return 0

		def Run(self,OsType:str):#return False success,True if failed
				if OsType == 'w':
						print(f"{self.batfile}")
						ret =  subprocess.run(f"{self.batfile}",capture_output=True,text=True).stdout
						return "stdout:\n"+ret.stdout+"\nstderr:\n"+ret.stderr
				elif OsType == 'u' or OsType == 'p' or OsType == 'l':
						ret = subprocess.run(["bash",f"{self.shfile}"],capture_output=True,text=True)
						return "stdout:\n"+ret.stdout+"\nstderr:\n"+ret.stderr
				else:
						return 39

		async def PrintCommand(self,msg):
				re = "```\n"
				with open(self.batfile,'r',encoding="utf-8") as f:
						for lines in f:
								re +=lines
				re += "```"
				await msg.channel.send(re)

		async def AddFile(self,attachment,msg,param):
				fp = f"{self.database}"
				fn = attachment.filename
				if len(param) >= 2:
						fp = param[1]
				if len(param) >= 3:
						fn = ""
						for i in range(2,len(param)):
								if i != 2:
										fn += " "
								fn += param[i]
				fn = fn.replace("/","\u2044")
#fn = fn.replace("'","\\'")
#fn = fn.replace('"',"\\\"")
				fn = fn.replace("?","\uFF1F")
				print(fn)
				cmd = f"mv {self.database}/{attachment.filename} {fp}/{fn}"
				print(cmd)
				await attachment.save(f"{fp}/{fn}")
#os.system(f"cd {self.database}")
#os.system("ls")
#re = os.system(cmd)
#if re != 0:
#await msg.channel.send("move file failed")
#return
				await msg.channel.send(f"added file to {fp}/{fn}")
				return 0

		def CheckAuthorization(self,msg,lvl):#0:no problem;1:there is an issue
				print(self.users)
				print(msg.author.id)
				if msg.author.id in self.users and self.users[msg.author.id] <= lvl:
						return 0
				else:
						return 1

		async def ParamCountError(self,msg,exp:int,rec:int):
				await msg.channel.send(f"error:parameter count:expected {exp},received {rec}")

		async def ParseMessage(self,msg,inp:str):
				inp = inp.split(' ')
				print(inp)
				if inp[0] == "add":
						for i in range(2,len(inp)):
								inp[1] += " "+inp[i]
						if self.CheckAuthorization(msg,100) != 0:
							await msg.channel.send("unauthorized user")
						elif len(inp) < 2:
								await self.ParamCountError(msg,2,len(inp))
						elif self.AddCommand(inp[1]) != 0:
								await msg.channel.send("Failed to add command")
						else:
								await msg.channel.send("added command : "+inp[1])

				elif inp[0] == "run":
						if self.CheckAuthorization(msg,1) != 0:
							await msg.channel.send("unauthorized user")
						elif len(inp) != 2:
								await self.ParamCountError(msg,2,len(inp))
						else:
								await msg.channel.send(f"```\n{self.Run(inp[1])}```")

				elif inp[0] == "clear":
						if self.CheckAuthorization(msg,100) != 0:
								await msg.channel.send("unauthorized user")
						elif len(inp) != 1:
								await self.ParamCountError(msg,1,len(inp))
						elif self.Clear() != 0:
								await msg.channel.send("Failed to run,may be caused by authorization")
						else:
								await msg.channel.send("successfully cleared!")

				elif inp[0] == "print":
						if self.CheckAuthorization(msg,100) != 0:
								await msg.channel.send("unauthorized user")
						elif len(inp) != 1:
								await self.ParamCountError(msg,1,len(inp))
						else:
								await self.PrintCommand(msg)

				elif inp[0] == 'addfile':
						if self.CheckAuthorization(msg,2) != 0:
								await msg.channel.send("unauthorized user")
						elif not msg.attachments:
								await msg.channel.send("no attachments found!")
						else:
								for attachment in msg.attachments:
										await self.AddFile(attachment,msg,inp)
