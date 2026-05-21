from langchain_openai import ChatOpenAI
from rag_knowledge import build_vectorstore

# 初始化全局知识库（生产环境可替换为远端向量数据库）
vectorstore = build_vectorstore()

class KnowledgeAgent:
    """知识检索Agent：基于RAG进行多跳检索"""
    def __init__(self):
        self.retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)  # 可替换为MiMo

    def search(self, query: str, context: str = "") -> str:
        # 单次检索，可结合上下文进行多跳
        docs = self.retriever.get_relevant_documents(query)
        knowledge = "\n".join([d.page_content for d in docs])
        return knowledge

class DataAgent:
    """数据查询Agent：模拟调用内部订单、物流等系统"""
    @staticmethod
    def query_order(order_id: str):
        # 模拟数据
        return {
            "order_id": order_id,
            "status": "delivered",
            "payment": "paid",
            "logistics": {
                "status": "signed",
                "signee": "前台代收",
                "time": "2026-05-18"
            },
            "amount": 299.0
        }

    @staticmethod
    def query_crm(email: str):
        return {"vip_level": "gold", "total_spent": 12000}

class ActionAgent:
    """动作执行Agent：模拟执行操作，并返回预览供校验"""
    @staticmethod
    def preview_action(action: str, params: dict):
        return f"预览：即将执行【{action}】，参数：{params}"

    @staticmethod
    def execute(action: str, params: dict):
        # 模拟真实API调用
        print(f"✅ 执行动作：{action}，参数：{params}")
        return {"status": "success", "action": action}