import os 
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
# from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
# from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
# import tempfile
from langchain.callbacks import get_openai_callback
# import panel as pn


def qa(file, query, chain_type, k):
   # load document
    loader = PyPDFLoader(file)
    documents = loader.load()
    # split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    # select which embeddings we want to use
    embeddings = OpenAIEmbeddings()
    # create the vectorestore to use as the index
    db = Chroma.from_documents(texts, embeddings)
      # expose this index in a retriever interface
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    # create a chain to answer questions 
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(), chain_type=chain_type, retriever=retriever, return_source_documents=True)
    result = qa({"query": query})
    print(result['result'])
    return result


def qa_result(api_key,prompt_text,file_name,Chain_type):
    os.environ["OPENAI_API_KEY"] = api_key
    if prompt_text:
        with get_openai_callback() as cb: 
            result = qa(file="./pdf_temp_storage/"+file_name, query=prompt_text, chain_type=Chain_type, k=2)
            # print(f"Total Tokens: {cb.total_tokens}")
            # print(f"Prompt Tokens: {cb.prompt_tokens}")
            # print(f"Completion Tokens: {cb.completion_tokens}")
            # print(f"Total Cost (USD): ${cb.total_cost}")
            return {"response":result["result"],
                    "reference":result["source_documents"],
                    "Total Tokens": {cb.total_tokens},
                    "Prompt Tokens": {cb.prompt_tokens},
                    "Completion Tokens": {cb.completion_tokens}
                    }

       
#   qa_result("Which year this Document is published","refine")
