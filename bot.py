import os
import random
from os import system
import urllib
import json
from json import dumps, load
import argparse
from urllib.request import urlopen
from time import sleep
import threading
import amino as aminofix
Import aminofix
import time
from gtts import gTTS
from uuid import uuid4
client=aminofix.Client()
os.system("clear")
os.system("pip install -U amino.fix")
print("\t\033[1;32m Alexa1.0  \033[1;36m Community Bot \n\n")
email="5elue3gh9p0n@1secmail.net"
password="Techvision"
deviceid="4266538AA0F9A4E7CC44B705E23EAB3951FB63E01E168A62B651A50B24A141C087CD97D320D355385D"
client.login(email=email,password=password)
cid="3"
cidy=3

adm=[]
self=client.socket
def generate_transaction_id(self):
        return str(uuid4())
transaction=generate_transaction_id(self)

admx=["http://aminoapps.com/p/0j106z5,http://aminoapps.com/p/9rkn9p"]

subclient=aminofix.SubClient(comId=cid,profile=client.profile)
msg=""" KISS ME NOW """
print("Alexa 1.0 Ready")
l=[]
lis = ["It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes definitely",
    "You may rely on it",
    "As I see it yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Reply hazy try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful","yes","No" ,"Probably","100%", "Not sure"]

@client.event("on_group_member_join")
def on_group_member_join(data):
	if data.comId==cidy:
		try:
			x=data.message.author.icon
			response=requests.get(f"{x}")
			file=open("sample.png","wb")
			file.write(response.content)
			file.close()
			img=open("sample.png","rb")
			subclient.send_message(chatId=data.message.chatId,message=f"""
			[c]Welcome @ <${data.message.author.nickname}$>
""",embedId=data.message.author.userId,embedTitle=data.message.author.nickname,embedLink=f"ndc://x{cid}/user-profile/{data.message.author.userId}",embedImage=img,mentionUserIds=[data.message.author.userId])
			print(f"\nwelcomed {data.message.author.nickname} to gc ")
		except Exception as e:
			print(e)
