HuggingFace Image Router

OpenAI-compatible router for HuggingFace text-to-image models.

Supports models like:

- FLUX
- SDXL
- Stable Diffusion
- Custom HF models

---

Features

- Multiple API keys
- Round-robin key rotation
- Style presets
- Negative prompts
- Width / height control
- Multi-image generation
- Local image storage
- Model listing

---

Installation

git clone https://github.com/technicalboy2023/hf-image-router.git
cd hf-image-router

python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn requests python-dotenv

---

Environment Variables

Create ".env":

HF_KEY_1=hf_xxxxx
HF_KEY_2=hf_xxxxx
HF_KEY_3=
HF_KEY_4=

---

Run

uvicorn router:app --host 0.0.0.0 --port 9100

---

Generate Image

POST /v1/images/generations

Example:

{
"model":"black-forest-labs/FLUX.1-schnell",
"prompt":"cyberpunk city neon lights",
"n":1,
"width":1024,
"height":1024
}

---

Get Image

GET /images/{filename}

---

Health

GET /health

---

License

MIT
