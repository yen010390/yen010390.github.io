#**M01W04 - Project 1.2: Tạo và triển khai một chatbot cho một chủ đề cá nhân**


## **II. Chương trình RAG**

### **1. Cài đặt các gói thư viện cần thiết**
#(a) Import các thư viện cần thiết
!pip install -q transformers==4.52.4
!pip install -q bitsandbytes==0.46.0
!pip install -q accelerate==1.7.0
!pip install -q langchain==0.3.25
!pip install -q langchain==0.3.25 langchain-community==0.3.24

!pip install -q langchainhub==0.1.21
!pip install -q langchain-chroma==0.2.4
!pip install -q langchain_experimental==0.3.4
# !pip install -q langchain-community==0.3.24
!pip install -q langchain_huggingface==0.2.0
!pip install -q python-dotenv==1.1.0
!pip install -q pypdf
!pip install -q streamlit==1.36.0

import os
os.kill(os.getpid(), 9)

import os
import tempfile
import torch
import streamlit as st

from transformers import BitsAndBytesConfig, AutoModelForCausalLM, AutoTokenizer, pipeline

from langchain import hub
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import PyPDFLoader, TextLoader

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface.llms import HuggingFacePipeline

from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

### **2. Xây dựng vector database:**
#(a) Upload file
from google.colab import files
uploaded_files = files.upload()

#(b) Đọc file pdf
!pip install -q PyPDF2
from PyPDF2 import PdfMerger

merger = PdfMerger()
for filename in uploaded_files.keys():
    if filename.endswith(".pdf"):
        merger.append(filename)

# Lưu file PDF gộp
merged_pdf_path = "AIO-2024-All-Materials.pdf"
merger.write(merged_pdf_path)
merger.close()

from langchain_community.document_loaders import PyPDFLoader

Loader = PyPDFLoader
FILE_PATH = "./AIO-2024-All-Materials.pdf"
loader = Loader(FILE_PATH)
documents = loader.load()

print(f"Tổng số đoạn văn bản trích xuất: {len(documents)}")
print(documents[0].page_content[:500])  # In thử nội dung đoạn đầu

#(c) Khởi tạo mô hình embedding:
embedding = HuggingFaceEmbeddings(
    model_name="bkai-foundation-models/vietnamese-bi-encoder")

#(d) Khởi tạo bộ tách văn bản (text splitter):
semantic_splitter = SemanticChunker(
    embeddings=embedding,
    buffer_size=1,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=95,
    min_chunk_size=500,
    add_start_index=True
    )

docs = semantic_splitter.split_documents(documents)
print("Number of semantic chunks: ", len(docs))

#(e) Khởi tạo vector database:
vector_db = Chroma.from_documents(documents=docs,
                                  embedding=embedding)
retriever = vector_db.as_retriever()


result = retriever.invoke("What is SQL?")
print("Number of relevant documents: ", len(result))

###**3. Khởi tạo mô hình ngôn ngữ lớn Vicuna**
#(a) Khai báo một số cài đặt cần thiết cho mô hình:
nf4_config = BitsAndBytesConfig(
    oad_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
    )

#(b) Khởi tạo mô hình và tokenizer:
MODEL_NAME = "lmsys/vicuna-7b-v1.5"

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=nf4_config,
    low_cpu_mem_usage=True
    )

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


#(c) Tích hợp tokenizer và model thành một pipeline để tiện sử dụng:
model_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    pad_token_id=tokenizer.eos_token_id,
    device_map="auto"
    )

llm = HuggingFacePipeline(
    pipeline=model_pipeline,
    )

### **4. Chạy chương trình**
prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
  return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
    )

USER_QUESTION = "YOLOv10 là gì?"
output = rag_chain.invoke(USER_QUESTION)
answer = output.split("Answer:")[1].strip()
print(answer)

##**III. Xây dựng giao diện**
###**1. Cài đặt môi trường conda**
#Colab
!pip install langchain langchain-community langchainhub langchain-chroma langchain-huggingface transformers accelerate bitsandbytes


