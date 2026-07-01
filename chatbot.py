from transformers import pipeline

MODEL_NAME = "HuggingFaceTB/SmolLM2-360M-Instruct"

print("Loading the AI model... (This may take a few seconds)")

chatbot = pipeline(
    "text-generation",
    model=MODEL_NAME
)

print("AI model loaded successfully!")


def get_text_from_message(message):
    """
    Extracts plain text from a Gradio message.
    """

    content = message["content"]

    if isinstance(content, list):
        return content[0]["text"]

    return content


def build_prompt(message, history):
    """
    Builds a conversation prompt from chat history and the latest message.
    """

    prompt = (
    "You are a friendly AI companion.\n"
    "Answer the user directly and naturally.\n"
    "Do not analyze the sentence unless the user asks you to.\n"
    "Keep answers short and conversational.\n\n"
)

    for item in history:
        role = item["role"]
        text = get_text_from_message(item)

        if role == "user":
            prompt += f"User: {text}\n"
        elif role == "assistant":
            prompt += f"Assistant: {text}\n"

    prompt += f"User: {message}\nAssistant:"

    return prompt


def ask_ai(message, history):
    """
    Sends the full conversation to the AI model and returns the assistant answer.
    """

    prompt = build_prompt(message, history)

    response = chatbot(
        prompt,
        max_new_tokens=120
    )

    full_text = response[0]["generated_text"]

    answer = full_text.replace(prompt, "").strip()

    return answer