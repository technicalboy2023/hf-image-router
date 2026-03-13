from fastapi import FastAPI
from fastapi.responses import Response
import requests
import os
import time
import random
from dotenv import load_dotenv

app = FastAPI()

# ------------------------
# LOAD ENV
# ------------------------

load_dotenv()

HF_KEYS = [
os.getenv("HF_KEY_1"),
os.getenv("HF_KEY_2"),
os.getenv("HF_KEY_3"),
os.getenv("HF_KEY_4"),
os.getenv("HF_KEY_5"),
os.getenv("HF_KEY_6"),
os.getenv("HF_KEY_7"),
os.getenv("HF_KEY_8"),
os.getenv("HF_KEY_9"),
os.getenv("HF_KEY_10")
]

# remove empty keys
HF_KEYS = [k for k in HF_KEYS if k]

IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

session = requests.Session()

key_index = 0


# ------------------------
# KEY ROTATION
# ------------------------

def get_key():

    global key_index

    key = HF_KEYS[key_index]

    key_index = (key_index + 1) % len(HF_KEYS)

    return key


# ------------------------
# STYLE PRESETS
# ------------------------

STYLE_PRESETS = {

"cinematic":
"cinematic lighting, ultra realistic",

"anime":
"anime style, studio ghibli",

"fantasy":
"fantasy art, magical environment",

"realistic":
"photorealistic, 8k photography"
}


# ------------------------
# IMAGE GENERATION
# ------------------------

def generate_image(model, prompt, negative, width, height):

    url = f"https://router.huggingface.co/hf-inference/models/{model}"

    headers = {
        "Authorization": f"Bearer {get_key()}"
    }

    payload = {

        "inputs": prompt,

        "parameters": {

            "negative_prompt": negative,

            "width": width,

            "height": height

        }

    }

    try:

        r = session.post(url, json=payload, headers=headers, timeout=180)

        if r.status_code == 503:

            time.sleep(8)

            r = session.post(url, json=payload, headers=headers)

        if r.status_code == 200:

            return r.content

    except:

        pass

    return None


# ------------------------
# SAVE IMAGE
# ------------------------

def save_image(data):

    name = f"{int(time.time())}_{random.randint(1000,9999)}.png"

    path = os.path.join(IMAGE_DIR, name)

    with open(path, "wb") as f:

        f.write(data)

    return name


# ------------------------
# IMAGE ENDPOINT
# ------------------------

@app.post("/v1/images/generations")

async def generate(data: dict):

    prompt = data.get("prompt")

    model = data.get("model")

    n = data.get("n", 1)

    width = data.get("width", 1024)

    height = data.get("height", 1024)

    negative = data.get("negative_prompt", "")

    style = data.get("style")

    if style in STYLE_PRESETS:

        prompt = prompt + ", " + STYLE_PRESETS[style]

    if not model:

        model = "black-forest-labs/FLUX.1-schnell"

    results = []

    for _ in range(n):

        img = generate_image(model, prompt, negative, width, height)

        if not img:
            continue

        name = save_image(img)

        results.append({

            "url": f"/images/{name}",

            "model": model

        })

    return {

        "created": int(time.time()),

        "data": results

    }


# ------------------------
# IMAGE SERVE
# ------------------------

@app.get("/images/{img}")

async def serve(img: str):

    path = os.path.join(IMAGE_DIR, img)

    if not os.path.exists(path):

        return {"error": "not found"}

    with open(path, "rb") as f:

        return Response(content=f.read(), media_type="image/png")


# ------------------------
# MODELS LIST
# ------------------------

@app.get("/v1/models")

async def models():

    url = "https://huggingface.co/api/models"

    params = {

        "pipeline_tag": "text-to-image",

        "limit": 1000

    }

    r = session.get(url, params=params)

    data = r.json()

    models = []

    for m in data:

        models.append({

            "id": m["modelId"],

            "object": "model"

        })

    return {

        "object": "list",

        "data": models

    }


# ------------------------
# HEALTH
# ------------------------

@app.get("/health")

async def health():

    return {

        "status": "ok",

        "keys": len(HF_KEYS)

    }
