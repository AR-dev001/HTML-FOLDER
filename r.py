
from config import HF_API_KEY

import requests
import base64
import os
import re
import io

from PIL import Image
from colorama import init, Fore, Style

init(autoreset=True)

ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

# Updated vision models
# Automatic provider selection is used instead of forcing Novita.

VISION_MODELS = [
    "zai-org/GLM-4.5V:novita",
    "Qwen/Qwen3-VL-30B-A3B-Instruct:novita",
    "Qwen/Qwen2.5-VL-72B-Instruct:featherless-ai",
    "google/gemma-3-27b-it:deepinfra",
]

TEXT_MODELS = [
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen2.5-14B-Instruct",
    "Qwen/Qwen2.5-32B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "meta-llama/Llama-3-8B-Instruct",
]

# ============================
# IMAGE PROCESSING
# ============================

def _data_url(path: str) -> str:
    with Image.open(path) as img:
        img = img.convert("RGB")
        img.thumbnail((640, 640))

        buffer = io.BytesIO()

        img.save(
            buffer,
            format="JPEG",
            quality=55,
            optimize=True
        )

        encoded = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

        return "data:image/jpeg;base64," + encoded


# ============================
# API REQUEST
# ============================

def query_hf_api(payload: dict):
    try:
        response = requests.post(
            ROUTER_URL,
            headers=HEADERS,
            json=payload,
            timeout=120
        )

    except requests.RequestException as error:
        return None, f"Request failed: {error}"

    if response.status_code != 200:
        try:
            data = response.json()
            error = data.get("error", {})

            if isinstance(error, dict):
                message = error.get("message") or str(data)
            else:
                message = str(error)

        except Exception:
            message = response.text.strip() or response.reason

        return None, f"Status {response.status_code}: {message}"

    try:
        return response.json(), None

    except ValueError:
        return None, "The API returned an invalid response."


def _extract_text(data) -> str:
    try:
        message = data["choices"][0]["message"]
        content = message.get("content") or ""

        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):
            parts = []

            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        parts.append(item.get("text", ""))

            return " ".join(parts).strip()

        return ""

    except (KeyError, IndexError, TypeError):
        return ""


def _run_models(
    models,
    messages,
    max_tokens=160,
    temperature=0.2
):
    errors = []

    for model in models:
        print(f"{Fore.CYAN}Trying model: {model}")

        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        data, error = query_hf_api(payload)

        if error:
            print(f"{Fore.RED}{error}")
            errors.append(f"{model}: {error}")

            # No remaining credits will affect every model.
            if "402" in error or "no remaining credits" in error.lower():
                return None, error

            continue

        output = _extract_text(data)

        if output:
            return output, None

        errors.append(f"{model}: Empty response.")

    return None, "\n".join(errors) or "All models failed."


# ============================
# TEXT UTILITIES
# ============================

def _words(text: str):
    return re.findall(r"\S+", (text or "").strip())


def _exact_n_words(text: str, n: int) -> str:
    return " ".join(_words(text)[:n])


def _count_words(text: str) -> int:
    return len(_words(text))


def _clean_output(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"\s+", " ", text)

    text = re.sub(
        r"^(caption|description|summary)\s*:\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    return text.strip()


def _ensure_sentence_end(text: str) -> str:
    text = text.strip()

    if text and text[-1] not in ".!?":
        text += "."

    return text


# ============================
# TEXT GENERATION
# ============================

def generate_text(
    prompt: str,
    max_new_tokens: int = 220
) -> str:
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    output, error = _run_models(
        TEXT_MODELS,
        messages,
        max_tokens=max_new_tokens
    )

    if not output:
        raise Exception(error)

    return _clean_output(output)


def generate_exact_sentence(
    prompt: str,
    n_words: int,
    max_new_tokens: int,
    tries: int = 6
) -> str:
    current_prompt = (
        prompt
        + f"\nWrite exactly {n_words} words."
        + "\nUse one complete sentence."
        + "\nReturn only the sentence, without a title."
    )

    last_count = 0

    for attempt in range(tries):
        output = generate_text(
            current_prompt,
            max_new_tokens=max_new_tokens
        )

        output = _clean_output(output)
        output = _ensure_sentence_end(output)

        count = _count_words(output)

        if count == n_words:
            return output

        last_count = count

        current_prompt = (
            prompt
            + f"\nRewrite your answer using exactly {n_words} words."
            + "\nUse one complete sentence."
            + "\nReturn only the sentence."
            + "\nPrevious answer: "
            + output
        )

    raise Exception(
        f"Could not get exactly {n_words} words. "
        f"The last attempt had {last_count} words."
    )


# ============================
# IMAGE CAPTION
# ============================

def get_basic_caption(image_path: str) -> str:
    print(f"{Fore.YELLOW}Generating basic caption ...")

    try:
        image_url = _data_url(image_path)

    except Exception as error:
        return f"[Error] Image processing failed: {error}"

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "Describe the main subject and important "
                        "details of this image in one complete "
                        "sentence. Return only the sentence."
                    )
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                }
            ]
        }
    ]

    caption, error = _run_models(
        VISION_MODELS,
        messages,
        max_tokens=100
    )

    if caption:
        return _clean_output(caption)

    return f"[Error] {error}"