#Local
# conda create -n aio-rag python=3.11
# conda activate aio-rag

###**2. Khởi tạo Session State**
if "rag_chain" not in st.session_state:
  st.session_state.rag_chain = None
if "models_loaded" not in st.session_state:
  st.session_state.models_loaded = False
if "embeddings" not in st.session_state:
  st.session_state.embeddings = None
if "llm" not in st.session_state:
  st.session_state.llm = None

###**4. Định nghĩa các hàm hỗ trợ**
#### **4.1. Hàm tải Embedding Model**
@st.cache_resource
def load_embeddings():
  return HuggingFaceEmbeddings(model_name="bkai-foundation-models/vietnamese-biencoder")

#### **4.2. Hàm tải Large Language Model**
@st.cache_resource
def load_llm():
  MODEL_NAME = "lmsys/vicuna-7b-v1.5"
  nf4_config = BitsAndBytesConfig(
      load_in_4bit=True,
      bnb_4bit_quant_type="nf4",
      bnb_4bit_use_double_quant=True,
      bnb_4bit_compute_dtype=torch.bfloat16
      )

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True
    )

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    pad_token_id=tokenizer.eos_token_id,
    device_map="auto"
    )

return HuggingFacePipeline(pipeline=model_pipeline)

#### **4.3. Hàm xử lý PDF**
def process_pdf(uploaded_file):
  with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
    tmp_file.write(uploaded_file.getvalue())
    tmp_file_path = tmp_file.name

loader = PyPDFLoader(tmp_file_path)
documents = loader.load()

semantic_splitter = SemanticChunker(
    embeddings=st.session_state.embeddings,
    buffer_size=1,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=95,
    min_chunk_size=500,
    add_start_index=True
    )

docs = semantic_splitter.split_documents(documents)
vector_db = Chroma.from_documents(documents=docs, embedding=st.session_state.
embeddings)
retriever = vector_db.as_retriever()

prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
  return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | st.session_state.llm
    | StrOutputParser()
    )


os.unlink(tmp_file_path)
return rag_chain, len(docs)

## **5. Xây dựng giao diện người dùng**
### **5.1. Cấu hình trang và tiêu đề**
st.set_page_config(page_title="PDF RAG Assistant", layout="wide")
st.title("PDF RAG Assistant")

st.markdown("""
**Ứng dụng AI giúp bạn hỏi đáp trực tiếp với nội dung tài liệu PDF bằng tiếng Việt**
**Cách sử dụng đơn giản:**
1. **Upload PDF** Chọn file PDF từ máy tính và nhấn "Xử lý PDF"
2. **Đặt câu hỏi** Nhập câu hỏi về nội dung tài liệu và nhận câu trả lời ngay lập tức
---
""")

### **5.2. Tải models**
If not st.session_state.models_loaded:
  st.info("Đang tải models...")
  st.session_state.embeddings = load_embeddings()
  st.session_state.llm = load_llm()
  st.session_state.models_loaded = True
  st.success("Models đã sẵn sàng!")
  st.rerun()

### **5.3 Upload và xử lý PDF**
uploaded_file = st.file_uploader("Upload file PDF", type="pdf")
if uploaded_file and st.button("Xử lý PDF"):
  with st.spinner("Đang xử lý..."):
    st.session_state.rag_chain, num_chunks = process_pdf(uploaded_file)
    st.success(f"Hoàn thành! {num_chunks} chunks")

### **5.4. Giao diện hỏi đáp**
if st.session_state.rag_chain:
  question = st.text_input("Đặt câu hỏi:")
  if question:
    with st.spinner("Đang trả lời..."):
      output = st.session_state.rag_chain.invoke(question)
      answer = output.split("Answer:")[1].strip() if "Answer:" in output else

output.strip()
st.write("**Trả lời:**")
st.write(answer)

