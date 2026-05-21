# MiMo Customer Service Agent (多Agent协作工单处理系统)

> 基于 LangGraph 构建的智能客服自动化工单处理系统，实现了长链推理、多Agent协作（知识检索 / 数据查询 / 动作执行）以及安全门校验机制。  
> 该项目演示了如何用大模型驱动复杂业务流程自动化，适用于售后、技术支持等场景。

## 🧠 项目简介
解决SaaS售后场景中大量重复工单人工处理效率低、准确率波动的问题。通过主控Agent调度三个专用Agent，结合RAG知识库和实时数据查询，自动完成意图识别→信息检索→决策推理→操作执行→安全校验的全链路闭环。

**核心技术点**：
- **长链推理**：多步验证与交叉校验，如先查物流→匹配SOP→决策补偿→二次审核
- **多Agent协作**：Orchestrator + Knowledge/Data/Action Agent
- **RAG**：基于FAISS的多跳检索，模拟内部知识库
- **安全门**：执行前由LLM二次审批，防止幻觉误操作

## 🛠 快速开始
1. 克隆仓库  
   `git clone https://github.com/wsxz1122/customer-service-agent`  
   `cd customer-service-agent`

2. 安装依赖  
   `pip install -r requirements.txt`

3. 配置环境变量  
   `cp .env.example .env`  
   填写你的 OpenAI Key（或任何兼容接口的密钥）

4. 运行演示  
   `python demo.py`

5. 单步调试主流程  
   `python main.py`

## 📊 预期效果（示例数据）
- 首次响应时间从18分钟降至1.9分钟
- 处理准确率提升至96.5%
- 自动解决率62%
- 日消耗Token约480万

## 📂 项目结构
- `main.py`：状态图定义与整体编排
- `agents.py`：各专用Agent及模拟系统
- `rag_knowledge.py`：本地知识库构建
- `demo.py`：快速演示多场景运行

## 🔧 适配不同模型
将 `.env` 中 `OPENAI_API_BASE` 和 `OPENAI_API_KEY` 替换为你所用大模型服务商的接口地址与密钥（如 OpenAI、MiMo、DeepSeek 等），代码中所有 `ChatOpenAI` 调用将自动走对应模型。

