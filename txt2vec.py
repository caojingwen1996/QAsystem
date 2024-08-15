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
from langchain_experimental.graph_transformers import LLMGraphTransformer


# neo4j
from langchain.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores import Neo4jVector


from langchain_core.documents import Document
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)

CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.
Examples: Here are a few examples of generated Cypher statements for particular questions:
# How many people played in Top Gun?
MATCH (m:Movie {{name:"Top Gun"}})<-[:ACTED_IN]-()
RETURN count(*) AS numberOfActors

The question is:
{question}"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)

embeddings_model=HuggingFaceEmbeddings(
    model_name=config.EMBEDDING_MODEL_PATH,
    model_kwargs={"device": "cpu", "trust_remote_code": True,"local_files_only":True})
llm = Tongyi(model_name=config.LLM_MODEL_NAME)
graph_db = Neo4jGraph()
chain = GraphCypherQAChain.from_llm(llm=llm,
                                    graph=graph_db, 
                                    verbose=True,
                                    cypher_prompt=CYPHER_GENERATION_PROMPT, 
                                    return_intermediate_steps=True)
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
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=10
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

def graph_doc():
   
    splitted_documents= split_docs(load_pdf_docs())
    
    print("开始graph")
    llm_transformer = LLMGraphTransformer(llm=llm)
    graph_documents= llm_transformer.convert_to_graph_documents(splitted_documents)
    print(len(graph_documents))
    i=len(graph_documents)
    for doc in graph_documents:
        # print(doc)
        graph_db.add_graph_documents([doc]) 
        print(i)
        i=i-1

    #     print('nodes')
    #     print(doc.nodes)
    #     print('Relationships')
    #     print(doc.relationships)
    

    # 太多了 需要分批保存
    # graph.add_graph_documents(graph_documents) 
    print("save to neo4j graph db") 
 
def chat_from_graph(input):
    print("开始chat")
    graph_q=f'query:{input}'
    result = chain.invoke(graph_q)
    print(result["intermediate_steps"])
    print(result["result"])


if __name__ == '__main__':
    # print(os.listdir(config.SRC_FODER_PATH))
    # embedding_doc()
    # graph_db.refresh_schema()
    # print("refresh schema")
    # graph_doc()
    chat_from_graph("关于制造税收的段落")



