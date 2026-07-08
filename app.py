import gradio as gr

from core.runtime import process_message


def chat(message, history):
    return process_message(message, history)


demo = gr.ChatInterface(
    fn=chat,
    title="DayZ AI Companion"
)

demo.launch()