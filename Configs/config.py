
import os


# 用于Embedding的本地模型路径
EMBEDDING_MODEL_PATH='../Model/text2vec-base-chinese'

# 本地向量数据库的root路径
VECTOR_DB_PATH='Data/VectorDB/faiss_index_text2vec'

# 待处理的文档
SRC_FODER_PATH='Data/src/tulong'


#tongyi
os.environ["DASHSCOPE_API_KEY"] = "sk-190e2fb00a9b4233b1644ebdd080a390" #my
LLM_MODEL_NAME = "qwen2-1.5b-instruct" #my

#username: neo4j
os.environ["NEO4J_USERNAME"]='neo4j'
os.environ["NEO4J_PASSWORD"]='SOupwIu7HWAokTWi-fBJhPV77cs6YBpbrRG-QrjxYRM'
os.environ["NEO4J_URI"]='neo4j+s://a6a79697.databases.neo4j.io'
