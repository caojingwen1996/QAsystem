from Configs import config

from langchain_community.chat_message_histories import ChatMessageHistory,Neo4jChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.llms.tongyi import Tongyi
from langchain.schema import StrOutputParser

from langchain_community.graphs import Neo4jGraph
from langchain.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)

from uuid import uuid4




CYPHER_GENERATION_TEMPLATE = """Task: You are an expert Neo4j Developer translating user questions into Cypher to answer questions about movies and provide recommendations.
Convert the user's question based on the schema.Generate Cypher statement to query a graph database.
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


SESSION_ID = str(uuid4())
print(f"Session ID: {SESSION_ID}")
memory=ChatMessageHistory()
graph_db = Neo4jGraph()



def get_memory(session_id):
    # The conversation history is stored in the neo4j_graph
    # for example :
    # MATCH (s:Session)-[:LAST_MESSAGE]->(last:Message)<-[:NEXT*]-(msg:Message) RETURN s, last, msg
    return Neo4jChatMessageHistory(session_id=session_id,graph=graph_db)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a surfer dude, having a conversation about the surf conditions on the beach. Respond using surfer slang.",
        ),
        ("system", "{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)
chat_llm= Tongyi(model_name=config.LLM_MODEL_NAME)

chat_chain=prompt | chat_llm | StrOutputParser()

cypher_chain  = GraphCypherQAChain.from_llm(llm=chat_llm,
                                    graph=graph_db, 
                                    verbose=True,
                                    cypher_prompt=CYPHER_GENERATION_PROMPT, 
                                    return_intermediate_steps=True)

def chat_from_graph(input):
    print("开始chat")
    graph_q=f'query:{input}'
    result = cypher_chain.invoke(graph_q)
    print(result["intermediate_steps"])
    print(result["result"])



def do_chat():
    current_weather = """
    {
        "surf": [
            {"beach": "Fistral", "conditions": "6ft waves and offshore winds"},
            {"beach": "Bells", "conditions": "Flat and calm"},
            {"beach": "Watergate Bay", "conditions": "3ft waves and onshore winds"}
        ]
    }"""
    # for what???
    my_chat_with_message_history = RunnableWithMessageHistory(
        chat_chain,
        get_memory,
        input_messages_key="question",
        history_messages_key='chat_history',
    )

    while True:
        question = input("> ")

        response = my_chat_with_message_history.invoke(
            {
                "context": current_weather,
                "question": question,
                
            }, 
            config={
                "configurable": {"session_id": SESSION_ID}
            }
        )
        
        print(response)


if __name__ == '__main__':

    print('start to query ...')
    do_chat()