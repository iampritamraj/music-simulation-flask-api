# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 21:53:35 2021

@author: Pritam
@contact: pritam.prp49@gmail.com
"""
from flask import Flask, Response,request,jsonify
import pymongo
import requests
import librosa
import datetime
import json
import ast

# TODO: Need to implement put and delete api endpoints

app = Flask(__name__)
# >>>>>>>>>>>>>>>>>> DATABASE CONNECTIVITY >>>>>>>>>>>>>>>>>>>>>
# for mongo atlas connectivity
#client = please add connection string here
# for localhost connectivity
client = pymongo.MongoClient("localhost:27017")
database = client["filedproject"]
collection = database['audiofile']

audio_url = "https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_1MG.mp3"

@app.route('/',methods=['GET'])
def home():
    return "<h1> Hello world<h1>"




@app.route('/upload',methods=['GET','POST'])
def upload():
    # TODO avoide checking string length limit,it can be easily done on frontend
    audio_id = request.args.get('audioId')
    audio_url = request.args.get('audioUrl')
    audio_type = request.args.get('audioType')
    audio_name = request.args.get('audioName')
    podcast_host = request.args.get('host')
    podcast_participants = request.args.get('participants')
    audiobook_narrator = request.args.get('narrator')
    if audio_id and audio_url and audio_type and audio_name: #TODO need to verify unique audio_id
        if audio_type == 'song':
            response = requests.get(audio_url)
            if response.ok:
                with open("sampleAudio.mp3", "wb") as audio: #TODO need to remove and added just for testing purpose of api
                    audio.write(response.content)

                collection.insert_one({
                                        "audioId":int(audio_id),
                                        "audioType":"song",
                                        "audioName":audio_name,
                                        "audioDuration":librosa.get_duration(filename='sampleAudio.mp3'), # in future this params provide by user
                                        "uploadTime":str(datetime.datetime.utcnow()), # in future this params provide by user
                                        "audioData":response.content
                                        
                                    })
                return {
                    "error":False,
                    "message":"data inserted successfully",

                }
            else:
                # TODO # don't need it after audio metadata passed by browser
                return False
        elif audio_type == 'podcast':
            if podcast_host is None:
                return {
                    "error":True,
                    "message":"please provide podcast host name"
                }
            response = requests.get(audio_url)
            if response.ok:
                with open("audio.mp3", "rb") as audio: #TODO need to remove and added just for testing purpose of api
                    audio.write(response.content)

                collection.insert_one({
                                        "audioId": audio_id,
                                        "audioType": "podcast",
                                        "audioName": audio_name,
                                        "host": podcast_host,
                                        "audioDuration": librosa.get_duration(filename='audio.mp3'), # in future this params provide by user
                                        "uploadTime": str(datetime.datetime.utcnow()), # in future this params provide by user
                                        "participants": podcast_participants, # additional and None if participants not present TODO: max 10 members can be added
                                        "audioData": response.content,
                                        
                                        
                                    })
            else:
                # TODO # don't need it after audio metadata passed by browser
                return {
                    "error":True,
                    "message":"Invalid audio url response",
                    "response":response.status_code
                }
        elif audio_type == 'audiobook':
            if audiobook_narrator is None:
                return {
                    "error":True,
                    "message":"please provide audiobook narrator"
                }
            response = requests.get(audio_url)
            if response.ok:
                with open("audio.mp3", "rb") as audio: #TODO need to remove and added just for testing purpose of api
                    audio.write(response.content)

                collection.insert_one({
                                        "audioId": audio_id,
                                        "audioType": "audiobook",
                                        "audioName": audio_name,
                                        "audioDuration": librosa.get_duration(filename='audio.mp3'), # in future this params provide by user
                                        "uploadTime": str(datetime.datetime.utcnow()), # in future this params provide by user
                                        "narrator": audiobook_narrator,
                                        "audioData": response.content
                                        
                                    })
            else:
                # TODO # don't need it after audio metadata passed by browser
                 return {
                    "error":True,
                    "message":"Invalid audio url response",
                    "response":response.status_code
                }
        else:
            return {
            "error":True,
            "message":"invalid audio type",
            "additional info":"currently support only three audio types:song,podcast,audiobook"
            }

    else:
        return {
            "error":True,
            "message":"please try again with  required parameters",
            "mandatory params":{
                "audio_url":"required",
                "audio_id":"required",
                "audio_type":"required",
                "audio_name":"required",
            }
        }







@app.route("/fetchAudio",methods=["GET"])
def get_audio():
    audio_type = request.args.get('audioType')
    audio_id = request.args.get('audioId')
    if audio_type and audio_id:
        data = collection.find_one({"audioId": int(audio_id)}) #TODO: need to add aggregation for audio_type and audio_id(query optimization)
        if data:
            # TODO: should remove audio and just return complete data as json string

            # audio return just for testing purpose

            def generate():
                with open("SampleAudio.mp3", 'wb') as f:
                    f.write(data["audioData"])
                with open("SampleAudio.mp3", "rb") as audio:
                    audio_data = audio.read(1024)
                    while audio_data:
                        yield audio_data
                        audio_data = audio.read(1024)
            return Response(generate(), mimetype="audio/x-wav")
            #return json.dumps(ast.literal_eval(data))
        else:
            return {"error":False,
                "message":"Audio not found for given ID"}

    else:
        return {
            "error":True,
            "message":"please try again with required parameters",
            "mandatory params":{
                "audio_id":"required",
                "audio_type":"required",
            }
        }


if __name__ == '__main__':
    app.run(port= 8090,debug=True)