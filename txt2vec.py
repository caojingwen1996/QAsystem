from langchain_community.document_loaders.unstructured import UnstructuredFileLoader
from langchain_community.vectorstores.faiss import FAISS
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
from Configs import config

embeddings_model=HuggingFaceEmbeddings(
    model_name=config.EMBEDDING_MODEL_PATH,
    model_kwargs={"device": "cpu", "trust_remote_code": True,"local_files_only":True})

 

def load_pdf_docs():
    print("开始load")
    files=os.listdir(config.SRC_FODER_PATH)
    filepaths=[os.path.join(config.SRC_FODER_PATH,file) for file in files]
    loader=UnstructuredFileLoader(file_path=filepaths)
    documents=loader.load()
    print(len(documents))
    # print(documents[0])

    return documents
def split_docs(documents):
    print("开始split")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200, chunk_overlap=10
    )
    splitted_documents = text_splitter.split_documents(documents)
    print(len(splitted_documents))
    # print(splitted_documents[0])
    return splitted_documents



# # # 获取要嵌入的文档内容
# # texts = [doc.page_content for doc in splitted_documents]
# # output = embeddings.embed_documents(texts)

# # # print(len(output))
# # # print(output[0]) 
def embedding_doc():
    print("开始FAISS")
    splitted_documents= split_docs(load_pdf_docs())
    db = FAISS.from_documents(splitted_documents, embeddings_model)
    db.save_local(config.VECTOR_DB_PATH)
    print("向量索引已保存在：", config.VECTOR_DB_PATH)


if __name__ == '__main__':
    print(os.listdir(config.SRC_FODER_PATH))
    embedding_doc()
    
