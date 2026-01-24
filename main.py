# Imports
from dotenv import load_dotenv
import os
import gradio as gr

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI



# Load Environment Variables
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

# System Prompt
system_prompt = """
You are Sau-Crypto.
Answer question through Sau-Crypto's questioning and reasoning...
You will speak from your point of view. You will share personal things from your life
even when the user don't ask for it. For example, if the user asks about the theory of
relativity, you will share your personal experiencer with it and not only explain the theory.
"""


# LLM Configuration
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=gemini_key,
    temperature=0.5
)


# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])


# Chain
chain = prompt | llm | StrOutputParser()

print("Hi, I am Sau-Crypto, how can I help you?")


# Chat Function
def chat(user_input, hist):
    langchain_history = []

    for item in hist:
        if item['role'] == 'user':
            langchain_history.append(HumanMessage(content=item['content']))
        elif item['role'] == 'assistant':
            langchain_history.append(AIMessage(content=item['content']))

    response = chain.invoke({
        "input": user_input,
        "history": langchain_history
    })

    new_hist = hist + [
            {'role': "user", 'content': user_input},
            {'role': 'assistant', 'content': response}
        ]

    return "", new_hist, new_hist


def clear_chat():
    return "", [], []

# Gradio Interface (NO Blocks)
demo = gr.Interface(
    fn=chat,
    inputs=[
        gr.Textbox(
            placeholder="Ask Sau-Crypto anything...",
            label="Your Message"
        ),
        gr.State([])  # input state
    ],
    outputs=[
        gr.Textbox(),  # to clear input after sending
        gr.Chatbot(
            avatar_images=(None, "AI.png")
        ),
        gr.State([])   # output state
    ],
    title="💬 Chat with Sau-Crypto",
    description="Your personal conversation with Sau-Crypto",
)

demo.launch(share=True)