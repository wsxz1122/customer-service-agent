from main import app, AgentState

if __name__ == "__main__":
    test_queries = [
        "我的订单ORD-12345显示已签收但我没收到货，请处理",
        "我刚刚的付款被扣了两次，帮我退款",
    ]
    for q in test_queries:
        state = AgentState(
            user_input=q, intent="", entities={}, knowledge_context="",
            data_context={}, reasoning_chain=[], planned_actions=[], approved=False,
            final_response=""
        )
        result = app.invoke(state)
        print(f"客户：{q}")
        print(f"回复：{result['final_response']}\n")
        print("推理链：", result["reasoning_chain"])
        print("-"*50)