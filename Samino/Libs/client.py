import os
import base64
import requests
from uuid import UUID
from aminos import Wss
from typing import BinaryIO
from binascii import hexlify
from aminos.src.objects import *
from time import time as timestamp

from .lib import *
from .lib import api
from .lib.objects import *
from .lib import CheckExceptions


class Client:
    def __init__(self, deviceId: str = None, proxies: dict = None, debug: bool = False):
        self.debug = debug
        self.proxies = proxies
        self.uid = None
        headers.deviceId = deviceId
        self.deviceId = headers.Headers().deviceId
        self.headers = headers.Headers().headers
        self.socket: Wss

    def change_lang(self, lang: str = "ar-SY"):
        headers.lang = lang
        self.headers = headers.Headers().headers

    def sid_login(self, sid: str):
        if "sid=" not in sid: return TypeError("SessionId should starts with 'sid='")

        headers.sid = sid
        req = requests.get(api(f"/g/s/account"), headers=self.headers, proxies=self.proxies)
        info = Account(req.json()["account"])

        headers.sid = sid
        headers.uid = info.userId

        self.uid = headers.uid
        self.sid = headers.uid
        self.socket = Wss(self.headers)

        if req.status_code != 200: return info
        else: return CheckExceptions(req.json())

    def login(self, email: str, password: str):
        data = json.dumps({
            "email": email,
            "secret": f"0 {password}",
            "clientType": 100,
            "action": "normal",
            "deviceID": self.deviceId,
            "v": 2,
            "timestamp": int(timestamp() * 1000)
        })
        req = requests.post(api(f"/g/s/auth/login"), headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        else:
            sid = req.json()["sid"]
            self.uid = req.json()["auid"]
            self.sid = f"sid={sid}"
            self.headers["NDCAUTH"] = self.sid
            headers.sid = self.sid
            headers.uid = self.uid
            self.userId = self.uid
            self.headers = headers.Headers().headers
            self.web_headers = headers.Headers().web_headers
            self.socket = Wss(self.headers, self.debug)
            self.socket.launch()
            self.event = self.socket.event
            self.socketClient = self.socket.getClient()
            return Login(req.json())

    def logout(self):
        data = json.dumps({
            "deviceID": self.deviceId,
            "clientType": 100,
            "timestamp": int(timestamp() * 1000)
        })

        req = requests.post(api("/g/s/auth/logout"), headers=headers.Headers(data=data).headers, data=data, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        else:
            self.sid = None
            self.userId = None
            headers.sid = None
            headers.uid = None
            self.socket.close()
            return Json(req.json())

    def check_device(self, deviceId: str):
        head = self.headers
        head["NDCDEVICEID"] = deviceId
        req = requests.post(api(f"/g/s/device"), headers=head)
        if req.json()["api:statuscode"] != 0: return CheckExceptions(req.json())
        return Json(req.json())

    def upload_image(self, image: BinaryIO):
        data = image.read()

        self.headers["content-type"] = "image/jpg"
        self.headers["content-length"] = str(len(data))

        req = requests.post(api(f"/g/s/media/upload"), data=data, headers=self.headers, proxies=self.proxies)
        return req.json()["mediaValue"]

    def send_verify_code(self, email: str):
        data = json.dumps({
            "identity": email,
            "type": 1,
            "deviceID": self.deviceId,
            "timestamp": int(timestamp() * 1000)
        })
        req = requests.post(api(f"/g/s/auth/request-security-validation"), headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def accept_host(self, requestId: str, chatId: str):
        req = requests.post(api(f"/g/s/chat/thread/{chatId}/transfer-organizer/{requestId}/accept"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def verify_account(self, email: str, code: str):
        data = json.dumps({
            "type": 1,
            "identity": email,
            "data": {"code": code},
            "deviceID": self.deviceId
        })
        req = requests.post(api(f"/g/s/auth/activate-email"), headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def restore(self, email: str, password: str):
        data = json.dumps({
            "secret": f"0 {password}",
            "deviceID": self.deviceId,
            "email": email,
            "timestamp": int(timestamp() * 1000)
        })

        req = requests.post(api(f"/g/s/account/delete-request/cancel"), headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def delete_account(self, password: str = None):
        data = json.dumps({
            "deviceID": self.deviceId,
            "secret": f"0 {password}",
            "timestamp": int(timestamp() * 1000)
        })

        req = requests.post(api(f"/g/s/account/delete-request"), headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def get_account_info(self):
        req = requests.get(api(f"/g/s/account"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return AccountInfo(req.json()["account"])

    def claim_coupon(self):
        req = requests.post(api(f"/g/s/coupon/new-user-coupon/claim"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def change_amino_id(self, aminoId: str = None):
        data = json.dumps({"aminoId": aminoId, "timestamp": int(timestamp() * 1000)})
        req = requests.post(api(f"/g/s/account/change-amino-id"), data=data, headers=headers.Headers(data=data).headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def get_my_communitys(self, start: int = 0, size: int = 25):
        req = requests.get(api(f"/g/s/community/joined?v=1&start={start}&size={size}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return CommunityList(req.json()["communityList"]).CommunityList

    def get_chat_threads(self, start: int = 0, size: int = 25):
        req = requests.get(api(f"/g/s/chat/thread?type=joined-me&start={start}&size={size}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return ThreadList(req.json()["threadList"]).ThreadList

    def get_chat_info(self, chatId: str):
        req = requests.get(api(f"/g/s/chat/thread/{chatId}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Thread(req.json()["thread"]).Thread

    def leave_chat(self, chatId: str):
        req = requests.delete(api(f"/g/s/chat/thread/{chatId}/member/{self.uid}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def join_chat(self, chatId: str):
        req = requests.post(api(f"/g/s/chat/thread/{chatId}/member/{self.uid}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def start_chat(self, userId: [str, list], title: str = None, message: str = None, content: str = None, chatType: int = 0):
        if type(userId) is list: userIds = userId
        elif type(userId) is str: userIds = [userId]
        else: raise TypeError("Please put a str or list of userId")

        data = json.dumps({
            "title": title,
            "inviteeUids": userIds,
            "initialMessageContent": message,
            "content": content,
            "type": chatType,
            "timestamp": int(timestamp() * 1000)
        })

        req = requests.post(api(f"/g/s/chat/thread"), headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def get_from_link(self, link: str):
        req = requests.get(api(f"/g/s/link-resolution?q={link}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return FromCode(req.json()["linkInfoV2"]["extensions"]).FromCode

    def edit_profile(self, nickname: str = None, content: str = None, icon: BinaryIO = None, backgroundColor: str = None, backgroundImage: str = None, defaultBubbleId: str = None):
        data = {
            "address": None,
            "latitude": 0,
            "longitude": 0,
            "mediaList": None,
            "eventSource": "UserProfileView",
            "timestamp": int(timestamp() * 1000)
        }

        if nickname: data["nickname"] = nickname
        if icon: data["icon"] = self.upload_image(icon)
        if content: data["content"] = content
        if backgroundColor: data["extensions"]["style"] = {"backgroundColor": backgroundColor}
        if backgroundImage: data["extensions"]["style"] = {"backgroundMediaList": [[100, backgroundImage, None, None, None]]}
        if defaultBubbleId: data["extensions"] = {"defaultBubbleId": defaultBubbleId}

        data = json.dumps(data)
        req = requests.post(api(f"/g/s/user-profile/{self.userId}"), headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        else: return Json(req.json())

    def flag_community(self, comId: str, reason: str, flagType: int):
        data = json.dumps({
            "objectId": comId,
            "objectType": 16,
            "flagType": flagType,
            "message": reason,
            "timestamp": int(timestamp() * 1000)
        })
        req = requests.post(api(f"/x{comId}/s/g-flag"), headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def leave_community(self, comId: str):
        req = requests.post(api(f"/x{comId}/s/community/leave"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def join_community(self, comId: str):
        req = requests.post(api(f"/x{comId}/s/community/join"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def unfollow(self, userId: str):
        req = requests.post(api(f"/g/s/user-profile/{userId}/member/{self.userId}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def follow(self, userId: [str, list]):
        if type(userId) is str: req = requests.post(api(f"/g/s/user-profile/{userId}/member"), headers=self.headers, proxies=self.proxies)
        elif type(userId) is list:
            data = json.dumps({"targetUidList": userId, "timestamp": int(timestamp() * 1000)})
            req = requests.post(api(f"/g/s/user-profile/{self.userId}/joined"), headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        else: raise TypeError("Please put a str or list of userId")
        
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def get_member_following(self, userId: str, start: int = 0, size: int = 25):
        req = requests.get(api(f"/g/s/user-profile/{userId}/joined?start={start}&size={size}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return UserProfileList(req.json()["userProfileList"]).UserProfileList

    def get_member_followers(self, userId: str, start: int = 0, size: int = 25):
        req = requests.get(api(f"/g/s/user-profile/{userId}/member?start={start}&size={size}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return UserProfileList(req.json()["userProfileList"]).UserProfileList

    def get_member_visitors(self, userId: str, start: int = 0, size: int = 25):
        req = requests.get(api(f"/g/s/user-profile/{userId}/visitors?start={start}&size={size}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return VisitorsList(req.json()["visitors"]).VisitorsList

    def get_blocker_users(self, start: int = 0, size: int = 25):
        req = requests.get(api(f"/g/s/block/full-list?start={start}&size={size}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return req.json()["blockerUidList"]

    def get_blocked_users(self, start: int = 0, size: int = 25):
        req = requests.get(api(f"/g/s/block/full-list?start={start}&size={size}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return req.json()["blockedUidList"]

    def get_wall_comments(self, userId: str, sorting: str, start: int = 0, size: int = 25):
        sorting = sorting.lower()

        if sorting == "newest": sorting = "newest"
        elif sorting == "oldest": sorting = "oldest"
        elif sorting == "top": sorting = "vote"
        else: raise TypeError("حط تايب يا حمار")  # Not me typed this its (a7rf)

        req = requests.get(api(f"/g/s/user-profile/{userId}/g-comment?sort={sorting}&start={start}&size={size}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return CommentList(req.json()["commentList"]).CommentList

    def send_message(self, chatId: str, message: str = None, messageType: int = 0, file: BinaryIO = None, fileType: str = None, replyTo: str = None, mentionUserIds: list = None, stickerId: str = None, snippetLink: str = None, ytVideo: str = None, snippetImage: BinaryIO = None, embedId: str = None, embedType: int = None, embedLink: str = None, embedTitle: str = None, embedContent: str = None, embedImage: BinaryIO = None):
        if message is not None and file is None: message = message.replace("[@", "‎‏").replace("@]", "‬‭")

        mentions = []
        if mentionUserIds:
            for mention_uid in mentionUserIds: mentions.append({"uid": mention_uid})

        if embedImage: embedImage = [[100, self.upload_image(embedImage), None]]

        data = {
            "type": messageType,
            "content": message,
            "attachedObject": {
                "objectId": embedId,
                "objectType": embedType,
                "link": embedLink,
                "title": embedTitle,
                "content": embedContent,
                "mediaList": embedImage
            },
            "extensions": {"mentionedArray": mentions},
            "clientRefId": int(timestamp() / 10 % 100000000),
            "timestamp": int(timestamp() * 1000)
        }

        if replyTo: data["replyMessageId"] = replyTo

        if stickerId:
            data["content"] = None
            data["stickerId"] = stickerId
            data["type"] = 3

        if snippetLink and snippetImage:
            data["extensions"]["linkSnippetList"] = [{
                "link": snippetLink,
                "mediaType": 100,
                "mediaUploadValue": base64.b64encode(snippetImage.read()).decode(),
                "mediaUploadValueContentType": "image/png"
            }]

        if ytVideo:
            data["content"] = None
            data["mediaType"] = 103
            data["mediaValue"] = ytVideo

        if file:
            data["content"] = None
            if fileType == "audio":
                data["type"] = 2
                data["mediaType"] = 110

            elif fileType == "image":
                data["mediaType"] = 100
                data["mediaUploadValueContentType"] = "image/jpg"
                data["mediaUhqEnabled"] = False

            elif fileType == "gif":
                data["mediaType"] = 100
                data["mediaUploadValueContentType"] = "image/gif"
                data["mediaUhqEnabled"] = False

            else: raise TypeError("")

            data["mediaUploadValue"] = base64.b64encode(file.read()).decode()
            data["attachedObject"] = None
            data["extensions"] = None

        data = json.dumps(data)
        req = requests.post(api(f"/g/s/chat/thread/{chatId}/message/{message}"), headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def get_community_info(self, comId: str):
        req = requests.get(api(f"/g/s-x{comId}/community/info?withInfluencerList=1&withTopicList=true&influencerListOrderStrategy=fansCount"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Community(req.json()["community"]).Community

    def mark_as_read(self, chatId: str):
        req = requests.post(api(f"/g/s/chat/thread/{chatId}/mark-as-read"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def delete_message(self, messageId: str, chatId: str):
        req = requests.delete(api(f"/g/s/chat/thread/{chatId}/message/{messageId}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def get_chat_messages(self, chatId: str, start: int = 0, size: int = 25):
        req = requests.get(api(f"/g/s/chat/thread/{chatId}/message?v=2&pagingType=t&size={size}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return GetMessages(req.json()["messageList"]).GetMessages

    def get_message_info(self, messageId: str, chatId: str):
        req = requests.get(api(f"/g/s/chat/thread/{chatId}/message/{messageId}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Message(req.json()["message"]).Message

    def tip_coins(self, chatId: str = None, blogId: str = None, coins: int = 0, transactionId: str = None):
        if transactionId is None: transactionId = str(UUID(hexlify(os.urandom(16)).decode("ascii")))
        data = json.dumps({
            "coins": coins,
            "tippingContext": {
                "transactionId": transactionId
            },
            "timestamp": int(timestamp() * 1000)
        })

        if chatId is not None: url = api(f"/g/s/blog/{chatId}/tipping")
        elif blogId is not None: url = api(f"/g/s/blog/{blogId}/tipping")
        else: raise TypeError("please put chat or blog Id")

        req = requests.post(url, headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def reset_password(self, email: str, password: str, code: str, deviceId: str = None):
        if deviceId is None: deviceId = self.deviceId

        data = json.dumps({
            "updateSecret": f"0 {password}",
            "emailValidationContext": {
                "data": {
                    "code": code
                },
                "type": 1,
                "identity": email,
                "level": 2,
                "deviceID": deviceId
            },
            "phoneNumberValidationContext": None,
            "deviceID": deviceId,
            "timestamp": int(timestamp() * 1000)
        })


        req = requests.post(api(f"/g/s/auth/reset-password"), headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def change_password(self, password: str, newPassword: str):
        data = json.dumps({
            "secret": f"0 {password}",
            "updateSecret": f"0 {newPassword}",
            "validationContext": None,
            "deviceID": self.deviceId
        })
        header = headers.Headers(data=data).headers
        header["ndcdeviceid"], header["ndcauth"] = header["NDCDEVICEID"], header["NDCAUTH"]
        req = requests.post(api("/g/s/auth/change-password"), headers=header, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        else: return Json(req.json())


    def get_user_info(self, userId: str):
        req = requests.get(api(f"/g/s/user-profile/{userId}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return UserProfile(req.json()["userProfile"]).UserProfile

    def comment(self, comment: str, userId: str = None, replyTo: str = None):
        data = {
            "content": comment,
            "stickerId": None,
            "type": 0,
            "eventSource": "UserProfileView",
            "timestamp": int(timestamp() * 1000)
        }

        if replyTo: data["respondTo"] = replyTo

        data = json.dumps(data)

        req = requests.post(api(f"/g/s/user-profile/{userId}/g-comment"), headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def delete_comment(self, userId: str = None, commentId: str = None):
        req = requests.delete(api(f"/g/s/user-profile/{userId}/g-comment/{commentId}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def invite_by_host(self, chatId: str, userId: [str, list]):
        data = json.dumps({"uidList": userId, "timestamp": int(timestamp() * 1000)})

        req = requests.post(api(f"/g/s/chat/thread/{chatId}/avchat-members"), headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def kick(self, chatId: str, userId: str, rejoin: bool = True):
        if rejoin: rejoin = 1
        if not rejoin: rejoin = 0

        req = requests.delete(api(f"/g/s/chat/thread/{chatId}/member/{userId}?allowRejoin={rejoin}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def block(self, userId: str):
        req = requests.post(api(f"/g/s/block/{userId}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def unblock(self, userId: str):
        req = requests.delete(api(f"/g/s/block/{userId}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def get_public_chats(self, type: str = "recommended", start: int = 0, size: int = 50):
        req = requests.get(api(f"/g/s/chat/thread?type=public-all&filterType={type}&start={start}&size={size}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        else: return ThreadList(req.json()["threadList"]).ThreadList

    def get_content_modules(self, version: int = 2):
        req = requests.get(api(f"/g/s/home/discover/content-modules?v={version}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def get_banner_ads(self, size: int = 25, pagingType: str = "t"):
        req = requests.get(api(f"/g/s/topic/0/feed/banner-ads?moduleId=711f818f-da0c-4aa7-bfa6-d5b58c1464d0&adUnitId=703798&size={size}&pagingType={pagingType}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return ItemList(req.json()["itemList"]).ItemList

    def get_announcements(self, lang: str = "ar", start: int = 0, size: int = 20):
        req = requests.get(api(f"/g/s/announcement?language={lang}&start={start}&size={size}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return BlogList(req.json()["blogList"]).BlogList

    def get_discover(self, type: str = "discover", category: str = "customized", size: int = 25, pagingType: str = "t"):
        req = requests.get(api(f"/g/s/topic/0/feed/community?type={type}&categoryKey={category}&moduleId=64da14e8-0845-47bf-946a-17403bd6aa17&size={size}&pagingType={pagingType}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return CommunityList(req.json()["communityList"]).CommunityList

    def invite_to_voice_chat(self, userId: str = None, chatId: str = None):
        data = json.dumps({"uid": userId, "timestamp": int(timestamp() * 1000)})
        req = requests.post(api(f"/g/s/chat/thread/{chatId}/vvchat-presenter/invite"), headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def get_wallet_history(self, start: int = 0, size: int = 25):
        req = requests.get(api(f"/g/s/wallet/coin/history?start={start}&size={size}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return WalletHistory(req.json()).WalletHistory

    def get_wallet_info(self):
        req = requests.get(api(f"/g/s/wallet"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return WalletInfo(req.json()["wallet"]).WalletInfo

    def get_all_users(self, type: str = "recent", start: int = 0, size: int = 25):
        if type == "recent": type = "recent"
        elif type == "banned": type = "banned"
        elif type == "featured": type = "featured"
        elif type == "leaders": type = "leaders"
        elif type == "curators": type = "curators"
        else: type = "recent"

        req = requests.get(api(f"/g/s/user-profile?type={type}&start={start}&size={size}"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return UserProfileList(req.json()["userProfileList"]).UserProfileList

    def get_chat_members(self, start: int = 0, size: int = 25, chatId: str = None):
        req = requests.get(api(f"/g/s/chat/thread/{chatId}/member?start={start}&size={size}&type=default&cv=1.2"), headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return UserProfileList(req.json()["memberList"]).UserProfileList

    def get_from_id(self, id: str, comId: str = None, objectType: int = 2):  # never tried
        """
        Get Link from Id.

        **Parameters**
            - **comId** : Id of the community.
            - **objectType** : Object type of the id.
            - **id** : The id.

        **Returns**
            - **Success** : :meth:`Json Object <samino.lib.objects.Json>`

            - **Fail** : :meth:`Exceptions <samino.lib.exceptions>`
        """
        data = json.dumps({
            "objectId": id,
            "targetCode": 1,
            "objectType": objectType,
            "timestamp": int(timestamp() * 1000)
        })

        if comId is None: url = api(f"/g/s/link-resolution")
        elif comId is not None: url = api(f"/g/s-x{comId}/link-resolution")
        else: raise TypeError("please put a comId")

        req = requests.post(url, headers=headers.Headers(data=data).headers, proxies=self.proxies, data=data)
        if req.status_code != 200: return CheckExceptions(req.json())
        return FromCode(req.json()["linkInfoV2"]["extensions"]["linkInfo"]).FromCode

    def chat_settings(self, chatId: str, viewOnly: bool = None, doNotDisturb: bool = None, canInvite: bool = False, canTip: bool = None, pin: bool = None):
        res = []

        if doNotDisturb is not None:
            if doNotDisturb: opt = 2
            if not doNotDisturb: opt = 1
            else: raise TypeError("Do not disturb should be True or False")

            data = json.dumps({"alertOption": opt, "timestamp": int(timestamp() * 1000)})
            req = requests.post(api(f"/g/s/chat/thread/{chatId}/member/{self.uid}/alert"), data=data, headers=headers.Headers(data=data).headers, proxies=self.proxies)
            if req.status_code != 200: return CheckExceptions(req.json())
            res.append(Json(req.json()))

        if viewOnly is not None:
            if viewOnly: viewOnly = "enable"
            if not viewOnly: viewOnly = "disable"
            else: raise TypeError("viewOnly should be True or False")

            req = requests.post(api(f"/g/s/chat/thread/{chatId}/view-only/{viewOnly}"), headers=self.headers, proxies=self.proxies)
            if req.status_code != 200: return CheckExceptions(req.json())
            res.append(Json(req.json()))

        if canInvite is not None:
            if canInvite: canInvite = "enable"
            if not canInvite: canInvite = "disable"
            else: raise TypeError("can invite should be True or False")

            req = requests.post(api(f"/g/s/chat/thread/{chatId}/members-can-invite/{canInvite}"), headers=self.headers, proxies=self.proxies)
            if req.status_code != 200: return CheckExceptions(req.json())
            res.append(Json(req.json()))

        if canTip is not None:
            if canTip: canTip = "enable"
            if not canTip: canTip = "disable"
            else: raise TypeError("can tip should be True or False")

            req = requests.post(api(f"/g/s/chat/thread/{chatId}/tipping-perm-status/{canTip}"), headers=self.headers, proxies=self.proxies)
            if req.status_code != 200: return CheckExceptions(req.json())
            res.append(Json(req.json()))

        if pin is not None:
            if pin: pin = "pin"
            if not pin: pin = "unpin"
            else: raise TypeError("pin should be True or False")

            req = requests.post(api(f"/g/s/chat/thread/{chatId}/{pin}"), headers=self.headers, proxies=self.proxies)
            if req.status_code != 200: return CheckExceptions(req.json())
            res.append(Json(req.json()))

        return res

    def like_comment(self, commentId: str, userId: str = None, blogId: str = None):
        data = json.dumps({"value": 4, "timestamp": int(timestamp() * 1000)})

        if userId: url = api(f"/g/s/user-profile/{userId}/comment/{commentId}/g-vote?cv=1.2&value=1")
        elif blogId: url = api(f"/g/s/blog/{blogId}/comment/{commentId}/g-vote?cv=1.2&value=1")
        else: raise TypeError("Please put blogId or wikiId")

        req = requests.post(url, data=data, headers=headers.Headers(data=data).headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def unlike_comment(self, commentId: str, blogId: str = None, userId: str = None):
        if userId: url = api(f"/g/s/user-profile/{userId}/comment/{commentId}/g-vote?eventSource=UserProfileView")
        elif blogId: url = api(f"/g/s/blog/{blogId}/comment/{commentId}/g-vote?eventSource=PostDetailView")
        else: raise TypeError("Please put blog or user Id")

        req = requests.delete(url, headers=self.headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def register(self, nickname: str, email: str, password: str, deviceId: str = None):
        if deviceId is None: deviceId = self.deviceId

        data = json.dumps({
            "secret": f"0 {password}",
            "deviceID": deviceId,
            "email": email,
            "clientType": 100,
            "nickname": nickname,
            "latitude": 0,
            "longitude": 0,
            "address": None,
            "clientCallbackURL": "narviiapp://relogin",
            "type": 1,
            "identity": email,
            "timestamp": int(timestamp() * 1000)
        })

        req = requests.post(api(f"/g/s/auth/register"), data=data, headers=headers.Headers(data=data).headers, proxies=self.proxies)
        if req.status_code != 200: return CheckExceptions(req.json())
        return Json(req.json())

    def watch_ad(self, uid: str = None):
        data = headers.AdHeaders(uid if uid else self.uid).data
        req = requests.post(tapjoy, json=data, headers=headers.AdHeaders().headers, proxies=self.proxies)
        print(req.status_code)
        if req.status_code != 204: return CheckExceptions(req.status_code)
        else: return Json(req.text)
