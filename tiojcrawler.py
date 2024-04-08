from bs4 import BeautifulSoup
import requests
import time

user = ''
solved = []
topcoders = []
async def Init(message):
    global topcoders,solved,user
    topcoders = []
    solved = []
    mp = {}
    for i in range(1,14):
        await message.channel.send('processing:'+str(i)+'/13')
        now_page = 'https://tioj.ck.tp.edu.tw/problems?page='+str(i)
        re = requests.get(now_page)
        soup = BeautifulSoup(re.text,'html.parser')
        soup = soup.find(class_ = 'table-hover')
        soup = soup.find('tbody').find_all('tr')
        for i in soup:
            tmp = i.find_all('td')
            # await message.channel.send(tmp[1].text,tmp[2].text,tmp[3],tmp[4].text)
            if tmp[3].find('a') != None:
                coder = tmp[3].find('a')['href'][7:]
                # await message.channel.send(coder)
                if coder in mp:
                    mp[coder].append(tmp[1].text)
                else:
                    mp[coder] = [tmp[1].text]

    user = input('enter user id:\n')
    solved = GetProblems("https://tioj.ck.tp.edu.tw/users/"+user)
    for i in mp:
        topcoders.append([i,mp[i]])
    topcoders = sorted(topcoders,key=lambda x:(len(x[1]),x[0]))
    while type(solved) == type('hi'):
        await message.channel.send('invalid user name')
        user = input('enter user id:\n')
        solved = GetProblems("https://tioj.ck.tp.edu.tw/users/"+user)
    er = []
    for i in solved:
        if i[1] == 0:
            er.append(i)
    for i in er:
        solved.remove(i)
    for i in range(len(solved)):
        solved[i].pop()
        solved[i] = str(solved[i][0])
    # await message.channel.send(solved)

async def GetProblems(inp):
    global nullresponse
    # await message.channel.send(inp)
    re = requests.get(inp)
    soup = BeautifulSoup(re.text,"html.parser")
    soup = soup.find(class_='table table-condensed')
    if soup == None:
        return 'fail'
    soup = soup.find_all('a')
    # soup = soup.find_all(class_ = '')
    re = []
    for i in soup:
        k = i.attrs['class'][0]
        if k == 'text-success':
            re.append([i.text,1])
        else:
            re.append([i.text,0])
    # for i in soup:
    #     await message.channel.send(i.__class__)
    return re
async def FindDiff(params,message):
    global user
    user1 = "https://tioj.ck.tp.edu.tw/users/"
    user2 = 'https://tioj.ck.tp.edu.tw/users/'
    user2 = user2+user
    user1 = user1+params[0]
    arr1 = GetProblems(user1)
    arr2 = GetProblems(user2)
    if type(arr1) == type('hi') or type(arr2) == type('hi'):
        await message.channel.send('failed')
        return
    anob = []
    bnoa = []
    for i in range(len(arr1)):
        if arr1[i][1] == 1 and arr2[i][1] == 0:
            anob.append(arr1[i][0])
        elif(arr1[i][1] == 0 and arr2[i][1] == 1):
            bnoa.append(arr1[i][0])
    await message.channel.send("solved by rival:\n")
    for i in anob:
        await message.channel.send(i,end = ',')
    await message.channel.send()
async def FindProblems(message):
    arr = []
    for i in range(1,14):
        await message.channel.send('processing:'+str(i)+'/13')
        now_page = 'https://tioj.ck.tp.edu.tw/problems?page='+str(i)
        re = requests.get(now_page)
        soup = BeautifulSoup(re.text,'html.parser')
        soup = soup.find(class_ = 'table-hover')
        soup = soup.find('tbody').find_all('tr')
        for i in soup:
            tmp = i.find_all('td')
            # await message.channel.send(tmp[1].text,tmp[2].text,tmp[3],tmp[4].text)
            if tmp[1].text in solved:
                continue
            else:
                arr.append([tmp[1].text,tmp[2].text,float(tmp[4].find('a').text.split('/')[0])])
            arr[-1][0] = arr[-1][0].replace('\n',' ')
            arr[-1][1] = arr[-1][1].replace('\n',' ')
            # await message.channel.send(tmp[4].text.split(' '))
        # time.sleep(0.05)
    arr = sorted(arr,key=lambda x:x[-1])
    for i in arr:
        await message.channel.send(i)
        await message.channel.send(' ')
async def Solve(s,message):
    global user,solved,topcoders
    if len(s) == 0:
        await message.channel.send('error\n')
    elif s[0] == 'd':
        if len(s)<2:
            await message.channel.send('error\n')
            return
        FindDiff(s[1:],message)
    elif s[0] == 'h':
        await message.channel.send('functions:\nd:compare with another user\np:await message.channel.send unsolved problems with specific order accending\nc:change user\ns:show solved ids\nt:show topcoders by accending order')
    elif s[0] == 'p':
        await FindProblems(message)
    elif s[0] == 'c':
        user = s[1]
        solved = GetProblems("https://tioj.ck.tp.edu.tw/users/"+user)
        if type(solved) == type('hi'):
            await message.channel.send('invalid user id')
            return
            solved = GetProblems("https://tioj.ck.tp.edu.tw/users/"+user)
        er = []
        for i in solved:
            if i[1] == 0:
                er.append(i)
        for i in er:
            solved.remove(i)
        for i in range(len(solved)):
            solved[i].pop()
            solved[i] = str(solved[i][0])
    elif s[0] == 's':
        for i in solved:
            await message.channel.send(i)
    elif s[0] == 't':
        for person,cnt in topcoders:
            await message.channel.send(str(person)+":",cnt)
