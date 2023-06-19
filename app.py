import os, gradio
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from vectorstore import VectorstoreIndexCreator

os.environ['MPLCONFIGDIR'] = '/tmp/'
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

text_folder = '10K_Annual_Reports'
loaders = [UnstructuredPDFLoader(os.path.join(text_folder, fn)) for fn in os.listdir(text_folder)]

# Create the index, if it does not exist, and save it
if not os.path.isfile('VectorStoreIndex/chroma-embeddings.parquet'):
  from langchain.vectorstores import Chroma
  index = VectorstoreIndexCreator(vectorstore_cls=Chroma, vectorstore_kwargs={ "persist_directory": "VectorStoreIndex/"}).from_loaders(loaders)
  index.vectorstore.persist()

# Load the saved index
index_saved = VectorstoreIndexCreator().from_persistent_index("VectorStoreIndex")

description = """This is an AI conversational agent where you provide it with the annual reports of companies, and it can study it and answer any questions 
you have about it. Currently, the LLM has been trained on the following companies' 10-K reports: Amazon, Apple, Alphabet (Google), Meta (Facebook), Microsoft, 
Netflix and Tesla.' I plan to include more companies' 10-K reports in future.
Once the LLM is trained on a new 10-K report, it stores the vector embeddings of the document locally using ChromaDB to make the querying faster and also to 
save time and money on creating the vector embeddings for the same document in future.
The LLM's universe is only the 10-K reports it has been trained on; it cannot pull information from the internet. So, you can ask it about anything that's 
contained in their 10-K reports. If it cannot find an answer to your query within the 10-K reports, it will reply with "I don't know". Some example of questions 
you can ask are: 
    - What are the risks for Tesla?
    - What was Google's earnings for the last fiscal year?
    - Who are the competetors of Apple?
An example of querying about something the LLM's training did not include: 
    - Query:    "What is Tesco?"
    - Response: " Tesco is not mentioned in the context, so I don't know."
"""

def chat_response(query):
  return index_saved.query(query)

if __name__ == "__main__":
    interface = gradio.Interface(fn=chat_response, inputs="text", outputs="text", title='Annual Reports GPT', description=description)
    
    interface.launch(server_name="0.0.0.0", server_port=7860)
