
# coding: utf-8

# In[1]:


from sklearn.feature_extraction.text import CountVectorizer
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config as rasa_config
from rasa_nlu.model import Metadata, Interpreter

import json
import numpy as np
import pandas as pd
import re

from IPython.display import Markdown, display
from IPython.display import clear_output

def printmd(string):
    display(Markdown(string))


# In[2]:


df = pd.read_csv('billboard_2000s.csv',encoding = "ISO-8859-1" )
df.head(5)


# In[3]:

# In[4]:


def clean_text(text):
    
    # convert all text to lower case
    text = text.lower()
    
    # convert contractions back to long form
    text = re.sub("\'s", "s", text)
    text = re.sub("\'ve", "ve ", text)
    text = re.sub("can't", "cannot ", text)
    text = re.sub("n't", "nt ", text)
    text = re.sub("\'m", "m ", text)
    text = re.sub("\'re", "re ", text)
    text = re.sub("\'d", "d ", text)
    text = re.sub("\'ll", "ll ", text)
    text = re.sub("\'", "", text)
    
    # remove non-alphabet and non-numbers
    text = re.sub('\W', ' ', text)

    # remove multi-space
    text = re.sub('\s+', ' ', text)
    
    # remove leading and trailing spaces
    text.strip(' ')
    
    return text


# In[68]:


# Create a vocabulary of unique words from all the song names 
df_song_names_all = df['Song'].map(lambda com : clean_text(com))
vectorizer = CountVectorizer(min_df=1)
vectorizer.fit(df_song_names_all.values)
df_song_string_vectorized = vectorizer.transform(df_song_names_all.values)

replay_or_what = True

