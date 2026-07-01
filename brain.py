import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from prompts import COMPANION_PROMPT

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading AI model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32
)

print("AI model loaded successfully!")


def get_text_from_message(message):
    content = message["content"]

    if isinstance(content, list):
        return content[0]["text"]

    return content


def build_messages(message, history):
    messages = [
        {
            "role": "system",
            "content": COMPANION_PROMPT
        }
    ]

    for item in history:
        role = item["role"]
        text = get_text_from_message(item)

        if role in ["user", "assistant"]:
            messages.append({"role": role, "content": text})

    messages.append({"role": "user", "content": message})

    return messages


def ask_ai(message, history):
    messages = build_messages(message, history)

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(prompt, return_tensors="pt")

    output = model.generate(
        **inputs,
        max_new_tokens=120,
        do_sample=True,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id
    )

    generated_tokens = output[0][inputs["input_ids"].shape[-1]:]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()

    return answer