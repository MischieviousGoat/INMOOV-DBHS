import requests, json, os, io, re, base64, random, whisper

SERVER = "http://127.0.0.1:5001"
BOTNAME = "InMoov"
USERNAME = "Human"
def split_prompt(text):
    parts = re.split(r'\n[a-zA-Z]', text)
    return parts

def transcribe(fp):
   model = whisper.load_model("base")
   temp_arr = model.transcribe(fp, fp16 = False, language = 'English')
   prompt = temp_arr['text']
   return prompt

def get_prompt(history, text): 
    return {
        "prompt": history + f"{USERNAME}: {text}\n{BOTNAME}:",
        "use_story": False,
        "use_memory": True,
        "use_authors_note": False,
        "use_world_info": False,
        "max_context_length": 1000,
        "max_length": 60,
        "rep_pen": 1.0,
        "rep_pen_range": 2048,
        "rep_pen_slope": 0.7,
        "temperature": 0.8,
        "tfs": 0.97,
        "top_a": 0.8,
        "top_k": 0,
        "top_p": 0.5,
        "typical": 0.19,
        "sampler_order": [6, 0, 1, 3, 4, 2, 5],
        "singleline": False, 
        "sampler_seed": 3452223,  
        "sampler_full_determinism": False,     
        "frmttriminc": False,
        "frmtrmblln": False
    }

def response(history, text): 
    prompt = get_prompt(history, text)
    response = requests.post(f"{SERVER}/api/v1/generate", json=prompt) 
    if response.status_code == 200:
        results = response.json()['results']
        text = results[0]['text'] 
        response_text = split_prompt(text)[0]
        response_text = response_text.replace("  ", " ")        
        response_text = response_text.replace("\n", "")
        #print(response_text)
        return response_text