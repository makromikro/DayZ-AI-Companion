import json


def extract_memory_with_ai(chatbot, tokenizer, message):
    """
    Use the AI model to extract important facts from a message.
    """

    prompt = f"""
You are an information extraction assistant.

Extract only long-term facts about the user.

Examples:
- Name
- Country
- Age
- Favorite weapon
- Base location
- Friends
- Goals

Return ONLY valid JSON.

User message:
{message}
"""

    messages = [
        {
            "role": "system",
            "content": "Return only JSON."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    prompt_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(prompt_text, return_tensors="pt")

    output = chatbot.generate(
        **inputs,
        max_new_tokens=120,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id
    )

    generated = output[0][inputs["input_ids"].shape[-1]:]

    response = tokenizer.decode(
        generated,
        skip_special_tokens=True
    ).strip()

    try:
        return json.loads(response)
    except Exception:
        return {}