import gradio as gr
from chatbot import ask_ai


demo = gr.ChatInterface(
    fn=ask_ai,
    title="My First AI Companion",
    description="A simple AI companion powered by Hugging Face and Python."
)

demo.launch()