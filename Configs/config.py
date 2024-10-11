
import os


# 用于Embedding的本地模型路径
EMBEDDING_MODEL_PATH='/Model/text2vec-base-chinese'

# 本地向量数据库的root路径
VECTOR_DB_PATH='Data/VectorDB/faiss_index_text2vec'

# 待处理的文档
SRC_FODER_PATH='Data/src/bim'


#tongyi
os.environ["DASHSCOPE_API_KEY"] = "sk-3791888c6e47445eadb80fe15d80d8cd" #my
LLM_MODEL_NAME = "qwen2-7b-instruct" #0.006元/千Token

#username: neo4j
# os.environ["NEO4J_USERNAME"]='neo4j'
# os.environ["NEO4J_PASSWORD"]='SOupwIu7HWAokTWi-fBJhPV77cs6YBpbrRG-QrjxYRM'    
# os.environ["NEO4J_URI"]='neo4j+s://a6a79697.databases.neo4j.io'

# local
os.environ["NEO4J_URI"]='bolt://localhost:7687'
os.environ["NEO4J_USERNAME"]='neo4j'
os.environ["NEO4J_PASSWORD"]='12345678'

