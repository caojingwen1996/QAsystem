0.爬取中文文本

1.txt2vec(专业术语embedding)
#input：text
#output:vector
【中文文本向量化模型】text2vec-base-chinese

2. vectorStore
【向量数据库】Milvus/FAISS

3.在数据库中检索
#intput: question
#output: releated text context
【检索器】retriever = db.as_retriever()

4.处理用户的输入输出
#input:question
#output:Answer
【生成模型】llm

RAG:检索-生成-增强
