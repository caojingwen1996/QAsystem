# 任务
0.爬取中文文本

1.txt2vec(专业术语embedding)
#input：text
#output:vector
【中文文本向量化模型】text2vec-base-chinese
部署参考：https://blog.csdn.net/hugo_lei/article/details/134630373bi

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


# 进度
- [x] demo搭建
- [ ] 挑选合适的rag模型
- pdf图表？
 - graph库？向量数据库+图数据库
- [ ] 搭建网页端
- [ ] 自动更新知识库

# GraphRAG
- [x] 非结构化文本创建知识图谱
  - [ ] 本地4neo4j
  - [ ] 敏感词过滤
- [ ] Cypher 知识图谱检索信息
- [ ] 向量数据库+图数据库

# RAG
## 目前存在的问题
- 多跳问题：
- 路由问题：Chunking后，年份等关键信息丢失，导致的错误。
- 数据
  - 结构化数据：embedding元数据，通过function call进行调用
  - 非结构化数据
  - 管理大文件：知识库的来源。
  - 文件解析：需要持续优化
## 应用场景
从业务简单的应用开始：
- 内部查询工具
- 智能客服
- 知识库管理
- 清晰且固定的业务（反面：逻辑与流程复杂多变）
- AI擅长的业务：生成+推理




