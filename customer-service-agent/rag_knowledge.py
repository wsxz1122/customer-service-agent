import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

# 模拟内部知识库文档
def create_sample_documents():
    docs = [
        Document(page_content="物流已签收但客户未收到的处理SOP：1. 核实签收照片；2. 若签收人非本人，发起物流调查；3. 调查期间补偿客户20元优惠券；4. 调查结果确认后按情况退款/重发。", metadata={"source": "sop_logistics"}),
        Document(page_content="退款政策：未签收订单全额退款；已签收非质量问题的退货需扣除运费；质量问题全额退款并承担运费。退款到账时间3-5个工作日。", metadata={"source": "refund_policy"}),
        Document(page_content="API 403错误常见原因：1. API密钥过期；2. 请求频率超限；3. IP未加入白名单。处理步骤：检查密钥有效期 → 查看限流配额 → 验证IP白名单配置。", metadata={"source": "api_troubleshoot"}),
        Document(page_content="密码重置流程：用户需提供注册邮箱，系统发送验证码，验证通过后允许设置新密码。需确保账户处于正常状态。", metadata={"source": "password_reset"}),
    ]
    return docs

def build_vectorstore():
    docs = create_sample_documents()
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore