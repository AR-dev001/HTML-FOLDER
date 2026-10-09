import random
import sys

if random.randint(1, 100) == 1:
    print("\nUnexpected system anomaly detected.")
    print("Terminating session...")
    sys.exit()
else:
    print("\nAll processes nominal.")
import base64, requests
from config import HF_API_KEY

API_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}
MODELS = [
    "zai-org/GLM-4.5V",
    "Qwen/Qwen2.5-VL-72B-Instruct",
    "Qwen/Qwen2.5-VL-32B-Instruct",
    "google/gemma-3-27b-it",
]

def data_url(b: bytes) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(b).decode("utf-8")

def extract_err(r: requests.Response) -> str:
    try:
        j = r.json()
        return j.get("error", {}).get("message") or str(j)
    except Exception:
        return (r.text or "").strip() or r.reason or "Request failed."

def box(title: str, lines: list[str], icon: str):
    w = max(30, len(title) + 4, *(len(x) for x in lines))
    print("\n" + "┏" + "━" * (w + 2) + "┓")
    print(f"┃ {icon} {title.ljust(w - 2)} ┃")
    print("┣" + "━" * (w + 2) + "┫")
    for x in lines:
        print(f"┃ {x.ljust(w)} ┃")
    print("┗" + "━" * (w + 2) + "┛\n")

def caption_single_image():
    image_source = input("🖼️ Enter image filename (default: test.jpg): ").strip() or "test.jpg"
    try:
        with open(image_source, "rb") as f:
            img = f.read()
    except Exception as e:
        box("File Error", [f"Could not load: {image_source}", f"Reason: {e}"], "❌")
        return

    base = {
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "Give a short caption for this image."},
                {"type": "image_url", "image_url": {"url": data_url(img)}},
            ],
        }],
        "max_tokens": 60,
        "temperature": 0.2,
    }

    last = None
    for model in MODELS:
        payload = dict(base, model=model)
        try:
            r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=120)
        except requests.RequestException as e:
            last = f"Request failed: {e}"
            continue

        if r.status_code != 200:
            last = extract_err(r)
            continue

        try:
            d = r.json()
        except Exception:
            last = "Non-JSON response received from the API."
            continue

        cap = (d.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
        if cap:
            box("Image Caption Generated", [
                f"🖼️ Image  : {image_source}",
                "📝 Caption:",
                f"   {cap}",
            ], "🎉")
            return
        last = "No caption found."

    box("Caption Failed", [f"🖼️ Image  : {image_source}", f"❌ Error : {last or 'Unknown error'}"], "⚠️")

def main():
    caption_single_image()

if __name__ == "__main__":
    main()
