import json
import torch


def extract_memory_with_ai(model, tokenizer, message):
    """
    Use the AI model to extract important long-term facts
    from a user message.
    """

    prompt = f"""
You are an information extraction assistant.

Extract only long-term facts about the user.

Examples of things to remember:
- Name
- Age
- Country
- Favorite weapon
- Base location
- Friends
- Goals

Return ONLY valid JSON.

Example:

User:
My name is Burak. I live in Germany. My favorite weapon is the M4A1.

Output:
{{
    "player_name": "Burak",
    "country": "Germany",
    "favorite_weapon": "M4A1"
}}

User:
{message}
"""

    messages = [
        {
            "role": "system",
            "content": "Return only valid JSON."
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

    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    generated = output[0][inputs["input_ids"].shape[-1]:]

    response = tokenizer.decode(
        generated,
        skip_special_tokens=True
    ).strip()

    print("\n==============================")
    print("RAW AI EXTRACTOR RESPONSE")
    print("==============================")
    print(response)
    print("==============================\n")

    # Remove markdown code fences if the model added them
    clean_response = (
        response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        memory = json.loads(clean_response)

        print("Parsed memory:")
        print(memory)

        return memory

    except Exception as e:
        print("JSON parsing failed:")
        print(e)
        return {}