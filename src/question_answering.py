from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
import os
from langchain.document_loaders import PyPDFLoader
from langchain.output_parsers import CommaSeparatedListOutputParser, PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Chroma
import pinecone

from doc_embeddings import get_vector_db, get_vector_db_pinecone, get_embedding
from llm_wrapper import get_gpt_llm

chat = get_gpt_llm()

"""chain = load_qa_chain(chat, chain_type="stuff")
res = chain({"input_documents": v, "question": q})
print(res["output_text"])
"""

def run_qa_chain(chain, query, vec_db) -> str:
    # Lookup
    docs = vec_db.similarity_search(query, k=10, include_metadata=True)
    res = chain({"input_documents": docs, "question": query})
    return res["output_text"]


def run_qa_chain_pinecone(chain, query, vec_db) -> str:

    docs = vec_db.similarity_search(query, k=3)
    res = chain({"input_documents": docs, "question": query})
    return res["output_text"]

# Chain 1
query = """
What does Hydroxyzine pamoate actually do?
"""

reg_parser = CommaSeparatedListOutputParser()
reg_pfi = reg_parser.get_format_instructions()

# Define the prompt template
reg_prompt = PromptTemplate(template="{context}\n{question}\n{fmt}",
                               input_variables=["context", "question"],
                               partial_variables={"fmt": reg_pfi})

# Define the question-answering chain
qa_chain = load_qa_chain(chat, chain_type="stuff", prompt=reg_prompt)

#reg_simsearch = get_vector_db().similarity_search(query, include_metadata=True)
index_name = "drugexp"
#res = run_qa_chain(chain=qa_chain, query=query, vec_db=get_vector_db())

load_dotenv()
pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"), environment=os.environ.get("PINECONE_ENV"))

res = run_qa_chain_pinecone(chain=qa_chain, query=query, vec_db=get_vector_db_pinecone(index_name, get_embedding()))

#print(reg_simsearch)
print(res)