@client.event("on_text_message")
def on_text_message(data):
	if data.comId==cidy:
		ex=data.message.content
		cd=ex.split(' ')
		x=cd[0]
		c=cd[1:]
		adx=[]
		for w in cd:
			adx.append(w)
		print(adx)
		if ex:
			for i in adx:
				if len(i)<=50:
					if i[:23]=="http://aminoapps.com/p/" or i[:23]=="http://aminoapps.com/c/":
						fok=client.get_from_code(i)
						cidx=fok.path[1:fok.path.index("/")]
						if cidx!=cid:
							try:
								subclient.delete_message(chatId=data.message.chatId,messageId=data.message.messageId,asStaff=True)
								s=subclient.get_chat_thread(data.message.chatId).title
								subclient.start_chat(userId=adm,message=f"ndc://x{cid}/user/profile/{data.message.author.userId} was advertisng in {s}")
								
								subclient.send_message(chatId=data.message.chatId,message=f"<${data.message.author.nickname} don't advertise here")
								print("spotted advertiser")
							except Exception as e:
								print(e)
			if x.lower()=="?info" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message="[ci]Hey there i m a communtiy Bot and my name is alexa , Kwel's bot                            admin link : http://aminoapps.com/p/9rkn9p 👈 for contact ")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="!join":
				if c==[]:
					try:
						subclient.send_message(chatId=data.message.chatId,message=f"{data.message.author.nickname}, you have to paste the link after join")
					except:
						pass
				else:
					try:
						for i in c:
							try:
								d=client.get_from_code(i).objectId
								subclient.join_chat(chatId=d)
								subclient.send_message(chatId=data.message.chatId,message="Joined chatroom !!")
							except Exception as e:
								print(e)
						print(f"Info requested by {data.message.author.nickname}")
					except Exception as e:
						print(e)
			if x.lower()=="?vc" and c==[]:
				try:
					subclient.invite_to_vc(userId=data.message.author.userId,chatId=data.message.chatId)
					print(f"Invited {data.message.author.nickname} to vc")
				except Exception as e:
					print(e)
					subclient.send_message(chatId=data.message.chatId,message=f"[ic]I dont have co/host/host/staff id to invite u to vc, <$@{data.message.author.nickname}$>")
			if x.lower()=="?startvc" and c==[]:
				if x.lower() not in l:
					try:
						subclient.send_message(chatId=data.message.chatId,message="Starting VC in 5 seconds")
						time.sleep(2)
						client.start_vc(comId=cid,chatId=data.message.chatId,joinType=1)
						#subclient.send_message(chatId=data.message.chatId,message=f"Vc started")
						print(f"VC started")
					except Exception as e:
						print(e)
						try:
							subclient.send_message(chatId=data.message.chatId,message=f"[ic]I dont have co/host/host id to run that command, <${data.message.author.nickname}$>",mentionUserIds=[data.message.author.userId])
						except:
							pass
				else:
					try:
						subclient.send_message(chatId=data.message.chatId,message=f"Start command is locked <${data.message.author.nickname}$> !!",mentionUserIds=[data.message.author.userId])
					except:
						pass
			if x.lower()=="?endlive" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message="Ending VC in 5 seconds")
					time.sleep(5)
					client.end_vc(comId=cid,chatId=data.message.chatId,joinType=2)
				except Exception as e:
					print(e)
					subclient.send_message(chatId=data.message.chatId,message=f"[ic]I dont have co/host/host/staff id to run that command, <${data.message.author.nickname}$>",mentionUserIds=[data.message.author.userId])
			if x.lower()=="?onlinemem" and c==[]:
				if x.lower() not in l:
					try:
						o=""
						q=subclient.get_online_users(start=0,size=2000)
						for uid in q.profile.nickname:
							o=o+uid+"\n"
						subclient.send_message(chatId=data.message.chatId,message=f"""[c]Online Members
[c]𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁
[c]{o}
[c]𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁""")
						print("done")
					except Exception as e:
						print(e)
				else:
					try:
						subclient.send_message(chatId=data.message.chatId,message="Members command is locked")
					except:
						pass

			if x.lower()=="?check" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message="""                                                                                                                                                                                    
╔     I'M ONLINE     ╝                                                                                                                                                                                       """)
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="?qa":
				try:
					subclient.send_message(chatId=data.message.chatId,message=str(random.choice(lis)),replyTo=data.message.messageId)
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="?say":
				if x.lower() not in l:
					if c==[]:
						try:
							subclient.send_message(chatId=data.message.chatId,message=f"{data.message.author.nickname}, i can't talk unless you write something after say !")
						except:
							pass
					else:
						try:
							t=''
							lx='en'
							for i in c:
								t=t+i
							out=gTTS(text=t,lang=lx,tld='co.in',slow=False)
							out.save("soundfx.mp3")
							with open("soundfx.mp3","rb") as f:
								subclient.send_message(chatId=data.message.chatId,file=f,fileType="audio")
							f.close()
							print(f"Info requested by {data.message.author.nickname}")
						except Exception as e:
							print(e)
				else:
					try:
						subclient.send_message(chatId=data.message.chatId,message="say command is locked")
					except:
						pass
			if x.lower()=="?love":
				try:
					for i in c:
						msg = i + " null null "
						msg = msg.split(" ")
						msg[2] = msg[1]
						msg[1] = msg[0]		
						
						subclient.send_message(chatId=data.message.chatId,message=f"""
						            [c]-----------------
[c]Love Match ❤️  {random.randint(0,100)}%
[c]---------------
""")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="?dance" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message="""
 (_＼ヽ
  　 ＼＼ .Λ＿Λ
      ＼(　ˇωˇ)　
　        >　⌒ヽ
     　　　/ 　 へ＼
　　      /　　/　＼＼
          ﾚ　ノ　　 ヽ_つ
          /　/
       /　/|
      (　(ヽ
 　     |　|、＼
       | 丿 ＼ ⌒)
        | |　　) /
      `ノ ) 　 Lﾉ
    (_／""")
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
			if x.lower()=="?help" and c==[]:
				try:
					subclient.send_message(chatId=data.message.chatId,message=f"[cb] ?check       - ?startvc         - ?endlive            - ?say               - ?love            - ?dance           - ?qa            - ?info            <${data.message.author.nickname}$> !!",mentionUserIds=[data.message.author.userId])
					print(f"Info requested by {data.message.author.nickname}")
				except Exception as e:
					print(e)
def run_amino_socket():
    j=0
    while True:
        if j>=200:
            print("Updating socket.......")
            client.close()
            client.start()
            print("Socket updated")
            j=0
        j=j+1
        time.sleep(30)
run_amino_socket()
