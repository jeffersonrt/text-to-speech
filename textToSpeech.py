import os
import random
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from dotenv import dotenv_values
from pydub import AudioSegment

env = dotenv_values(".env")

# Setup Service
authenticator = IAMAuthenticator(env["api_key"])

#New TTS Service
tts = TextToSpeechV1(authenticator=authenticator)

#Set Service URL
tts.set_service_url(env["url"])

# Voices US
voiceEmily = 'en-US_EmilyV3Voice'
voiceAllison = 'en-US_AllisonV3Voice'
voiceHenry = 'en-US_HenryV3Voice'
voiceKevin = 'en-US_KevinV3Voice'
voiceLisa = 'en-US_LisaV3Voice'
voiceMichael = 'en-US_MichaelV3Voice'
voiceOlivia = 'en-US_OliviaV3Voice'

# Voices GB
voiceCharlotte = 'en-GB_CharlotteV3Voice'
voiceJames = 'en-GB_JamesV3Voice'
voiceKate = 'en-GB_KateV3Voice'


voices = [voiceEmily, voiceAllison, voiceHenry, voiceKevin, voiceLisa, voiceMichael, voiceOlivia]

#code
with open('./wordphrases.txt', 'r') as f:
  text = f.readlines()

  for line in text:
    lineElements = line.replace('\n','').partition(' - ')
    word = lineElements[0]
    phrase = lineElements[2]
    voice = random.choice(voices)

    with open('./files/'+word+'.mp3', 'wb') as audio_file:
      res = tts.synthesize(phrase, accept='audio/mp3', voice=voice).get_result()
      audio_file.write(res.content)

print('AUDIO RECORDED 🔈')

# Edit audio :: Add silence before

basepath = 'files/'
duration=500

with os.scandir(basepath) as audio_files:
  for file_mp3 in audio_files:
    if not file_mp3.name.startswith('.') and  file_mp3.is_file():
      phrase = AudioSegment.from_mp3('files/'+file_mp3.name)
      one_sec_segment = AudioSegment.silent(duration=duration)
      final_phrase = one_sec_segment + phrase
      final_phrase.export('edited/'+file_mp3.name, format="mp3")

print('GOOD TO GO 🚀')