# Chatbot-NLP
Python Based NLP chatbot, Can answer any questions using wiki API and has built in facts and features related to dogs!

# Features
- Simple responses based on specific sentences being entered
- Utilizes WeatherAPI for responses about weather in specific locations
- Utilizes WikiAPI to respond to any questions it doesnt have knowledge on
- First Order Logic (FOL) to allow the Chatbot to remember, store & recall from Knowledgebase (KB)
- FOL Proof functions for contradicting - E.g. Can disagree with user if they are certain something else is correct
- Text-To-Speech (TTS)
- Cosine Similarity to know a question even if it is spelt wrong based on a pre-determined Q&A csv file
- Machine Learning to decipher if given image is a dog or not a dog
- Documentation available on this regarding exact features including example conversations

# What I Learned and Improved on
- NLTK for First Order Logic and Cosine Similarity
- Machine Learning using Tensorflow and Keras with GPU for Binary Image Classification
- Understanding Logical Knowledgebases for FOL
- Image Pre-processing with Pillow and Numpy for Machine Learning training and classification
- CSV Parsing
- Use of AIML for use in our XML file to store Questions and Answers
- Cosine Similarity for determining sentence similarity
- Use of Pyttsx3 for TTS of all outputted text if required by user
