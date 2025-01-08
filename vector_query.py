import gradio as gr
from langchain_community.vectorstores import FAISS
from y.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Milvus
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi
from Configs import config

'''
本地向量数据库作为查询源
'''


def load_knowledges_db():
    model_kwargs = {"device": "cpu", "trust_remote_code": True,"local_files_only":True}

    embeddings_model=HuggingFaceEmbeddings(
        model_name=config.EMBEDDING_MODEL_PATH,
        model_kwargs=model_kwargs)
    return FAISS.load_local(config.VECTOR_DB_PATH, embeddings_model,allow_dangerous_deserialization=True)



def load_prompt():
    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible.

    {context}

    Question: {question}

    Helpful Answer:"""
    custom_rag_prompt = PromptTemplate.from_template(template)
    return custom_rag_prompt

# test query
print("开始query")
db = load_knowledges_db()
retriever = db.as_retriever()

llm = Tongyi(model_name=config.LLM_MODEL_NAME)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def chat_loop(user_input):
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | load_prompt()
        | llm
        | StrOutputParser()
    )
    return rag_chain.invoke(user_input)

if __name__ == '__main__':
    user_input = "你能为我解答哪些困惑？"
    while True:
        response = chat_loop(user_input)
        print("智能助手：", response)
        user_input = input("你：")

