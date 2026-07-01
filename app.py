import gradio as gr
from chatbot import ask_ai


demo = gr.ChatInterface(
    fn=ask_ai,
    title="My First AI Companion",
    description="A simple AI companion with conversation history."
)

demo.launch()