from brain import tokenizer, model
from ai_extractor import extract_memory_with_ai

message = "My name is Burak. I live in Germany. My favorite weapon is the M4A1."

result = extract_memory_with_ai(
    model,
    tokenizer,
    message
)

print(result)