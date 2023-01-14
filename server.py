from aiohttp import web  
from pymongo import MongoClient
from functools import partial 
from pytube import YouTube
import aiohttp
import aiohttp_jinja2
import jinja2
import random
import json
import os , sys ,re , time
import wikipedia
import requests
# local imports 
import regularExpressions




    


async def download_yt_video(request):
    if len(os.listdir("./downloads")) > 10:
        for f in os.listdir("./downloads"):
            os.remove(os.path.join("./downloads/" , f))
    parameters = await request.post()
    # getting url from parameters 
    video_url = parameters["url"]
    # getting itag from parameters 
    mime_type_or_itag = parameters["itag"].split("$" ,1)
    mime_type = mime_type_or_itag[0]
    itag = int(mime_type_or_itag[1])
    def change_name(mime_type,stream,path):
        name = stream.default_filename
        if mime_type == "audio/webm":
            name_without_ext = os.path.splitext(f"./downloads/{name}")[0]
            new_name = name_without_ext + '.mp3'
            try:
                os.rename(f"./downloads/{name}",f"./downloads/{new_name}" )
                name = new_name
            except:
                pass
    yt = YouTube(video_url,on_complete_callback=partial(change_name,mime_type))
    stream = yt.streams.get_by_itag(itag)
    stream.download('./downloads')
    name = stream.default_filename
    if mime_type == "audio/webm":
            name_without_ext = os.path.splitext(f"./downloads/{name}")[0]
            new_name = name_without_ext + '.mp3'
            try:
                os.rename(f"./downloads/{name}",f"./downloads/{new_name}" )
                name = new_name
            except:
                pass
    
    # making stream download through client brouwser
    # data = request.post()
    f = open(f"./downloads/{name}" , "rb")

    headers={
            "Content-Type": mime_type,
        
        }
    return web.Response(body = f, headers = headers)
    
    
    
        

async def downloadyt(request):
    # getting youtube video url from requests
    video_url = request.query["urlyt"]
    yt = YouTube(video_url)
    # getting a list of streams available 
    # making a empty array to store available itags 
    itag_resolution_list = {}
    # print(streams_list)
    for stream in yt.streams.filter( progressive=True).all():
        itag_resolution_list[stream.resolution] = f"{stream.mime_type}${stream.itag}"
    for stream in yt.streams.filter(only_audio=True):
        itag_resolution_list[stream.resolution] = f"{stream.mime_type}${stream.itag}"
        

    context = {
        "thumbnail" : yt.thumbnail_url ,
        "title" : yt.title,
        "itags_resolution_list" : itag_resolution_list,
        "video_url" : video_url,
        
    } 
    return aiohttp_jinja2.render_template('index.jinja2', request, context)
def getYtLinks(msg,response):
    urls = re.findall(regularExpressions.all_link_regex,msg) 
    if len(urls) != 0:
        for link in urls:
            if "youtu.be" in link or "youtube.com" in link:
                yt = YouTube(link)
                response["replies"].append({"message": f"Videos links found in message \nTitle : {yt.title}\nDownload to gallery: {credentials.botlink}?urlyt={link}"})
            else:
                continue
        return True
    else:
        return False

def stickerBan(msg,abuser_name,response):
    if(bool(regularExpressions.sticker_regex.match(msg))):
        response["replies"].append({"message":f"Stickers are not allowed.\nDear {abuser_name} you will get removed by admin if you continue sending more stickers"})
        return True
    else:
        return False
def searchInWiki(msg,searcher_name,response):
    if("wiki" in msg.split(" ")[0]):
        try:
            responce_from_bot = wikipedia.summary(msg)
            response["replies"].append({"message": f" Hey {searcher_name} here is your question summary: \n{responce_from_bot}"})
        except:
            response["replies"].append({"message": f"No result found for {searcher_name} query."})
        return True
    else:
        return False
def help(msg,response):
    if(msg=="help"):
        response['replies'].append({"message":f"1. Send any YouTube video link to get direct download link.\n\n2. Send any topic heading (History,Science,Any acronym,Invention,culture,Politics etc.) to get brief summary:\n\t Message must in the format: \n\t\t\t\t\twiki <your topic> \n\n\n Warning: <,> don't use these signs "})
        return True
    else:
        return False
    
async def chatBot(request):
    # getting  data from notificatioin reader application
    reply_msg = await request.content.read()
    # formating data to get message
    raw_string = reply_msg.decode('utf-8')
    # making raw string to json format
    json_string = json.loads(raw_string)
    # getting query set
    query_set = json_string['query']
    # initlizing requred variables from queryset
    sender = query_set["sender"]
    message = query_set["message"].lower()
    isGroup = query_set["isGroup"]
    groupParticipant = query_set["groupParticipant"]
    # initilizing response dict
    response = {"replies": []}
    #----------------------------------------- main logic -----------------------
    # if msg not is help 
    if(not help(message,response)):
        # these are sepratly for group and personal 
        if(isGroup):
            stickerBan(message,groupParticipant,response)
            searchInWiki(message,groupParticipant,response)
        else:
            if(searchInWiki(message,sender,response)):
                pass
            else:
                response["replies"].append({"message": f"Hello {sender}, I am hard-coded robot and i can only do few tasks that i know. I am not smart enough to do everything that you expect. Type help to get my tasks list "})
        getYtLinks(message,response)
    else:
        pass

    return web.json_response(response)

async def my_web_app():
    app = web.Application()
    aiohttp_jinja2.setup(app, loader = jinja2.FileSystemLoader('./templates'))
    app.router.add_route('POST', "/chatbot", chatBot)
    app.router.add_route('GET', "/downloadyt", downloadyt)
    app.router.add_route('POST', "/download_yt_video", download_yt_video)
    return app



if __name__ == '__main__':
    web.run_app(my_web_app(),port=8000)    
    



   
