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
from langchain_community.llms.tongyi import Tongyi
from langchain_community.chat_models import ChatTongyi
from langchain_experimental.graph_transformers import LLMGraphTransformer


# neo4j

from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores import Neo4jVector


from langchain_core.documents import Document
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)




embeddings_model=HuggingFaceEmbeddings(
    model_name=config.EMBEDDING_MODEL_PATH,
    model_kwargs={"device": "cpu", "trust_remote_code": True,"local_files_only":True})
llm = Tongyi(model_name=config.LLM_MODEL_NAME)
chat_tongyi=ChatTongyi(model_name=config.LLM_MODEL_NAME)
graph_db = Neo4jGraph() # neo4j python driver

# result['intermediate_steps']  result['result']

 


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

    #普通切分 vs 基于语义的切分
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300, chunk_overlap=10
    )
    splitted_documents = text_splitter.split_documents(documents)
    print(len(splitted_documents))
    # for doc in splitted_documents:
    #     print(doc.page_content)
    #     print('--------')
    # print(splitted_documents[0])
    return splitted_documents



# # # 获取要嵌入的文档内容

def embedding_doc():
    print("开始FAISS")
    splitted_documents= split_docs(load_pdf_docs())
    db = FAISS.from_documents(splitted_documents, embeddings_model)
    db.save_local(config.VECTOR_DB_PATH)
    print("向量索引已保存在：", config.VECTOR_DB_PATH)

def save_to_graph(graph_docs):
    i=len(graph_docs)
    for doc in graph_docs:
        graph_db.add_graph_documents([doc]) 
        print(i)
        print(doc.nodes)
        i=i-1
        #     print('nodes')
        #     print(doc.nodes)
        #     print('Relationships')
        #     print(doc.relationships)
    
def graph_doc():
   
    splitted_documents= split_docs(load_pdf_docs())
    
    print("开始graph")
    llm_transformer = LLMGraphTransformer(llm=llm)
    i=len(splitted_documents)
   
        # print(doc)
    graph_docs=[]
    def batch_process(documents, batch_size):
        for i in range(0, len(documents), batch_size):
            yield documents[i:i + batch_size]
    batch_size = 100  # 根据实际情况调整批处理大小
    graph_docs = []

    for batch in batch_process(splitted_documents, batch_size):
        try:
            batch_graph_doc= llm_transformer.convert_to_graph_documents(batch) # how to make good nodes?
            graph_docs.extend(batch_graph_doc)
            print(len(graph_docs))
            save_to_graph(batch_graph_doc)
        except Exception as e:
            print(f"An exception occurred: {e}")
            continue
 
 
    

    # 太多了 需要分批保存
    # graph.add_graph_documents(graph_documents) 
    print("save to neo4j graph db") 
 



if __name__ == '__main__':
    # print(os.listdir(config.SRC_FODER_PATH))
    # embedding_doc()
    # graph_db.refresh_schema()
    # print("refresh schema")
    graph_doc()
  



