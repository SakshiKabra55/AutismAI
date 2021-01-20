import pandas as pd
import nltk
import sys
import os
import speech_recognition as sr
from os import listdir
from os.path import isfile, join
from googletrans import Translator
from nltk.stem import WordNetLemmatizer
from rake_nltk import Rake
from two_lists_similarity import Calculate_Similarity as cs

#initializing Speech_recognizer
r = sr.Recognizer()
rake = Rake()
#initializing language translator
translator = Translator(service_urls=['translate.google.com'])


def speech_to_text():
    #taking input speech using the microphone
    with sr.Microphone() as source:
        #print("Speak Anything(language: Bengali)")
        audio = r.listen(source)
        try:
            #audio to text conversion
            text = r.recognize_google(audio,language='bn-IN')
            return text
        #if speech is not detected properly
        except:
            text = "Sorry could not recognize what you said!!"

    return text

def text_to_img(text_bn):

    if (text_bn=="Sorry could not recognize what you said!!"):
        sys.exit()

    else:
        keyword_image_data=pd.read_csv('keyword_image_data.csv')
        #bengali-english translator
        text_en = translator.translate(text_bn, dest='en')
        #toeknizing the sentence
        word_tokens = nltk.word_tokenize(text_en.text)
        #Part of Speech Tagging
        tagged_words = nltk.pos_tag(word_tokens)

        #keyword extraction from the text
        rake.extract_keywords_from_text(text_en.text)
        extracted_keywords = rake.get_ranked_phrases()

        #lemmatizing the keywords
        lemmatizer = WordNetLemmatizer()
        lem_key=[]

        for keyword in extracted_keywords:
            lem_key.append(lemmatizer.lemmatize(keyword))

        #Extracting all images name from All_image folder
        master_path = os.getcwd()
        path=master_path+'/static/All_image'
        images = [f for f in listdir(path) if isfile(join(path, f))]

        DIR = master_path+'/fuzzy_output/'
        #List similarity object initializing
        csObj = cs(lem_key,images)

        #List fuzzy_match_output to 'txt_img.csv'
        csObj.fuzzy_match_output(output_csv_name = 'fuzzy_output.csv', output_csv_path = DIR)

        #Getting top matched image name from the 'txt_img.csv' file
        fuzzy_output_data = pd.read_csv(DIR+'fuzzy_output.csv')

        if (fuzzy_output_data['similarity_score'][0] >= 0.85):
            img_name = fuzzy_output_data['similar_ref_list_item'][0]
            # fuzzy_output_sliced = fuzzy_output_data.loc[fuzzy_output_data['similarity_score'] >= 0.85]
            # pd.concat(keyword_image_data,fuzzy_output_sliced.rename(columns={'input_list_item':'Extracted Text',
            #                                                                 'similar_ref_list_item':'Image Name'}),ignore_index=True)
            # keyword_image_data.to_csv('keyword_image_data.csv',index=False)
        else:
            img_name = "No Image"



        return img_name
