from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from text2vec import SentenceModel
from transformers import AutoModel
import os
import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

os.environ["DASHSCOPE_API_KEY"] = "sk-190e2fb00a9b4233b1644ebdd080a390" #my

# model_path='/opt/codes/Model/text2vec-base-chinese'
model_path='../Model/text2vec-base-chinese'
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

splitted_documents = text_splitter.split_documents(documents)
# docs = text_splitter.split_text(text)
print(len(splitted_documents)) # 11
print(splitted_documents[0]) 

print("开始embed")
model_kwargs = {"device": "cpu", "trust_remote_code": True,"local_files_only":True}

embeddings=HuggingFaceEmbeddings(
    model_name=model_path,model_kwargs=model_kwargs)

# # 获取要嵌入的文档内容
# texts = [doc.page_content for doc in splitted_documents]
# output = embeddings.embed_documents(texts)

# # print(len(output))
# # print(output[0]) 

print("开始FAISS")

db = FAISS.from_documents(splitted_documents, embeddings)
save_path=os.path.join("Data","faiss_index_text2vec/doc")
db.save_local(save_path)
print("向量索引已保存在：", save_path)


# test query
print("开始query")
db = FAISS.load_local(save_path, embeddings,allow_dangerous_deserialization=True)
retriever = db.as_retriever()

template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum and keep the answer as concise as possible.

{context}

Question: {question}

Helpful Answer:"""
custom_rag_prompt = PromptTemplate.from_template(template)

llm = Tongyi(model_name="qwen1.5-72b-chat")
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def chat_loop(user_input):
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | custom_rag_prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain.invoke(user_input)


user_input = "介绍一下算力情况？"
while True:
    response = chat_loop(user_input)
    print("AI助手：", response)
    user_input = input("你：")



# if __name__ == '__main__':
 
#     from text2vec import SentenceModel
#     sentences = ['如何更换花呗绑定银行卡', '花呗更改绑定银行卡']

#     model = SentenceModel(model_path)
#     embeddings = model.encode(sentences)
#     print(embeddings)
