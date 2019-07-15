Question-Answer ChatBot for Music: 

(Supervised learning / Classification problem / Intent-Entity Recognition)
Built an interactive environment, where a user can ask questions with specific intents (i.e. asking about artist, year, ranking or lyrics), given a song name. The bot will predict the question's intent (class) and entity (associated song-name), extract the appropriate information from the database and provide the best response. The model was created using RASA NLU and SpaCy, and also featured a feedback loop to update and continuously improve the model's accuracy.

Report: 
"KW_CP2_RPT_Final_061319.pdf"

Model:
"qa_model.py"
(Note that RASA and other dependencies have to be installed in order for the model to function)