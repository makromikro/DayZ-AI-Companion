import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from prompts import COMPANION_PROMPT
from config import MODEL_NAME
from memory import remember, load_memory
from ai_extractor import extract_memory_with_ai

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
            messages.append(
                {
                    "role": role,
                    "content": text
                }
            )

    messages.append(
        {
            "role": "user",
            "content": message
        }
    )

    return messages


def ask_ai(message, history):

    memory = load_memory()

    facts = extract_memory_with_ai(model, tokenizer, message)

    for key, value in facts.items():
        remember(key, value)

    memory = load_memory()

    memory_text = ""

    if memory:
        memory_text = "\nKnown facts about the user:\n"

        for key, value in memory.items():
            memory_text += f"- {key}: {value}\n"

    messages = build_messages(
        memory_text + "\n" + message,
        history
    )

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
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