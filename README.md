HuggingFace Image Router

OpenAI-compatible router for HuggingFace text-to-image models.

Supports models such as:

- FLUX
- Stable Diffusion
- SDXL
- Kandinsky
- Playground

---

Features

- Multiple HF API keys
- Round-robin key rotation
- Style presets
- Negative prompts
- Width & height control
- Multi-image generation
- Local image storage
- Model listing

---

Installation

cd /home/aman
mkdir -p routers
cd routers

curl -O https://raw.githubusercontent.com/technicalboy2023/hf-image-router/main/install-router.sh
chmod +x install-router.sh

bash install-router.sh hf-image-router 9100

---

Configure API Keys

nano /home/aman/routers/hf-image-router/.env

Example:

HF_KEY_1=hf_xxxxx
HF_KEY_2=hf_xxxxx
HF_KEY_3=

Restart router:

sudo systemctl restart hf-image-router

---

Generate Image

POST /v1/images/generations

Example:

curl http://localhost:9100/v1/images/generations \
-H "Content-Type: application/json" \
-d '{
"model":"black-forest-labs/FLUX.1-schnell",
"prompt":"cyberpunk city neon lights",
"n":1
}'

---

View Image

GET /images/{filename}

Example:

http://localhost:9100/images/123456.png

---

Health Check

GET /health

---

License

MIT