while replay_or_what == True:
    
    clear_output()
    a = 0
    while a == 0:
    
        # loading the interpreter 
        interpreter = Interpreter.load('./models/nlu/default/current')

        # trigger for adding training question
        trigger = 0
    
        print('**WELCOME TO BILLBOARDS TOP 100 (2000s EDITION)**\n')
        
        print('ASK A QUESTION ABOUT ARTIST, YEAR, RANKING OR LYRICS GIVEN A SONG NAME.\n')
        
        print('EXAMPLES\n')

        print('ARTIST')
        print('  • QUESTION: who sang kiss kiss?')
        print('  • ANSWER: "chris brown featuring tpain" was the artist of the song "kiss kiss".\n')

        print('YEAR')
        print('  • QUESTION: what year did lollipop come out?')
        print('  • ANSWER: The song "lollipop" came out in "2008"\n')

        print('RANKING')
        print('  • QUESTION: what was the billboard ranking of the song womanizer?')
        print('  • ANSWER: The song "womanizer" ranked "80" in year "2008"\n')

        print('LYRICS')
        print('  • QUESTION: what are the lyrics for what ive done by linkin park?')
        print('  • ANSWER: Here are the lyrics of the song "what ive done" [...in this farewell theres]\n')

        print('--------------------------------------------------------------------------------------------------------------"\n') 

        # Establish user's intent
        b = 0
        while b == 0:
        
            try:
                question = input("Type your question here:\n")
                question = str(question)
                question = clean_text(question)

            except ValueError:
                print("Sorry I do not understand your question. Please ask in a different way or ask another question...\n")

            pred_int_ent = interpreter.parse(question)
            
            print('\n')
            print(f"Detected intent = {pred_int_ent['intent']['name']}")
            
            # if an intent is identified from question
            if pred_int_ent['intent']['name'] != 'Null':
                q_intent = pred_int_ent['intent']['name']  
            
            # if an intent cannot be identified from question, ask user for specific intent
            if pred_int_ent['intent']['name'] == 'Null':
                print("Sorry I do not understand the intent of your question.\n")
                
                trigger +=1
                
                d = 0
                while d == 0:
                
                    try:
                        answer_intent = input('Are you asking about an "artist", "year", "ranking" or "lyrics"? \n')
                        answer_intent = str(answer_intent).lower()
                        
                        if 'artist' in answer_intent:
                            q_intent = 'artist'
                        if 'year' in answer_intent:
                            q_intent = 'year'
                        if 'ranking' in answer_intent:
                            q_intent = 'ranking'
                        if 'lyrics' in answer_intent:
                            q_intent = 'lyrics'                  

                    except ValueError:
                        print("Invalid input. Please try again...\n")

                    if q_intent in ['artist','year','ranking','lyrics']:
                        d+=1
                        
                    else:
                        d=0

            # if an intent identified from question has less than 45% confidence, confirm with user the specific intent
            if pred_int_ent['intent']['confidence'] < 0.45:
                
                print(f'\nIs {q_intent} what you are looking for?\n')
                            
                trigger +=1
                
                f = 0
                while f==0:

                    try:
                        answer_confirm = input("Yes OR No \n")
                        answer_confirm = str(answer_confirm).lower()

                    except ValueError:
                        print("Invalid input. Please try again...\n")

                    if answer_confirm in ['yes','y']:
                        f+=1

                    elif answer_confirm in ['no','n']:
                        f+=2

                    else:
                        print("Invalid input. Please try again...\n")                            
 

                if f == 1:
                    q_intent = pred_int_ent['intent']['name']
                    
                if f == 2:
                        
                    g = 0
                    while g == 0:

                        try:
                            answer_intent = input('Are you asking about an "artist", "year", "ranking" or "lyrics"? \n')
                            answer_intent = str(answer_intent).lower()

                            if 'artist' in answer_intent:
                                q_intent = 'artist'
                            if 'year' in answer_intent:
                                q_intent = 'year'
                            if 'ranking' in answer_intent:
                                q_intent = 'ranking'
                            if 'lyrics' in answer_intent:
                                q_intent = 'lyrics'                  

                        except ValueError:
                            print("Invalid input. Please try again...\n")

                        if q_intent in ['artist','year','ranking','lyrics']:
                            g+=1

                        else:
                            g=0       
            
            b+=1 
            
            #print('\n')
            #print(pred_int_ent)
            #print('\n')
            #print(f'intent = {q_intent}')

        # if an entity cannot be identified from question, ask user for specific entity
        if pred_int_ent['entities'] == []:
            print("Sorry I did not get enough information. \n")

            trigger +=1
            
            h = 0
            while h == 0:

                try:
                    answer_entity = input("What is the name of the song again? \n")
                    answer_entity = str(answer_entity).lower()

                except ValueError:
                    print("Invalid input. Please try again...\n")

                question_string_cleaned = np.array([clean_text(answer_entity)])
                question_string_cleaned_vectorized = vectorizer.transform(question_string_cleaned)

                answer_list = []
                for i in range(len(df.Song)):
                    total = np.sum(df_song_string_vectorized.toarray()[i] * question_string_cleaned_vectorized.toarray())
                    answer_list.append(total)

                df_working = df
                df_working['c_song_name'] = answer_list
                df_working.sort_values(['c_song_name'],ascending=False).head(5)    

                for num in range(5):
                    print('\n')
                    print(f'{num+1}.:')
                    print(df_working.sort_values(['c_song_name'],ascending=False).head(5)['Song'].values[num])                     
                    
                try:
                    answer_entity_2 = input("Is it any of the above? (Type 1 thru 5 to select, or No) \n")
                    answer_entity_2 = int(answer_entity_2)
                    answer_entity_2 = (answer_entity_2)-1

                except ValueError:
                    print("Invalid input. Please try again...\n")                        

                if answer_entity_2 in [0,1,2,3,4]:
                    song_name = df_working.sort_values(['c_song_name'],ascending=False).head(5)['Song'].values[answer_entity_2]
                    h+=1

                else:
                    h=0
        
        # if an entity is identified from question, extract entity (song name) value 
        else:
            q_ent_value = []   

            for i in range(len(pred_int_ent['entities'])):
                
                if pred_int_ent['entities'][i]['entity'] == 'song_name':
                    q_ent_value.append(pred_int_ent['entities'][i]['value']) 

                    question_string_cleaned = np.array([clean_text(q_ent_value[0])])
                    question_string_cleaned_vectorized = vectorizer.transform(question_string_cleaned)

                    answer_list = []
                    for i in range(len(df.Song)):
                        total = np.sum(df_song_string_vectorized.toarray()[i] * question_string_cleaned_vectorized.toarray())
                        answer_list.append(total)

                    df_working = df
                    df_working['c_song_name'] = answer_list
                    df_working.sort_values(['c_song_name'],ascending=False).head(5)    

                    song_name = df_working.sort_values(['c_song_name'],ascending=False).head(1)['Song'].values[0]

        #print(f'song name = {song_name}')        
        
        # Based on established intent and entity value (song name), extract information from database as part of the result
        song_rank = str(df[df.Song == song_name].Rank.values[0])
        song_artist = str(df[df.Song == song_name].Artist.values[0])
        song_year = str(df[df.Song == song_name].Year.values[0])
        song_lyrics = str(df[df.Song == song_name].Lyrics.values[0])

        print('\n')
        print('Answer:')
                            
        if q_intent == 'artist':
            print (f'"{song_artist}" was the artist of the song "{song_name}".')

        if q_intent == 'year':
            print (f'The song "{song_name}" came out in "{song_year}"')

        if q_intent == 'ranking':
            print (f'The song "{song_name}" ranked "{song_rank}" in year "{song_year}"')

        if q_intent == 'lyrics':
            print (f'Here are the lyrics of the song "{song_name}"\n')
            print (song_lyrics)      
           
        print('\n')

        j = 0
        while j == 0:
        
            try:
                answer_correct_result = input("Did we provide you with the correct result? (Enter Yes or No)\n")
                answer_correct_result = str(answer_correct_result)

            except ValueError:
                print("Invalid input. Please try again...\n")

            if answer_correct_result.lower() in ['yes','y']:
                j+=1
            
            elif answer_correct_result.lower() in ['no','n']:
                
                print('Sorry. We will update our training data to improve the results. Please help us here...\n')  
                trigger +=1
                
                d = 0
                while d == 0:
                
                    try:
                        answer_intent = input('Are you asking about an "artist", "year", "ranking" or "lyrics"? \n')
                        answer_intent = str(answer_intent).lower()
                        
                        if 'artist' in answer_intent:
                            q_intent = 'artist'
                        if 'year' in answer_intent:
                            q_intent = 'year'
                        if 'ranking' in answer_intent:
                            q_intent = 'ranking'
                        if 'lyrics' in answer_intent:
                            q_intent = 'lyrics'                  

                    except ValueError:
                        print("Invalid input. Please try again...\n")

                    if q_intent in ['artist','year','ranking','lyrics']:
                        d+=1
                        
                    else:
                        d=0
               
                h = 0
                while h == 0:

                    try:
                        answer_entity = input("What is the name of the song again? \n")
                        answer_entity = str(answer_entity).lower()

                    except ValueError:
                        print("Invalid input. Please try again...\n")

                    question_string_cleaned = np.array([clean_text(answer_entity)])
                    question_string_cleaned_vectorized = vectorizer.transform(question_string_cleaned)

                    answer_list = []
                    for i in range(len(df.Song)):
                        total = np.sum(df_song_string_vectorized.toarray()[i] * question_string_cleaned_vectorized.toarray())
                        answer_list.append(total)

                    df_working = df
                    df_working['c_song_name'] = answer_list
                    df_working.sort_values(['c_song_name'],ascending=False).head(5)    

                    for num in range(5):
                        print('\n')
                        print(f'{num+1}.:')
                        print(df_working.sort_values(['c_song_name'],ascending=False).head(5)['Song'].values[num])                     

                    try:
                        answer_entity_2 = input("Is it any of the above? (Type 1 thru 5 to select, or No) \n")
                        answer_entity_2 = int(answer_entity_2)
                        answer_entity_2 = (answer_entity_2)-1

                    except ValueError:
                        print("Invalid input. Please try again...\n")                        

                    if answer_entity_2 in [0,1,2,3,4]:
                        song_name = df_working.sort_values(['c_song_name'],ascending=False).head(5)['Song'].values[answer_entity_2]
                        h+=1

                    else:
                        h=0
                
                song_rank = str(df[df.Song == song_name].Rank.values[0])
                song_artist = str(df[df.Song == song_name].Artist.values[0])
                song_year = str(df[df.Song == song_name].Year.values[0])
                song_lyrics = str(df[df.Song == song_name].Lyrics.values[0])

                print('\n') 

                if q_intent == 'artist':
                    print (f'"{song_artist}" was the artist of the song "{song_name}".')

                if q_intent == 'year':
                    print (f'The song "{song_name}" came out in "{song_year}"')

                if q_intent == 'ranking':
                    print (f'The song "{song_name}" ranked "{song_rank}" in year "{song_year}"')

                if q_intent == 'lyrics':
                    print (f'Here are the lyrics of the song "{song_name}"\n')
                    print (song_lyrics)

                print('\n')
                
        if trigger > 0:
            
            song_name_tag = '[' + song_name + ']' + '(song_name)'
            question_tag = question.replace(song_name , song_name_tag)
            add_question = '- ' + question_tag + '\n'
            #print(add_question)
            
            
            file_edit = open("nlu.md").read()
            
            for intent in ['artist','year','ranking','lyrics']:
                if intent == q_intent:
                    end_tag = '#end_mark_' + intent + '#'
                    file_edit = file_edit.replace(end_tag, add_question + end_tag)

            file = open("nlu.md", 'w')
            file.write(file_edit)
            file.close()    
        
            # loading the nlu training samples
            training_data = load_data("nlu.md")

            # trainer to educate our pipeline
            trainer = Trainer(rasa_config.load("config.yml"))

            # train the model
            interpreter = trainer.train(training_data)
            
            model_directory = trainer.persist("./models/nlu", fixed_model_name="current")
        
        c = 0
        while c == 0:
        
            try:
                continue_y_n = input("Would you like to ask another question? (Enter Yes or No)\n")
                continue_y_n = str(continue_y_n)

            except ValueError:
                print("INVALID INPUT. PLEASE TRY AGAIN...\n")
            
            if continue_y_n.lower() in ['yes','y']:
                c+=1
                clear_output()
            
            elif continue_y_n.lower() in ['no','n']:
                print('Have a good day. Program Terminate.\n')    
                c+=1
                a+=1        

            else:
                print("INVALID INPUT. PLEASE TRY AGAIN...\n")

        print('\n')
    replay_or_what = False


