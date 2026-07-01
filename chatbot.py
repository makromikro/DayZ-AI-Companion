from transformers import pipeline

MODEL_NAME = "HuggingFaceTB/SmolLM2-360M-Instruct"

print("Loading the AI model... (This may take a few seconds)")

chatbot = pipeline(
    "text-generation",
    model=MODEL_NAME
)

print("AI model loaded successfully!")


def ask_ai(question):
    """
    Sends a question to the AI model and returns its answer.
    """

    prompt = f"User: {question}\nAssistant:"

    response = chatbot(
        prompt,
        max_new_tokens=100
    )

    full_text = response[0]["generated_text"]

    answer = full_text.replace(prompt, "").strip()

    return answer