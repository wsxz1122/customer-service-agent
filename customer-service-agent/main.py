import os
from typing import TypedDict, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from agents import KnowledgeAgent, DataAgent, ActionAgent

load_dotenv()

# 初始化Agent
knowledge_agent = KnowledgeAgent()
data_agent = DataAgent()
action_agent = ActionAgent()
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 定义状态
class AgentState(TypedDict):
    user_input: str
    intent: str
    entities: dict
    knowledge_context: str
    data_context: dict
    reasoning_chain: List[str]  # 记录推理步骤
    planned_actions: List[dict]
    approved: bool
    final_response: str

# 节点函数
def intent_recognition(state: AgentState):
    prompt = f"识别以下客户消息的意图和实体：{state['user_input']}\n意图类别：order_query, refund, tech_support, password_reset, other"
    result = llm.invoke(prompt)
    # 简单模拟解析（生产环境可用结构化输出）
    state["intent"] = "order_query" if "订单" in state["user_input"] else "refund"
    state["entities"] = {"order_id": "ORD-12345"}  # 模拟提取
    state["reasoning_chain"] = [f"意图识别：{state['intent']}"]
    return state

def knowledge_retrieval(state: AgentState):
    # 第一跳检索：根据意图获取相关SOP
    query = f"{state['intent']} 处理流程"
    know = knowledge_agent.search(query)
    # 多跳示例：如果涉及物流异常，进一步检索
    if "物流" in state["user_input"]:
        know += "\n" + knowledge_agent.search("物流已签收但未收到")
    state["knowledge_context"] = know
    state["reasoning_chain"].append("已检索SOP和案例知识")
    return state

def data_inquiry(state: AgentState):
    # 调用数据Agent获取实时数据
    order = data_agent.query_order(state["entities"]["order_id"])
    crm = data_agent.query_crm("user@example.com")
    state["data_context"] = {"order": order, "crm": crm}
    state["reasoning_chain"].append(f"获取订单数据：{order['status']}，物流：{order['logistics']['status']}")
    return state

def decision_making(state: AgentState):
    # 长链推理：综合知识、数据，通过大模型生成决策
    prompt = f"""
    你是客服决策中心，基于以下信息做出处理决策：
    客户输入：{state['user_input']}
    意图：{state['intent']}
    知识库SOP：{state['knowledge_context']}
    实时数据：{state['data_context']}
    请给出明确的行动步骤，格式：每步一个动作及参数。如果数据冲突，请进行推理并说明依据。
    """
    decision = llm.invoke(prompt).content
    state["reasoning_chain"].append(f"决策推理：{decision}")
    # 模拟解析为动作列表（实际可结构化）
    if "物流调查" in decision:
        state["planned_actions"] = [
            {"action": "create_logistics_investigation", "params": {"order_id": "ORD-12345"}},
            {"action": "issue_coupon", "params": {"amount": 20, "reason": "物流异常补偿"}}
        ]
    else:
        state["planned_actions"] = [{"action": "provide_information", "params": {"message": decision}}]
    return state

def action_preview(state: AgentState):
    previews = []
    for act in state["planned_actions"]:
        prev = action_agent.preview_action(act["action"], act["params"])
        previews.append(prev)
    state["reasoning_chain"].append("动作预览生成，等待安全校验")
    return state

def safety_check(state: AgentState):
    # 安全门：由LLM二次校验动作的合理性
    prompt = f"校验以下拟执行操作是否安全合规，有无越权或风险：{state['planned_actions']}\n回复'批准'或'驳回'并说明理由。"
    check_result = llm.invoke(prompt).content
    if "批准" in check_result:
        state["approved"] = True
    else:
        state["approved"] = False
    state["reasoning_chain"].append(f"安全校验结果：{check_result}")
    return state

def execute_actions(state: AgentState):
    if not state["approved"]:
        state["final_response"] = "系统判定操作存在风险，已转交高级客服处理。"
        return state
    results = []
    for act in state["planned_actions"]:
        res = action_agent.execute(act["action"], act["params"])
        results.append(res)
    state["final_response"] = f"已自动为您完成以下操作：{results}"
    state["reasoning_chain"].append("所有动作已执行")
    return state

# 构建状态图
workflow = StateGraph(AgentState)
workflow.add_node("intent", intent_recognition)
workflow.add_node("knowledge", knowledge_retrieval)
workflow.add_node("data", data_inquiry)
workflow.add_node("decision", decision_making)
workflow.add_node("preview", action_preview)
workflow.add_node("safety", safety_check)
workflow.add_node("execute", execute_actions)

# 定义长链执行流
workflow.set_entry_point("intent")
workflow.add_edge("intent", "knowledge")
workflow.add_edge("knowledge", "data")
workflow.add_edge("data", "decision")
workflow.add_edge("decision", "preview")
workflow.add_edge("preview", "safety")
workflow.add_conditional_edges("safety", lambda s: "execute" if s["approved"] else END, {"execute": "execute", END: END})
workflow.add_edge("execute", END)

app = workflow.compile()

if __name__ == "__main__":
    # 模拟一个复杂工单
    user_input = "我上周三订的音箱还没收到，钱已经扣了，请帮我催一下或者退款。订单号ORD-12345"
    state = {
        "user_input": user_input,
        "intent": "",
        "entities": {},
        "knowledge_context": "",
        "data_context": {},
        "reasoning_chain": [],
        "planned_actions": [],
        "approved": False,
        "final_response": ""
    }
    final_state = app.invoke(state)
    print("=== 推理链路 ===")
    for step in final_state["reasoning_chain"]:
        print("•", step)
    print("\n=== 最终回复 ===")
    print(final_state["final_response"])