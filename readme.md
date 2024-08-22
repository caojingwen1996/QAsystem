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
过程：知识生产与加工、query改写、数据召回、后置处理以及大模型生产。


# 进度
- [x] demo搭建
- [ ] 挑选合适的rag模型
 - [ ] graph库
- [ ] 搭建网页端
- [ ] 自动更新知识库


# GraphRAG

## 进度
- [x] 非结构化文本创建知识图谱
  - [x] linux部署neo4j
  - [x] windows部署neo4j
  - [x] llm连接neo4j
  - [x] 生成知识图谱？  graph_db.add_graph_documents([doc]) 
  - [x] 如何查询知识图谱？GraphCypherQAChain
  - [ ] 建设工程规范-知识图谱
  - [ ] 如何保存对话历史？
  - [ ] 如何融合查询？
  - [ ] 敏感词过滤
- [ ] Cypher 知识图谱检索信息
- [ ] 向量数据库+图数据库
- [ ] 
## neo4j部署
Linux部署neo4j server,用nginx反向代理，便于二级域名管理。

## neo4j导入数据
doc->graph_doc->add_to_graphDB

## neo4j查询数据

















# 我要用RAG做什么？



形式？
- 融合多人？
- 数据获取形式？爬虫
  

## 从设计模式分类
- 自我反思（Reflection）
- 使用工具（Tool Use）
- 规划（Planning）
- 多智能体协作
  
## 从应用场景分类
- 知识库:
  - 客户项目管理
    - 目的：激活用户与资料的连接。
    - 背景：项目开发周期长，人员庞杂且变动频繁，过程资料多。 整个周期内留下的文件有：需求调研，规范文件，项目过程文件（设计，研发，实施，会议记录）
- 文件管理：【文档管理】模块+AI
- 清晰且固定的业务（反面：逻辑与流程复杂多变）
- AI擅长的业务：生成+推理
  - 数据分析

## 如何根据业务逻辑制作智能体
参考文章：https://cloud.tencent.com/developer/article/2427655









