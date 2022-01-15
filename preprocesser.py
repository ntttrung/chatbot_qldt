from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata
from unidecode import unidecode
from pyvi import ViUtils
from typing import Any, Dict, List, Text
from rasa.shared.nlu.training_data.message import Message
from rasa.nlu.constants import TOKENS_NAMES
from rasa.core.agent import Agent
import os
import pickle
import re
import nltk
import requests
from nltk.tokenize.treebank import TreebankWordDetokenizer
from rasa.utils.endpoints import EndpointConfig 

class VietnamesePreprocesser(Component):

    name = "VietnamesePreprocesser"
    provides = ["entities"]
    requires = ["message"]

    def __init__(self, component_config=None):
        print("Preloading accent model" )
        #nltk.download('punkt')
        # tai cai model tai day : https://github.com/vapormusic/mfe_models/releases/
        #model_dir = "./fasttext/"
        #with open(os.path.join(model_dir, 'kneserney_1st_ngram_model.pkl'), 'rb') as fin:
        #     self.model_loaded = pickle.load(fin)
         
        super().__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        """Not needed, because the the model is pretrained"""
        pass
        

          
    def process(self, message : Message, **kwargs):
        
            
        def isEnglish(s):
            x = re.search("[ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéTêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ]", s)
            if x:
              return False
            else:
              return True  
        def TelexConvert(s):
         #  x = re.search("[ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéTêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ]", s)
         words = s.split()
         actuary = ["act", "actuary", "actuarial", "science", "as","ielts","ilets","toelf","toefl","microsoft","office","specialists","mos","isfa","lyon","test","cert","certificate"]
         toankt = ["math", "mathematics"]
         dseb = ["data", "ds", "khdl", "cntt", "machine", "learning", "ai", "ml", "dseb","epo2","epo3","analyst"]
         newwords = []
         for word in words:
          tempword = word
          if tempword not in actuary and tempword not in toankt and tempword not in dseb:
            if tempword.find("aw") != -1:
                tempword = tempword.replace("aw", "ă")
            elif tempword.find("aa") != -1:
                tempword = tempword.replace("aa", "â")
            elif tempword.find("dd") != -1:
                tempword = tempword.replace("dd", "đ")
            elif tempword.find("oo") != -1:
                tempword = tempword.replace("oo", "ô")
            elif tempword.find("ow") != -1:
                tempword = tempword.replace("ow", "ơ")
            elif tempword.find("ee") != -1:
                tempword = tempword.replace("ee", "ê")
            elif tempword.find("uw") != -1:
                tempword = tempword.replace("uw", "ư")
            elif tempword.find("w") != -1:
                tempword = tempword.replace("w", "ư")
                
            if tempword.find("tr") == -1 & tempword[1:].find("r") != -1:
                tempword = tempword.replace("r", "")
            elif tempword.find("tr") != -1 & tempword[2:].find("r") != -1:
                tempword = tempword.replace("tr", "zzcazp")
                tempword = tempword.replace("r", "")
                tempword = tempword.replace("zzcazp", "tr")
            elif tempword[1:].find("s") != -1:
                tempword = tempword.replace("s", "")
            elif tempword[1:].find("f") != -1:
                tempword = tempword.replace("f", "")
            elif tempword[2:].find("x") != -1:
                tempword = tempword.replace("x", "")
            elif tempword.find("j") != -1:
                tempword = tempword.replace("j", "")
          newwords.append(tempword)
        #  return unidecode(" ".join(newwords))     
          return newwords
         
        def StopWordRemover(s):
             words = s.split()
             stopwords = ["cung","cũng","chắc","chac","ntn","đc","uh","vậy","vay","thì","nhỉ","thế","ừ","ko","nào","nao", "lam the nao", "làm thế nào", "ê", 'e',"khong", "the", "bạn", "em", "anh", "chị", "hỏi", "Em", "tôi", 'có', 'mình', '?', "ạ","vào trường"]
             newwords = []
             for word in words:
                print(word)
                if word in stopwords:
                   print("gone")
                   newwords.append("")
                else:
                   newwords.append(word)
             return " ".join(newwords)
        def convert_num(s):
            dict = {'0':'không', '1':'một', '2':'hai', '3':'ba',
                    '4': 'bốn', '5':'năm', '6': 'sáu', '7':'bảy',
                    '8': 'tám', '9':'chín'}
            charac = ''
            for i in s:
                if i in dict.keys():
                    i = dict[i]
                charac += i
            return charac
             
        try:
         text_data = ((str(message.get("text"))).lower())

         if message.get("text") != None :
           fillers = ["em muốn hỏi", "thêm thông tin", "thay co cho em hoi","thầy cô cho em hỏi","anh chị cho em hỏi","anh chi cho em hoi", "cho mình hỏi", "cho minh hoi","cho em hỏi","cho em hoi",
                        "em hỏi","page ơi", "tôi muốn hỏi", "tôi muốn tìm hiểu", "toi muon tim hieu", "với ạ", "của trường", "tư vấn giúp em",  "cho em", "ra sao"
                        "giúp mình", "tư vấn giúp mình", "cho hỏi", "xin hỏi", "mình muốn tìm hiểu", "thì sao", "tôi muốn hỏi", "kinh tế quốc dân", "kinh te quoc dan", "trường mình",
                        "trường tư vấn cho em", "cho em hỏi là", "mình có nhu cầu", "ktqd", "chatbot", '2020', '2021', "em muốn tìm hiểu", "muốn tìm hiểu", "bao nhiêu ạ", "có đúng không", "không biết", 'thầy cô']
        #    text_data = convert_num(text_data)
        #    text_data = StopWordRemover((str(message.get("text"))).lower())
           for filler in fillers:
             try:
              text_data = text_data.replace(filler,"")
              pass
             except:
              print("no")           
           text_data = StopWordRemover(text_data) 
        #    if(isEnglish(text_data)):
        #      new_message = TelexConvert(text_data)
        #    else:
        #      new_message = text_data      
        #    new_message = TelexConvert(text_data)      
        #    print("lmao2:" + new_message)
           new_message = text_data
           new_message = " ".join(new_message.split())
           print(new_message)
           message.set("text", new_message)
        except :
         pass
          

    def persist(self, file_name, model_dir):
        """Pass because a pre-trained model is already persisted"""
        pass