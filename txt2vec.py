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
# model_path='/opt/codes/Model/text2vec-base-chinese'
filename="算力行业周刊.pdf"
# model = AutoModel.from_pretrained(model_path, trust_remote_code=True) 



# test="/opt/codes/QAsystem/Data/算力行业周刊.pdf"
loader=UnstructuredFileLoader(os.path.join("Data",filename))

print("开始load")

documents=loader.load()

print(len(documents))
# print(documents[0]) 

print("开始split")
# text = """What I Worked On

# February 2021

# Before college the two main things I worked on, outside of school, were writing and programming. I didn't write essays. I wrote what beginning writers were supposed to write then, and probably still are: short stories. My stories were awful. They had hardly any plot, just characters with strong feelings, which I imagined made them deep.

# The first programs I tried writing were on the IBM 1401 that our school district used for what was then called "data processing." This was in 9th grade, so I was 13 or 14. The school district's 1401 happened to be in the basement of our junior high school, and my friend Rich Draves and I got permission to use it. It was like a mini Bond villain's lair down there, with all these alien-looking machines — CPU, disk drives, printer, card reader — sitting up on a raised floor under bright fluorescent lights.
# """

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200, chunk_overlap=10
)

docs = text_splitter.split_documents(documents)
# docs = text_splitter.split_text(text)
print(len(docs)) # 11
print(docs[0]) 

# print("开始embed")
# model_kwargs = {"device": "cpu", "trust_remote_code": True}

# embeddings=HuggingFaceEmbeddings(model_name=model_path)
# documents = ["foo bar"]
# output = embeddings.embed_documents(documents)
# print(output)


# db = FAISS.from_documents(docs, embeddings)

# db.save_local(os.path.join("Data","faiss_index_text2vec/doc"))


# if __name__ == '__main__':
 
#     from text2vec import SentenceModel
#     sentences = ['如何更换花呗绑定银行卡', '花呗更改绑定银行卡']

#     model = SentenceModel(model_path)
#     embeddings = model.encode(sentences)
#     print(embeddings)