# ============================
# MENU
# ============================

def print_menu():
    print(
        f"""{Style.BRIGHT}{Fore.GREEN}
================ Image to Text Conversion ================
Select output type:

1. Caption (5 words)
2. Description (30 words)
3. Summary (50 words)
4. Exit

===========================================================
"""
    )


# ============================
# MAIN PROGRAM
# ============================

def main():
    print(f"{Fore.CYAN}Running updated program.")
    print(f"{Fore.CYAN}Vision models: {VISION_MODELS}\n")

    image_path = input(
        f"{Fore.BLUE}Enter the image path: "
        f"{Style.RESET_ALL}"
    ).strip().strip('"')

    if not os.path.isfile(image_path):
        print(f"{Fore.RED}The file does not exist.")
        return

    try:
        with Image.open(image_path) as img:
            img.verify()

    except Exception as error:
        print(f"{Fore.RED}Failed to open image: {error}")
        return

    basic_caption = get_basic_caption(image_path)

    print(
        f"\n{Fore.YELLOW}Basic caption: "
        f"{Style.BRIGHT}{basic_caption}\n"
    )

    while True:
        print_menu()

        choice = input(
            f"{Fore.CYAN}Enter your choice (1 to 4): "
            f"{Style.RESET_ALL}"
        ).strip()

        if choice == "4":
            print(f"{Fore.GREEN}Goodbye!")
            break

        if choice not in {"1", "2", "3"}:
            print(f"{Fore.RED}Invalid choice. Enter 1 to 4.")
            continue

        if basic_caption.startswith("[Error]"):
            basic_caption = get_basic_caption(image_path)

            print(
                f"{Fore.YELLOW}Basic caption: "
                f"{Style.BRIGHT}{basic_caption}\n"
            )

            if basic_caption.startswith("[Error]"):
                print(
                    f"{Fore.RED}Caption generation failed. "
                    "Check the API error above.\n"
                )
                continue

        try:
            if choice == "1":
                prompt = (
                    "Write an accurate five word caption for "
                    "this image based on the following text: "
                    + basic_caption
                )

                output = generate_exact_sentence(
                    prompt,
                    5,
                    max_new_tokens=40
                )

                print(
                    f"{Fore.GREEN}Caption (5 words): "
                    f"{Fore.YELLOW}{Style.BRIGHT}{output}\n"
                )

            elif choice == "2":
                prompt = (
                    "Describe the image using the information "
                    "in this caption: "
                    + basic_caption
                    + "\nWrite exactly 30 words in one complete "
                    "sentence. Return only the sentence."
                )

                output = generate_exact_sentence(
                    prompt,
                    30,
                    max_new_tokens=100
                )

                print(
                    f"{Fore.GREEN}Description (30 words): "
                    f"{Fore.YELLOW}{Style.BRIGHT}{output}\n"
                )

            elif choice == "3":
                prompt = (
                    "Write a detailed summary of the image "
                    "based on this caption: "
                    + basic_caption
                    + "\nWrite exactly 50 words in one complete "
                    "sentence. Return only the sentence."
                )

                output = generate_exact_sentence(
                    prompt,
                    50,
                    max_new_tokens=150,
                    tries=7
                )

                print(
                    f"{Fore.GREEN}Summary (50 words): "
                    f"{Fore.YELLOW}{Style.BRIGHT}{output}\n"
                )

        except Exception as error:
            print(
                f"{Fore.RED}Generation failed: {error}\n"
            )


if __name__ == "__main__":
    main()