from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OctoAIEmbeddings
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter, HTMLHeaderTextSplitter
import os

load_dotenv()
OCTOAI_API_TOKEN = os.environ["OCTOAI_API_TOKEN"]

TEMPLATE = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. You are a cloudformation expert.
Question: {question} 
Context: {context} 
Answer:
"""

def make_context(corpus):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024,
        chunk_overlap=128,
    )
    
    splits = text_splitter.split_text(corpus)

    llm = OctoAIEndpoint(
        model_kwargs={"model":"meta-llama-3-70b-instruct"},
        max_tokens=1024,
        presence_penalty=0,
        temperature=0.1,
        top_p=0.9
    )

    embeddings = OctoAIEmbeddings()

    vector_store = FAISS.from_texts(splits, embedding=embeddings)

    retriever = vector_store.as_retriever()

    llm = OctoAIEndpoint(
        model_kwargs={"model":"meta-llama-3-70b-instruct"},
        max_tokens=1024,
        presence_penalty=0,
        temperature=0.1,
        top_p=0.9
    )

    prompt = ChatPromptTemplate.from_template(TEMPLATE)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain
    
def run_query(context, query):
    chain = context
    return chain.invoke(query)

if __name__ == "__main__":
    infrastructure = ""
    with open("source-bucket.yml", "r") as f:
        infrastructure = f.read()
    
    context = make_context(infrastructure)
    result  = run_query(context, "Describe my cloudformation resources.")
    print(result)
