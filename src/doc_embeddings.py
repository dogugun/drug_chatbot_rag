from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
import os
import chromadb
from langchain.vectorstores import Chroma

from package_extract import fetch_pdfs
from variables import VECTOR_DB_PATH
import pinecone
from langchain.vectorstores import Pinecone
BASEDIR = os.path.dirname(os.path.realpath(__file__))




def load_document(file):
    name, ext = os.path.splitext(file)
    if ext == ".pdf":
        print(f"Loading {file}")
        loader = PyPDFLoader(file)
    elif ext == ".docx":
        print(f"Loading {file}")
        loader = Docx2txtLoader(file)
    else:
        print("Document format is not supported")
    data = loader.load()
    return data


def chunk_data(data, chunk_size = 1500):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
    chunks = text_splitter.split_documents(data)
    return chunks

def get_embedding():
    model_id = 'sentence-transformers/all-MiniLM-L6-v2'
    model_kwargs = {'device': 'cpu'}
    hf_embedding = HuggingFaceEmbeddings( model_name=model_id, model_kwargs=model_kwargs )
    return hf_embedding

# TODO: use add_documents after initializing Chroma
# TODO: replicate the work from scratch in : https://developer.dataiku.com/latest/tutorials/machine-learning/genai/nlp/gpt-lc-chroma-rag/index.html#creating-the-vector-database
def save_document_to_chroma(chunks, embedding, collection_name):
    db = Chroma.from_documents(chunks,
                               embedding=embedding,
                               #metadatas=[{"source": f"{i}-wb24"} for i in range(len(chunks))],
                               persist_directory=VECTOR_DB_PATH,
                               collection_name = collection_name)
    db.persist()

def get_vector_db():
    db = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function = get_embedding())#, embedding_function=embeddings
    return db

def init_pinecone(delete=True):
    load_dotenv()
    pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"), environment=os.environ.get("PINECONE_ENV"))

    index_name = "drugexp"
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(name=index_name, dimension=384, metric="cosine", pods=1, pod_type="p1.x2")
    else:
        print(f"index {index_name} already exists")
        if delete:
            index = pinecone.Index(index_name)
            index.delete(delete_all=True)#, namespace='example-namespace'


def save_document_to_pinecone(chunks, embedding, index_name):
    db = Pinecone.from_documents(chunks, embedding, index_name=index_name)

    # db = Chroma.from_documents(chunks,
    #                            embedding=embedding,
    #                            #metadatas=[{"source": f"{i}-wb24"} for i in range(len(chunks))],
    #                            persist_directory=VECTOR_DB_PATH,
    #                            collection_name = collection_name)
    # db.persist()

def get_vector_db():
    db = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function = get_embedding())#, embedding_function=embeddings
    return db


def get_vector_db_pinecone(index_name, embeddings):
    index = pinecone.Index(index_name)
    vectorstore = Pinecone(index, embeddings.embed_query, "text")
    return vectorstore
    # db = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    # return db



def delete_collection(name):

    cclient = chromadb.PersistentClient(VECTOR_DB_PATH)

    cols = [col for col in cclient.list_collections() if col.name == name]
    if len(cols)>0:
        cclient.delete_collection(name)
        return len(cols)
    else:
        return -1


def list_documents():
    collections = chromadb.PersistentClient(VECTOR_DB_PATH).list_collections()
    return collections



def similarity_search(q, include_metadata=True):
    vector_db = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=get_embedding())
    v = vector_db.similarity_search(q, include_metadata=include_metadata)
    return v


def save_all_doc_embeddings():
    all_paths = fetch_pdfs()
    hf_embeddings = get_embedding()

    for dpath in all_paths:
        doc = load_document(dpath)

        for part in doc:
            part.page_content = part.page_content.replace("\t", " ")

        chunks = chunk_data(doc)
        collection_name =  dpath.split("/")[len(dpath.split("/"))-1].replace(".pdf", "")
        save_document_to_chroma(chunks, hf_embeddings, collection_name)


def save_all_doc_embeddings_pinecone():

    init_pinecone()

    all_paths = fetch_pdfs()
    hf_embeddings = get_embedding()
    index_name = "drugexp"

    index = pinecone.Index(index_name)
    vectorstore = Pinecone(index, hf_embeddings.embed_query, "text")

    for dpath in all_paths:
        doc = load_document(dpath)

        for part in doc:
            part.page_content = part.page_content.replace("\t", " ")

        chunks = chunk_data(doc)
        #collection_name =  dpath.split("/")[len(dpath.split("/"))-1].replace(".pdf", "")
        #save_document_to_chroma(chunks, hf_embeddings, collection_name)
        vectorstore.add_documents(chunks)


        #save_document_to_pinecone(chunks, hf_embeddings, index_name)

# save_all_doc_embeddings_pinecone()


