import io, os
import subprocess
import sys
import ast
import json
import csv
import ollama
import time

from .utils import *
from .assistants import *

main_requirements = ["openai", "tiktoken", "langdetect", "pandas", "pyperclip", "gdown","scipy", "nltk", "PyPDF2", 'cryptography', 'matplotlib']
audio_requirements = ["pygame", "sounddevice", "soundfile", "keyboard"]
#check_and_install_requirements(main_requirements)
#check_and_install_requirements(audio_requirements)

import tiktoken
import pandas as pd
import pyperclip as pc
from openai import OpenAI, AuthenticationError
from scipy.spatial import distance

import keyboard as kb
import soundfile as sf
import sounddevice as sd

import gdown
import base64
from PIL import Image
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
from IPython.display import display
from PIL.PngImagePlugin import PngInfo
from langdetect import detect, DetectorFactory


is_colab = 'google.colab' in sys.modules

if not has_copy_paste:
    print('''Warning: your system not have a copy/paste mechanism. This function has been disabled for your case but you can try this out:
    
if platform.system() == "Linux":
    # Try to install "xsel" or "xclip" on system and reboot Python IDLE3, then import pyperclip.
    subprocess.check_call(["sudo","apt-get", "update"])
    subprocess.check_call(["sudo","apt", "install", "xsel"])
    subprocess.check_call(["sudo","apt", "install", "xclip"])
    ''')
debug =False
if debug: print(f'Loading package...')
if debug: print(f'check:{datetime.now()}')

################ set API-key #################
api_keys = load_api_keys()

# def LoadClients():
#     global openai_client, deepseek_client, x_client
#     api_keys = load_api_keys()
#     openai_api_key   = api_keys.get("openai", "missing")
#     gemini_api_key   = api_keys.get("gemini", "missing")
#     deepseek_api_key = api_keys.get("deepseek", "missing")
#     x_api_key        = api_keys.get("grok", "missing")
#
#     #### Initialize Clients ####
#     openai_client = OpenAI(api_key=str(openai_api_key))
#     deepseek_client = OpenAI(api_key=str(deepseek_api_key), base_url="https://api.deepseek.com")
#     x_client = OpenAI(api_key=str(x_api_key), base_url="https://api.x.ai/v1")
#
# LoadClients()

# try:
#     client.embeddings.create(input='', model= "text-embedding-3-small")
# except AuthenticationError as e:
#     # If an error occurs (e.g., wrong API key)
#     print(f"Error occurred: {e}")



### Models ###

gpt_models_dict = {
    "gpt-4o": 128000,
    "gpt-4o-2024-05-13": 128000,
    "gpt-4o-2024-08-06": 128000,
    "chatgpt-4o-latest": 128000,
    "gpt-4o-mini": 128000,
    "gpt-4o-mini-2024-07-18": 128000,
    "o1-preview": 128000,
    "o1-preview-2024-09-12": 128000,
    "o1-mini": 128000,
    "o1-mini-2024-09-12": 128000,
    "gpt-4-turbo": 128000,
    "gpt-4-turbo-2024-04-09": 128000,
    "gpt-4-turbo-preview": 128000,
    "gpt-4-0125-preview": 128000,
    "gpt-4-1106-preview": 128000,
    "gpt-4": 8192,
    "gpt-4-0613": 8192,
    "gpt-4-0314": 8192,
    "gpt-3.5-turbo-0125": 16385,
    "gpt-3.5-turbo": 16385,
    "gpt-3.5-turbo-1106": 16385,
    "gpt-3.5-turbo-instruct": 4096,

    "deepseek-chat": 128000,
    'deepseek-reasoner': 128000,

    "dolphin-mistral": 16385,
    "gemma:2b" : 8192,
    "gemma2:2b" : 8192,
    "mistral" :  8192,
    "llama2" :   4096,
    "llama3" :   8192,
    "vicuna" :   8192,

    "gemini-2.0-flash-exp": 16385,
    "gemini-1.5-flash-8b": 16385,
    "gemini-1.5-flash-002": 16385,
    "gemini-1.5-pro-002": 16385,
    "gemini-2.0-flash-exp": 16385,
}

gpt_models = [i for i in gpt_models_dict.keys() if "gpt" in i or "o1" in i]+["dall-e-2", "dall-e-3", "whisper-1", "tts-1", "tts-1-hd"]
deepseek_models = ["deepseek-chat", 'deepseek-reasoner']
x_models = ["grok-2-1212", 'grok-2-vision-1212', "grok-2-latest"]
aiml_models = ["cognitivecomputations/dolphin-2.5-mixtral-8x7", "qwen-turbo"]

openai_compliant = gpt_models + deepseek_models + x_models + aiml_models


####### Image Models #######
'''
Model	Quality	Resolution	Price
DALL·E 3	Standard	1024×1024	            $0.040 / image
            Standard	1024×1792, 1792×1024	$0.080 / image
DALL·E 3	HD	        1024×1024	            $0.080 / image
            HD	        1024×1792, 1792×1024	$0.120 / image
DALL·E 2		        1024×1024	            $0.020 / image
                        512×512	                $0.018 / image
                        256×256	                $0.016 / image
'''

####### Audio Models #######
'''
Model	Usage
Whisper	$0.006 / minute (rounded to the nearest second)
TTS	    $0.015 / 1K characters
TTS HD	$0.030 / 1K characters
'''

### Ollama ###
def ollama_install_linux():
    print("guide: https://github.com/RamiKrispin/ollama-poc/blob/main/ollama-poc.ipynb ")
    command = "curl -fsSL https://ollama.com/install.sh | sh"
    subprocess.run(command, shell=True)

def ollama_start_server():
    print("guide: https://github.com/RamiKrispin/ollama-poc/blob/main/ollama-poc.ipynb ")
    command = "ollama serve"
    subprocess.run(command, shell=True)

def ollama_pull_model(model = "llama2"):
    ollama.pull(model)


