from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import os

import json

os.environ["QIANFAN_AK"] = "v2SKnMKK94eO3IiFjEuC6jio"
os.environ["QIANFAN_SK"] = "BAlrTZAWFqHZFeTGrqHANLziKvUFIka0"

fileID="ufyqh7egryk25xbm"
filename="西安市高新城·阳光里项目（一期）工程BIM技术应用PPT汇报"

loader=UnstructuredFileLoader(os.path.join("data",fileID,filename+".pptx"))

print("开始load")

documents=loader.load()

print("开始split")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200, chunk_overlap=10
)

docs = text_splitter.split_documents(documents)

print("开始embed")

embeddings=HuggingFaceEmbeddings(model_name="/opt/models/text2vec-base-chinese")

db = FAISS.from_documents(docs, embeddings)

db.save_local(os.path.join("data",fileID,"faiss_index_text2vec/doc"))