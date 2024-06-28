import gradio as gr
import os
import dashscope
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Milvus


os.environ["DASHSCOPE_API_KEY"] = "sk-190e2fb00a9b4233b1644ebdd080a390"



def greet(name, intensity):
    return "Hello, " + name + "!" * int(intensity)

demo = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
)


demo.launch()