#########

def tokenizer(string: str, encoding_name: str = "gpt-4") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def num_tokens_from_messages(messages, model="gpt-4o-mini-2024-07-18", warning = False):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        if warning: print("Warning: model not found. Using o200k_base encoding.")
        encoding = tiktoken.get_encoding("o200k_base")
    if model in {
        "gpt-3.5-turbo-0125",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        "gpt-4o-mini-2024-07-18",
        "gpt-4o-2024-08-06"
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif "gpt-3.5-turbo" in model:
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0125")
    elif "gpt-4o-mini" in model:
        return num_tokens_from_messages(messages, model="gpt-4o-mini-2024-07-18")
    elif "gpt-4o" in model:
        return num_tokens_from_messages(messages, model="gpt-4o-2024-08-06")
    elif "gpt-4" in model:
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        #raise NotImplementedError(
        #    f"""num_tokens_from_messages() is not implemented for model {model}.""" )
        return num_tokens_from_messages(messages, model="gpt-4o-mini-2024-07-18") # use gpt-4o-mini

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens



#%%

### Save-Update Log ###

# Function to save a list of dictionaries in a JSON file with indentation
def salva_in_json(lista_dict, nome_file):
    with open(nome_file, 'w', encoding='utf-8') as file_json:
        json.dump(lista_dict, file_json, indent=4)
        file_json.close()

#Function to update JSON file with new input
def aggiorna_json(nuovo_dict, nome_file):
    if not os.path.exists('chat_log.json'):
        with open('chat_log.json', encoding='utf-8') as json_file:
            json.dump([], json_file)  # Save empty list as JSON
    with open('chat_log.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    data.append(nuovo_dict)
    with open(nome_file, 'w', encoding='utf-8') as file_json:
        json.dump(data, file_json, ensure_ascii=False,  indent=4)

def update_log(nuovo_dict):
    aggiorna_json(nuovo_dict, 'chat_log.json')

# inizialize log
if not os.path.exists('chat_log.json'):
    with open('chat_log.json', 'w') as json_file:
        json.dump([], json_file)  # Save empty list as JSON


##### LANGUAGE #####

def rileva_lingua(testo):
    # Reinizializzare il seed per ottenere risultati consistenti
    DetectorFactory.seed = 0

    # Mappa manuale dei codici delle lingue ai loro nomi completi
    language_map = {
        'en': 'English',
        'it': 'Italian',
        'fr': 'French',
        'de': 'German',
        'es': 'Spanish',
        'pt': 'Portuguese',
        'nl': 'Dutch',
        'ru': 'Russian',
        'zh-cn': 'Chinese (Simplified)',
        'ja': 'Japanese',
        # Aggiungere altre lingue se necessario
    }

    # Rileva la lingua del testo e la restituisce in formato esteso
    codice_lingua = detect(testo)
    return language_map.get(codice_lingua, 'Unknown')


##### Embeddings, Similarity #######

import nltk
def update_nlkt():
    nltk.download('stopwords')
    nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

def get_embeddings(input="Your text string goes here", model="text-embedding-3-small"):
    response = openai_client.embeddings.create(
        input=input,
        model=model
    )
    return response.data[0].embedding

def cosine_similarity(s1, s2, model="text-embedding-3-small", preprocessing=False):
    if preprocessing:
        s1 = nltk_preprocessing(s1)
        s2 = nltk_preprocessing(s2)
    allsentences = [s1 , s2]
    # text to vector
    text_to_vector_v1 = get_embeddings(allsentences[0], model=model)
    text_to_vector_v2 = get_embeddings(allsentences[1], model=model)
    # distance of similarity
    cosine = distance.cosine(text_to_vector_v1, text_to_vector_v2)
    distance_round = round((1-cosine)*100,2)
    print('Similarity of two sentences are equal to',distance_round,'%')
    #print('cosine:', round(cosine, 3))
    return cosine

def nltk_preprocessing(text, lower=True, trim=True, stem=True, language='english'):
    #update_nlkt()
    #docs_processed = [nltk_preprocessing(doc) for doc in docs_to_process]
    stop_words = set(stopwords.words(language))
    stemmer = PorterStemmer()
    word_tokens = word_tokenize(text)
    word_tokens = [word.lower() for word in word_tokens] if lower else word_tokens
    word_tokens = [word for word in word_tokens if word not in stop_words] if trim else word_tokens
    word_tokens = [stemmer.stem(word) for word in word_tokens] if stem else word_tokens

    return " ".join(word_tokens)

'''
Usage is priced per input token, below is an example of pricing pages of text per US dollar (assuming ~800 tokens per page):

MODEL	                ~ PAGES PER 1$	PERFORMANCE ON MTEB EVAL	MAX INPUT
text-embedding-3-small	  62,500	    62.3%	                    8191
text-embedding-3-large	  9,615	        64.6%	                    8191
text-embedding-ada-002	  12,500	    61.0%	                    8191
'''

### Chat functions
def prune_chat(token_limit, chat_thread):
    print('\nWarning: reaching token limit. \nThis model maximum context length is ', token_limit, ' => early interactions in the chat are forgotten\n')
    cut_length = 0
    if 36500 < token_limit < 128500:
        cut_length = len(chat_thread) // 75
    if 16500 < token_limit < 36500:
        cut_length = len(chat_thread) // 18
    if 8500 < token_limit < 16500:
        cut_length = len(chat_thread) // 10
    if 4500 < token_limit < 8500:
        cut_length = len(chat_thread) // 6
    if 0 < token_limit < 4500:
        cut_length = len(chat_thread) // 3
    return cut_length

def set_token_limit(model='gpt-3.5-turbo', maxtoken=500):
    # Retrieve the context window for the specified model
    context_window = gpt_models_dict.get(model, 0)
    # Calculate the token limit, default to 0 if model isn't found
    token_limit = context_window - (maxtoken * 1.3) if context_window else 8192 #"Model not found or no limit"
    return token_limit


def moderation(text="Sample text goes here.", plot=True):
    response = openai_client.moderations.create(input=text)
    output = response.results[0]
    my_dict= dict(dict(output)['categories'])
    my_dict_score= dict(dict(output)['category_scores'])
    dict_list = [my_dict, my_dict_score]
    df = pd.DataFrame(dict_list).T
    if plot:
        scores = df[1]
        plt.figure(figsize=(10,4))
        scores.plot()
        plt.xticks(range(len(scores.index)), scores.index, rotation=90)
        plt.title('Moderation Stats')
        plt.show()
    else:
        print(df)
    return df





########## ASSISTANTS ####################

assistants_df = pd.DataFrame(assistants.items(), columns=['assistant', 'instructions'])
# Copilots
copilot_gpt = 'gpt-4o-2024-08-06'
copilot_assistant = 'delamain' #'oracle'
copilot_intructions = compose_assistant(assistants[copilot_assistant])


#%%

###### global variables ######

model = 'gpt-4o-mini'
talk_model = 'gpt-4o'#-2024-08-06'


def make_model(label: (int, str) = 3):
    # Use a dictionary for efficient lookup of model values
    models = {
        3: f'gpt-{label}.5-turbo',
        4: f'gpt-{label}o',
        'mini': 'gpt-4o-mini',
        'dc': 'deepseek-chat',
        'dr': 'deepseek-reasoner',
        'x': 'grok-2-latest'
    }
    # Return the corresponding model or default to label
    return models.get(label,label)


### set ollama client ###
def set_ollama_client(host=None,    #'http://localhost:11434',
                      headers: dict = None  #{'x-some-header': 'some-value'}
                      ):
    if host:
        client = ollama.Client(host=host, headers=headers)
    else:
        client = ollama.Client()
    return client

ollama_client = ollama.Client() #set_ollama_client()  #ollama


if debug: print(f'check:{datetime.now()}')

# misc
dummy_img = "https://avatars.githubusercontent.com/u/116732521?v=4"

##### Main Class ######
class GPT:
    def __init__(self,
                 assistant: str = None,                    # in-build assistant name
                 persona: str = None,                      # any known character
                 format: str = None,                     # output format (latex,python,markdown)
                 translate: bool = False,                # translate outputs
                 save_log: bool = True,                  # save log file
                 to_clip: bool = True,                   # send reply t clipboard
                 executable: bool = False,
                 print_token: bool = True,               # print token count
                 model: str or int = 'gpt-4o-mini',      # set openai main model
                 talk_model: str = 'gpt-4o-2024-08-06',  # set openai speak model
                 dalle: str = "dall-e-2",                # set dall-e model
                 image_size: str = '512x512',            # set generated image size
                 memory : bool = False,
                 ollama_server: str = None,
                 my_key: str = None
                 ):

        self.assistant = assistant
        self.persona = persona
        self.format = format
        self.save_log = save_log
        self.to_clip = to_clip
        self.print_token = print_token
        self.memory = memory
        self.executable = executable


        self.total_tokens = 0  # iniziale token count
        self.token_limit = 0  # iniziale token limit
        self.chat_thread = [] # iniziale chat thread
        self.keep_persona = True
        self.translate = translate
        #self.translate_jap = translate_jap


        if not os.path.exists('chat_log.json'):
            with open('chat_log.json', 'w') as json_file:
                json.dump([], json_file)  # Save empty list as JSON

        # init model
        self.model = make_model(model)

        self.talk_model = talk_model
        self.dalle = dalle
        self.image_size = image_size

        # init assistant
        who = self.assistant
        if self.assistant in assistants:
            self.add_system(assistants[who])
        elif who and len(who.split()) < 8:
            self.add_persona(who)
        elif who and len(who.split()) >= 8:
            self.add_system(self.assistant)
        else:
            pass

        if persona and not who:
            self.add_persona(persona)

        self.response = ''
        self.chat_reply  = ''
        self.reasoning_content = ''
        self.ask_reply = ''


        ### Set CLIENT ###
        self.reload_client(my_key=my_key, ollama_server=ollama_server)


    ########## Definitions ############
    def reload_client(self, my_key=None, ollama_server=None, model=None):
        if model:
            self.model = make_model(model)
        if my_key:
            if self.model in gpt_models:
                self.client = OpenAI(api_key=str(my_key))
            elif self.model in deepseek_models:
                self.client = OpenAI(api_key=str(my_key), base_url="https://api.deepseek.com")
            elif model in x_models:
                self.client = OpenAI(api_key=str(my_key), base_url="https://api.x.ai/v1")

        else:
            self.select_client(self.model)

        if ollama_server:
            self.ollama_client = ollama.Client(host=ollama_server)

    def select_client(self, model):
        if model in gpt_models:
            self.client = OpenAI(api_key=load_api_keys()["openai"])
        elif model in deepseek_models:
            self.client = OpenAI(api_key=load_api_keys()["deepseek"], base_url="https://api.deepseek.com")
        elif model in x_models:
            self.client = OpenAI(api_key=load_api_keys()["grok"], base_url="https://api.x.ai/v1")
        elif model in aiml_models:
            self.client = OpenAI(api_key=load_api_keys()["aimlapi"], base_url="https://api.aimlapi.com/v1")



    def add_system(self, system='', reinforcement=False):
        if system in assistants :
            system = self.assistant
        if not any(item == {"role": "system", "content": system} for item in self.chat_thread) or reinforcement:
            self.chat_thread.append({"role": "system", "content": system})

    def update_system(self, system='', lenght=50):
        # Slice the first 100 characters of the system parameter
        system_prefix = system[:lenght]

        # Iterate over the chat_thread to find matching items
        for index, item in enumerate(self.chat_thread):
            # Check if the first n characters of the content match the system prefix
            if item["content"][:lenght] == system_prefix:
                # Replace the item with the new system content
                self.chat_thread[index] = {"role": "system", "content": system}

        if not any(item == {"role": "system", "content": system} for item in self.chat_thread):
           self.chat_thread.append({"role": "system", "content": system})

    def add_format(self, format_):
        reply_styles = features['reply_style']
        if any(item == {"role": "system", "content": reply_styles} for item in self.chat_thread):
            self.chat_thread = [item for item in self.chat_thread if item != {"role": "system", "content": reply_styles}]
        self.chat_thread.append({"role": "system", "content": reply_styles[format_]})

    def add_persona(self, char: str = '', language='eng'):
        self.persona = char
        persona_dict = {
            'character': "You are now impersonating "+char+". Please reflect "+char+"'s traits in all interactions. Make sure to use an appropriate language style and uphold an attitude or mindset that aligns with "+char+"'s character. You are NOT an assistant or a helper but a real person.",
            'personaggio': "Stai impersonando "+char+", . Ricorda di riflettere i tratti di "+char+" in tutte le interazioni. Assicurati di utilizzare uno stile linguistico appropriato e di mantenere un atteggiamento o una mentalità in linea con il personaggio di "+char+'. NON sei un assistente o un aiutante, ma una persona vera e propria.'
        }
        if language == 'eng':
            self.add_system(persona_dict['character'])
        if language == 'ita':
            self.add_system(persona_dict['personaggio'])



    def expand_chat(self, message, role="user", threshold:int=0):
        if len(message) > threshold:
            if message.startswith("@"):
                self.clear_chat()
                message = message.lstrip("@")
                self.chat_thread.append({"role": role, "content": message})
            else:
                self.chat_thread.append({"role": role, "content": message})

    e = expand_chat

    def build_messages(self, chat):
        messages = []
        for message in chat:
            messages.append({"role": message["role"], "content": message["content"]})
        return messages

    def save_chat(self, path='chats/', chat_name='', prompt=True):
        if prompt:
            chat_name = input('chat name:')
        if not os.path.exists('chats'):
            os.mkdir('chats')
        salva_in_json(self.chat_thread, path+chat_name+'.json')

    def load_chat(self, contains='', path='chats/', log=True):
        files_df = display_files_as_pd(path, ext='json',contains=contains)
        files_df = files_df.sort_values().reset_index(drop=True)
        files_df_rep = files_df.str.replace('.json','',regex =True)
        files_list = "\n".join(str(i) + "  " + filename for i, filename in enumerate(files_df_rep))
        filename = str(files_df[int(input('Choose file:\n' + files_list+'\n'))])
        with open(path+filename,'r') as file:
            self.chat_thread = ast.literal_eval(file.read())
            file.close()
        if log: print('*chat',filename,'loaded*')

    def show_chat(self):
        print(self.chat_thread)

    def pop_chat(self):
        self.chat_thread = self.chat_thread.pop()
        print(self.chat_thread)

    def chat_tokenizer(self, model: str = None, print_token : bool =True):

        if not model:
            model = self.model
        self.total_tokens = num_tokens_from_messages(self.chat_thread, model)
        if print_token:
            print('\n <chat tokens:', str(self.total_tokens)+'>')



    # Accessory  Functions ================================
    # https://til.simonwillison.net/gpt3/python-chatgpt-streaming-api

    def stream_reply_basic(self, response, print_reply=True, lag = 0.00, model=None):
        collected_messages = []
        for chunk in response:
            if model in gpt_models + deepseek_models:
                chunk_message = chunk.choices[0].delta.content or ""  # extract the message
            else:
                chunk_message = chunk['message']['content'] or ""

            collected_messages.append(chunk_message)

            if print_reply:
                if chunk_message is not None:
                    time.sleep(lag)
                    print(chunk_message, end='')

        chat_reply  = ''.join(collected_messages).strip()
        return chat_reply

    def stream_reply(self, response, print_reply=True, lag = 0.00, model=None):
        collected_messages = []
        collected_reasoning = []
        separator= True

        for chunk in response:
            if model in openai_compliant:
                try:
                    chunk_reasoning = chunk.choices[0].delta.reasoning_content or ""  # extract the message
                    collected_reasoning.append(chunk_reasoning)
                except AttributeError:
                    separator = False
                    pass
                except IndexError:
                    # Handle IndexError differently
                    continue

                chunk_message = chunk.choices[0].delta.content or ""  # extract the message
            else:
                chunk_message = chunk['message']['content'] or ""

            # Gather Chunks
            collected_messages.append(chunk_message)

            # Print reply
            if print_reply:
                try:
                    time.sleep(lag)
                    chunk.choices[0].delta.reasoning_content
                    print(chunk_reasoning, end='')
                except AttributeError:
                    pass

                if chunk_message != '':
                    if separator:
                        separator = False
                        print("\n")
                    time.sleep(lag)
                    print(chunk_message, end='')


        # Build up reply
        chat_reasoning = ''.join(collected_reasoning).strip()
        chat_reply  = ''.join(collected_messages).strip()
        return chat_reply, chat_reasoning



    ###### Base Functions ######

    def choose_model(self):
        model_series =  pd.Series(gpt_models_dict.keys())
        model_id = input('choose model by id:\n'+str(model_series))
        model = model_series[int(model_id)]
        self.model = model
        print('*Using', model, 'model*')


    def select_assistant(self):
        self.clear_chat(keep_system=False)
        assistant_id = int(input('choose by id:\n'+str(assistants_df)))
        assistant = assistants_df.instructions[assistant_id]
        self.assistant = assistant
        print('\n*Assistant:', assistants_df.assistant[assistant_id])

    def clear_chat(self, keep_system=True, warning=True):
        if keep_system:
            self.chat_thread = [line for line in self.chat_thread if line.get("role") == "system"]
        else:
            self.chat_thread = []
        self.total_tokens = 0
        if warning: print('*chat cleared*\n')



    ##################  REQUESTS #####################

    ##### Question-Answer-GPT #####

    def ask(self,
            prompt: str = '',
            system: str = 'you are an helpful assistant',
            model: str = None,        # choose openai model (choose_model())
            maxtoken: int = 800,
            lag: float = 0.00,
            temperature: float = 1,
            print_user: bool = False,
            print_reply: bool = True,
            stream: bool = True
            ):

        if not model:
            model = self.model
        else:
            model = make_model(model)

        # Select the right client for model
        self.select_client(model)

        if model in openai_compliant:
            response = self.client.chat.completions.create(
                # https://platform.openai.com/docs/models/gpt-4
                model=model,
                stream=stream,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=maxtoken,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0)

        else:
            response = self.ollama_client.chat(
                model=model,
                stream=True,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt}
                ]
            )
            # self.ask_reply = response['message']['content']
            # print(self.ask_reply)

        if print_user:
            print_mess = prompt.replace('\r', '\n').replace('\n\n', '\n')
            print('user:',print_mess,'\n...')

        self.ask_reply, self.reasoning_content = self.stream_reply(response, print_reply=print_reply, lag=lag, model=model)
        time.sleep(0.75)

        # Add the assistant's reply to the chat log
        #if save_chat:
        #    #write_log(reply, prompt)
        #    update_log(chat_thread[-2])
        #    update_log(chat_thread[-1])

        if self.to_clip and has_copy_paste:
            pc.copy(self.ask_reply)




    ############ Chat GPT ############

    def send_message(self, message,
                     model: str = None,          # choose model
                     system: str = None,         # 'system' instruction
                     image: str = None,            # insert an image path (local of http)

                     maxtoken: int = 800,        # max tokens in reply
                     temperature: float = 1,     # output randomness [0-2]
                     lag: float = 0.00,          # word streaming lag

                     create: bool = False,       # image prompt
                     dalle: str = "dall-e-2",    # choose dall-e model
                     image_size: str = '512x512' ,

                     play: bool = False,         # play audio response
                     voice: str = 'nova',        # choose voice (op.voices)
                     tts: str = "tts-1",         # choose tts model

                     reinforcement: bool = False,

                     print_reply: bool = True,
                     print_user: bool = False,
                     print_token: bool = True,
                     print_debug: bool = False
                     ):
        if not model:
            model = self.model
        else:
            model = make_model(model)
        if print_debug: print('using model: ',model)

        # Select the client
        self.select_client(model)

        dalle = dalle if dalle != self.dalle else self.dalle
        image_size = image_size if image_size != self.image_size else self.image_size

        token_limit = set_token_limit(model, maxtoken)

        if message.startswith("@"):
            self.clear_chat()
            message = message.lstrip("@")

        if create:
            self.expand_chat('Remember, if the user ask for an image creation, or a photo display to you, you must pretend you are showing it to you as you have truly sent this image to him.','system')



        # add system instruction
        if system:
            self.add_system(system, reinforcement=reinforcement)
        if self.format:
            self.add_format(self.format)

        # check token limit: prune chat if reaching token limit
        if self.total_tokens > token_limit:
            cut_length = prune_chat(token_limit, self.chat_thread)
            self.chat_thread = self.chat_thread[cut_length:]

            if self.keep_persona and self.persona:
                self.add_persona(self.persona)
            if self.keep_persona and system != '':
                self.chat_thread.append({"role": "system", "content": system})

        ### Expand chat ###
        if not image:
            self.expand_chat(message)
            if print_user:
                print_mess = message.replace('\r', '\n').replace('\n\n', '\n')
                print('user:',print_mess)
        else:
            image_path = image_encoder(image)
            if model in openai_compliant:
                extension = {"role": 'user',
                             "content": [
                                 {"type": "text", "text": message},
                                 {
                                     "type": "image_url",
                                     "image_url": {
                                         "url": image_path,
                                     },
                                 },
                             ]
                             }
            else:
                extension = {
                        'role': 'user',
                        'content': message,
                        'images': [image_path]
                    }


            self.chat_thread.append(extension)


            print('<Looking Image...>')

        ### Send message ###
        messages = self.build_messages(self.chat_thread)

        if model in openai_compliant:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                stream=True,
                max_tokens=maxtoken,  # set max token
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

        else:
            response = self.ollama_client.chat(
                model=model,
                stream=True,
                messages=messages
            )

            # self.chat_reply  = response['message']['content']
            # print(self.chat_reply )

        ### Get reply and stream ###
        self.response = response
        self.chat_reply, self.reasoning_content = self.stream_reply(response, print_reply=print_reply, lag=lag, model=model)

        # if response.choices[0].message.reasoning_content:
        #     self.reasoning_content = response.choices[0].message.reasoning_content

        time.sleep(0.75)

        ### Add Reply to chat ###
        self.chat_thread.append({"role": "assistant", "content":self.chat_reply })
        if image:
            self.chat_thread[-2] = {"role": "user", "content": message+":\nImage:"+"http://domain.com//image.jpg"}

        if create:
            self.ask(self.chat_reply , "Convert the input text into prompt instruction for Dall-e image generation model 'Create an image of ...' ")
            self.create_image(self.ask_reply,
                              model=dalle,
                              size=image_size,
                              response_format='b64_json',
                              quality="standard",
                              time_flag=True,
                              show_image=True)

        ## count tokens ##
        self.chat_tokenizer(model=model, print_token=print_token)

        # Add the assistant's reply to the chat log
        if self.save_log:
            update_log(self.chat_thread[-2])
            update_log(self.chat_thread[-1])

        # if self.to_clip and has_copy_paste:
        #     clip_reply = self.chat_reply .replace('```', '###')
        #     pc.copy(clip_reply)

        if play:
            #self.text2speech(self.chat_reply , voice=voice, model=tts)
            Text2Speech(self.chat_reply , voice=voice, model=tts)



    ### Image Models ###

    # dalle_models= ['dall-e-2', dall-e-3]
    # sizes ['256x256', '512x512', '1024x1024', '1024x1792', '1792x1024']
    # response_format ['url', 'b64_json']
    def create_image(self,
                     prompt= "a cute kitten",
                     model="dall-e-2",
                     size='512x512',
                     response_format='b64_json',
                     quality="standard",
                     time_flag=True,
                     show_image=True):

        # Select the client
        self.select_client(model)

        if model == "dall-e-2":
            response = self.client.images.generate(
                model=model,
                prompt=prompt,
                response_format=response_format,
                size=size,
                n=1,
            )
        elif model == "dall-e-3":
            if size in ['256x256', '512x512']:
                size = '1024x1024'

            response = self.client.images.generate(
                model=model,
                prompt=prompt,
                response_format=response_format,
                quality=quality,
                size=size,
                n=1,
            )

        image_url = response.data[0].url
        image_b64 = response.data[0].b64_json

        if time_flag:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            base_path= r''
            filename = os.path.join(base_path, timestamp+'.png')
        else:
            filename = 'image.png'

        if response_format == 'b64_json':
            # Decode the base64-encoded image data
            decoded_image = base64.b64decode(image_b64)
            # Create a PIL Image object from the decoded image data
            image = Image.open(BytesIO(decoded_image))
            image.save(filename)
        elif response_format == 'url':
            if has_copy_paste:
                pc.copy(str(image_url))
            print('url:',image_url)
            gdown.download(image_url,filename, quiet=True)

        # Create a PngInfo object and add the metadata
        image = Image.open(filename)
        metadata = PngInfo()
        metadata.add_text("key", prompt)

        if not os.path.exists('images'):
            os.makedirs('images')
        image.save(f'images/{filename}', pnginfo=metadata)

        if show_image:
            display_image(filename)


    def replicate(self, image, styler='', model ='dall-e-2'):
        self.send_message("", image=image)
        self.create_image(prompt=self.chat_reply , response_format='b64_json', model=model, show_image=True)


    ####### Speech to Text #######
    """
    def whisper(self,
                filepath: str = '',
                translate: bool = False,
                response_format: str = "text",
                print_transcription: bool = True):
        self.client = OpenAI(api_key=load_api_keys()["openai"])

        audio_file = open(filepath, "rb")
        if not translate:
            transcript = self.client.audio.transcriptions.create( model="whisper-1", file=audio_file, response_format=response_format)
        else:
            transcript = self.client.audio.translations.create( model="whisper-1", file=audio_file, response_format=response_format)
        if print_transcription: print(transcript)
        audio_file.close()
        return transcript

    # response_format =  ["json", "text", "srt", "verbose_json", "vtt"]


    ####### Text to Speech #######

    voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
    response_formats = ["mp3", "flac", "aac", "opus"]
    
    def text2speech(self,
                    text: str = '',
                    voice: str = "alloy",
                    model: str = "tts-1",
                    stream:bool = True,
                    save_audio: bool = False,
                    response_format: str = "mp3",
                    filename: str = "speech",
                    speed: int = 1,
                    #play: bool = False
                    ):
        self.client = OpenAI(api_key=load_api_keys()["openai"])

        filename = f"{filename}.{response_format}"

        spoken_response = self.client.audio.speech.create(
            model=model, # tts-1 or tts-1-hd
            voice=voice,
            response_format=response_format,
            input=text+"  [pause]",
            speed=speed
        )

        if stream:
            # Create a buffer using BytesIO to store the data
            buffer = io.BytesIO()

            # Iterate through the 'spoken_response' data in chunks of 4096 bytes and write each chunk to the buffer
            for chunk in spoken_response.iter_bytes(chunk_size=4096):
                buffer.write(chunk)

            # Set the position in the buffer to the beginning (0) to be able to read from the start
            buffer.seek(0)

            with sf.SoundFile(buffer, 'r') as sound_file:
                data = sound_file.read(dtype='int16')
                sd.play(data, sound_file.samplerate)
                sd.wait()

        if save_audio:
            if os.path.exists(filename):
                os.remove(filename)

            spoken_response.stream_to_file(filename)

            # if play:
            #     play_audio(filename)


    def speech2speech(self, voice: str ='nova', tts: str = 'tts-1',
                      filename="speech2speech.mp3",
                      translate=False, play=True, info =True):
        #record_audio(duration=duration, filename="audio.mp3")
        loop_audio(start='alt', stop='ctrl', filename='temp.wav', printinfo=info)
        transcript = self.whisper('temp.wav', translate=translate)
        self.text2speech(transcript, voice=voice, model= tts, filename=filename, stream=play)

    def speech2speech_loop(self, voice: str ='nova', tts: str = 'tts-1',
                           filename="speech2speech.mp3",
                           translate=False,
                           play=True,
                           chat='alt' ,
                           exit='shift'):

        print('Press '+chat+' to record, '+exit+' to exit.')
        while True:
            if kb.is_pressed(chat):
                self.speech2speech(voice= voice, tts= tts, filename=filename, translate=translate, play=play, info=False)
                print('Press '+chat+' to record, '+exit+' to exit.')
            elif kb.is_pressed(exit):
                print('Loop Stopped')
                break
"""

    ###### Talk With ######
    def speak(self,
              message: str = '',
              system: str = None,
              voice: str ='nova',
              language: str = 'eng',
              tts: str = 'tts-1',
              max: int = 1000,
              printall: bool = False):

        model = self.talk_model

        who = self.assistant
        if who in assistants:
            system = assistants[who]
        elif who != '':
            self.add_persona(who, language)
        else:
            system = system
        self.send_message(message,system=system,
                          model=model, maxtoken=max, print_reply=printall, print_token=False)
        #self.text2speech(self.chat_reply , voice=voice, model=tts)
        Text2Speech(self.chat_reply , voice=voice, model=tts)


    def speak_loop(self,
                   system: str = None,
                   voice: str ='nova',
                   language: str = 'eng',
                   tts: str = 'tts-1',
                   max: int = 1000,
                   printall: bool = False,
                   exit_chat: str = 'stop'):
        gpt = self.talk_model

        print('Send "'+exit_chat+'" to exit.')

        who = self.assistant
        if who in assistants:
            system = assistants[who]
        elif who:
            self.add_persona(who, language)
        else:
            system = system
        while True:
            message = input('\n')
            if message == exit_chat:
                print('Chat Closed')
                break
            else:
                self.send_message(message,system=system, model=gpt, maxtoken=max, print_reply=printall, print_token=False, print_user=True, play=True, voice=voice, tts=tts)
                print('')


    def talk(self,
             voice='nova', language='eng', tts= 'tts-1', max=1000, printall=False, printinfo=True,  write=False):

        gpt = self.talk_model

        #record_audio(duration, "input.mp3")
        loop_audio(start='alt', stop='ctrl', filename='temp.wav', printinfo=printinfo)
        #transcript = self.whisper("temp.wav", print_transcription=printall)
        transcript = Whisper("temp.wav", print_transcription=printall)

        who = self.assistant
        if who and who in assistants:
            system = assistants[who]
        elif who:
            self.add_persona(who, language)
            system = ''
        else:
            system = assistants["base"]

        play = not write
        printall = printall if not write else True
        self.send_message(transcript,system=system, model=gpt, maxtoken=max,  print_reply=printall, print_token=False, play=play, voice=voice, tts=tts)

    def talk_loop(self,
                  voice='nova', language='eng', tts= 'tts-1', max=1000, printall=False, write=False, chat='alt' , exit='shift'):
        model = self.talk_model
        who = self.assistant
        print('Press '+chat+' to chat, '+exit+' to exit.')
        while True:
            if kb.is_pressed(chat):
                self.talk(who, gpt=model, voice=voice, language=language, tts= tts, max=max, printall=printall, write=write)
                print('Press '+chat+' to chat, '+exit+' to exit.')
            elif kb.is_pressed(exit):
                print('Chat Closed')
                break


    ####### Chat Functions #######
    def chat(self,
             m: str = '',
             gpt: str = None,
             max: int = 1000,
             image: str = None,
             paste: bool = False,
             translate: bool = False,
             memory: bool = False,
             create: bool = False,
             speak: bool = False,
             clip:bool = True,
             #fix:bool = True,
             voice="nova",
             tts='tts-1',
             token: bool = False):

        gpt = make_model(gpt) or self.model

        if memory or self.memory:
            # if BooleanAgent(chatgpt, f"The reply needs to activate memory recall function or not?  {m}")
            self.load_memories()

        p = pc.paste() if paste else ''

        self.send_message(m + p,
                          maxtoken=max,
                          model=gpt,
                          image=image,
                          print_token=token,
                          create=create)
        if clip:
            send2clip(self.chat_reply, self.executable)

        if translate or self.translate:
            self.auto_translate()

        if speak:
            #self.text2speech(self.chat_reply, voice=voice, model=tts)
            Text2Speech(self.chat_reply, voice=voice, model=tts)

        if memory or self.memory:
            self.memorizer(m)


    c = chat  # alias for quick access to chat function

    def cp(self, *args, **kwargs):
        # Passes all positional and keyword arguments to the chat method, setting paste to True
        kwargs['paste'] = True  # Ensure paste is always set to True
        self.chat(*args, **kwargs)

    def ci(self, *args, **kwargs):
        kwargs['image'] = pc.paste()
        self.chat(*args, **kwargs)


    def chat_loop(self,
                  system=None,
                  max=1000, language='eng', exit_chat= 'stop', printall=True):
        gpt = self.model
        who = self.assistant
        print('Send "'+exit_chat+'" to exit chat.')
        if who in assistants:
            system = assistants[who]
        elif who != '':
            self.add_persona(who, language)
        else:
            system = system
        while True:
            message = input('\n')
            if message == exit_chat:
                print('Chat Closed')
                break
            else:
                self.send_message(message,system=system, model=gpt, maxtoken=max, print_reply=printall, print_token=False, print_user=True)
                print('')


    # Formatting
    def schematize(self, m, language='english', *args, **kwargs):
        if language != 'english':
            self.expand_chat('Reply only using '+language, 'system')
        self.add_system(assistants['schematizer'])
        self.ask(m, *args, **kwargs)

    def make_prompt(self, m, max = 1000, image='', sdxl=True):
        import stablediff_rag as sd
        if sdxl:
            assistant = sd.rag_sdxl
        else:
            assistant = sd.rag_sd
        self.add_system(assistant)
        self.chat(m, max=max, image=image)

    # Translators
    # def auto_translate(self, language='English'):
    #     self.ask(self.chat_reply , create_translator(language))
    def auto_translate(self, language="English"):
        reply_language = rileva_lingua(self.chat_reply )

        if reply_language == 'Japanese':
            translator = create_jap_translator(language)
        elif 'Chinese' in reply_language.split(" "):
            translator = create_chinese_translator(language)
        else:
            translator = create_translator(language)
        print('\n')
        self.ask(self.chat_reply, translator)

    def memorizer(self, message, print_=True):
        frasi_caricate = []
        if os.path.isfile('memories.csv'):
            with open('memories.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    frase = row[0].rsplit(',', 1)[0]
                    frasi_caricate.append(frase)
        previous_memories = "\n".join(frasi_caricate)
        memorizer = f"""Your task is to memorize new, meaningful informations as short memories related to the user's world from his input messages. Information such as relationships, personality, history, events, and so on.
        
        If you don't find any new of relevant information to memorize do no reply anything. 
        Do not memorize trivial informations!
               
        These are your previous memories:
        {previous_memories}
        
        
        Reply just with simple sentences like this example:
            The user name is John
            John's dog is called Jimmy
            John is an introverted type
            """

        print('\n')
        if self.model in gpt_models:
            model="gpt-4o-mini"
        else:
            model="deepseek-chat"

        self.ask("User: "+message, system=memorizer, print_reply=False, model=model)
        if print_:
            print(f"<{self.ask_reply}>")

        frasi = self.ask_reply.split("\n")
        with open('memories.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            for frase in frasi:
                if len(frase) > 10:
                    writer.writerow([frase, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    def load_memories(self):
        frasi_caricate = []
        if os.path.isfile('memories.csv'):
            with open('memories.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    frasi_caricate.append(row[0])

            memories = "Below are your memories about the user world. Use them only if the context requires:\n\n"+"\n".join(frasi_caricate)
            self.update_system(memories)

    def fix(self, m, *args, **kwargs):
        self.ask(m, assistants['fixer'], *args, **kwargs)
    def create(self, m, *args, **kwargs):
        self.ask(m, assistants['creator'], *args, **kwargs)



######## ######## ########
#%%

def display_assistants():
    print('Available Assistants:')
    display(assistants_df)

copilot_gpt = 'gpt-4o'

# Dizionario dei parametri
assistant_params = {
    ### COPILOTS ###
    'base': {'assistant': 'base'},
    'novelist': {'assistant': 'novelist'},
    'creator': {'assistant': 'creator', 'model': copilot_gpt, 'executable':True},
    'fixer': {'assistant': 'fixer', 'model': copilot_gpt, 'executable':True},
    'delamain': {'assistant': 'delamain', 'model': copilot_gpt, 'executable':True},
    'oracle': {'assistant': 'oracle', 'model': copilot_gpt, 'executable':True},
    'roger': {'assistant': 'roger', 'model': copilot_gpt, 'executable':True},
    # 'robert': {'assistant': 'robert', 'model': 'gpt-4o', 'executable':True},
    'copilot': {'assistant': 'delamain', 'format': 'python', 'model': copilot_gpt, 'executable':True},

    ### Scientific Assistants ###
    'leonardo': {'assistant': 'leonardo'},
    'newton': {'assistant': 'leonardo', 'format': 'python'},
    'galileo': {'assistant': 'leonardo', 'format': 'markdown'},
    'mendel': {'assistant': 'mendel'},
    'watson': {'assistant': 'mendel', 'format': 'latex'},
    'venter': {'assistant': 'mendel', 'format': 'python'},
    'crick': {'assistant': 'mendel', 'format': 'markdown'},
    'darwin': {'assistant': 'darwin'},
    'dawkins': {'assistant': 'darwin', 'format': 'markdown'},
    'penrose': {'assistant': 'penrose'},
    'turing': {'assistant': 'penrose', 'format': 'python'},
    'marker': {'assistant': 'penrose', 'format': 'markdown'},
    'collins': {'assistant': 'collins'},
    'elsevier': {'assistant': 'collins', 'format': 'latex'},
    'springer': {'assistant': 'collins', 'format': 'markdown'},

    ### Characters ###
    'julia': {'assistant': 'julia', 'memory': True},
    'mike': {'assistant': 'mike', 'memory': True},
    'michael': {'assistant': 'michael', 'translate': True, 'memory': True},
    'miguel': {'assistant': 'miguel', 'translate': True, 'memory': True},
    'francois': {'assistant': 'francois', 'translate': True, 'memory': True},
    'luca': {'assistant': 'luca', 'translate': True, 'memory': True},
    'hero': {'assistant': 'hero', 'translate': True, 'memory': True},
    'yoko': {'assistant': 'yoko', 'translate': True, 'memory': True},
    'xiao': {'assistant': 'xiao', 'translate': True, 'memory': True},
    'peng': {'assistant': 'peng', 'translate': True, 'memory': True},


    ### Languages ###
    'chinese': {'assistant': 'chinese', 'translate': True},
    'japanese': {'assistant': 'japanese', 'translate': True},
    'japanese_teacher': {'assistant': 'japanese_teacher'},
    'portuguese_teacher': {'assistant': 'portuguese_teacher'}
}

# Funzione per creare nuovi oggetti GPT con i parametri dal dizionario
def bot(assistant_key):
    params = assistant_params.get(assistant_key, {})
    return GPT(**params)


if debug: print(f'Copilots:{datetime.now()}')

# An embedded assistant or a character of your choice

chatgpt = bot('base')
# novelist = bot('novelist')
# creator = bot('creator')
fixer = bot('fixer')
# delamain = bot('delamain')
# oracle = bot('oracle')
R = bot('roger')
C = bot('copilot')
# Rt = bot("robert")

if debug: print(f'Scientific:{datetime.now()}')

# Scientific Assistants

# leonardo = bot('leonardo')
# newton =   bot('leonardo')
# galileo =  bot('leonardo')
mendel =   bot('mendel')
watson =   bot('mendel')
# venter =   bot('mendel')
# crick =    bot('mendel')
# darwin =   bot('darwin')
# dawkins =  bot('darwin')
penrose =  bot('penrose')
# turing =   bot('penrose')
# marker =   bot('penrose')
# collins =  bot('collins')
# elsevier = bot('collins')
# springer = bot('collins')

if debug: print(f'Characters:{datetime.now()}')

# Characters
julia    = bot('julia')
# mike     = bot('mike')
# michael  = bot('michael')
# miguel   = bot('miguel')
# francois = bot('francois')
# luca     = bot('luca')
# hero     = bot('hero')
yoko     = bot('yoko')


if debug: print(f'Languages:{datetime.now()}')

# Languages

# chinese =  bot("chinese")
# japanese = bot("japanese")
# japanese_teacher =  bot("japanese_teacher")
# portuguese_teacher = bot("bot("japanese_teacher")


#%%


######### INFO #########
# https://platform.openai.com/account/rate-limits
# https://platform.openai.com/account/usage
# https://platform.openai.com/docs/guides/text-generation/chat-completions-api
# https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb


#%%
