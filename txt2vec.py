from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from text2vec import SentenceModel
from transformers import AutoModel
import os
import json

# os.environ["QIANFAN_AK"] = "v2SKnMKK94eO3IiFjEuC6jio"
# os.environ["QIANFAN_SK"] = "BAlrTZAWFqHZFeTGrqHANLziKvUFIka0"
model_path='/opt/codes/Model/text2vec-base-chinese'
filename="算力行业周刊.pdf"
model = AutoModel.from_pretrained(model_path, trust_remote_code=True) 



loader=UnstructuredFileLoader(os.path.join("Data",filename))

print("开始load")

documents=loader.load()

print("开始split")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200, chunk_overlap=10
)

docs = text_splitter.split_documents(documents)

print("开始embed")
model_kwargs = {"device": "cpu", "trust_remote_code": True}

embeddings=HuggingFaceEmbeddings(model_name=model_path)
documents = ["foo bar"]
output = embeddings.embed_documents(documents)
print(output)


# db = FAISS.from_documents(docs, embeddings)

# db.save_local(os.path.join("Data","faiss_index_text2vec/doc"))


# if __name__ == '__main__':
 
#     from text2vec import SentenceModel
#     sentences = ['如何更换花呗绑定银行卡', '花呗更改绑定银行卡']

#     model = SentenceModel(model_path)
#     embeddings = model.encode(sentences)
#     print(embeddings)
