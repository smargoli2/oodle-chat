import time
import datetime
import os

from dotenv import load_dotenv

from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone

from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

start = time.perf_counter()

# Setup environment variables for OpenAI & Pinecone
load_dotenv()
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
PINECONE_API_KEY = os.environ['PINECONE_API_KEY']
PINECONE_ENV = os.environ['PINECONE_ENV']

# Load in a local wiki of txt files
loader = DirectoryLoader('docs')

data = loader.load()

print(f'You have {len(data)} documents(s) in your data')

# Setup a connection to the OpenAI Embeddings
embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')

# Setup a connection to the Pinecone Vector Database to store the mappings
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_ENV
)
index_name = 'langchain-oodle'

metadata = [
    {
        'title': "Sales Orders Part 1 - Intro to Pending Allocation page",
        'video_link': "https://www.dropbox.com/s/3jcoaz66xe9e0ks/Sales%20Orders%20Part%201%20-%20Intro%20to%20Pending%20Allocation%20page.mp4?dl=0"
    },
    {
        'title': "Sales Orders Part 2 - Import",
        'video_link': "https://www.dropbox.com/s/3ffjucr92gfvgxw/Sales%20Orders%20Part%202%20-%20Import.mp4?dl=0"
    },
    {
        'title': "Sales Orders Part 3 - Manual Entry",
        'video_link': "https://www.dropbox.com/s/2rt4e7yh9wef17q/Sales%20Orders%20Part%203%20-%20Manual%20Entry.mp4?dl=0"
    },
    {
        'title': "Sales Orders Part 4 - Edit",
        'video_link': "https://www.dropbox.com/s/9p295u0b6tvkbbf/Sales%20Orders%20Part%204%20-%20Edit.mp4?dl=0"
    },
    {
        'title': "Sales Orders Part 5 - Cancel",
        'video_link': "https://www.dropbox.com/s/mrlksb4nggq3qbw/Sales%20Orders%20Part%205%20-%20Cancel.mp4?dl=0"
    },
    {
        'title': "Sales Orders Part 6 - Cut Quantity",
        'video_link': "https://www.dropbox.com/s/l9gxsaav20kcj09/Sales%20Orders%20Part%206%20-%20Cut%20Quantity.mp4?dl=0"
    },
    {
        'title': "Sales Orders Part 7 - Swap Model Number",
        'video_link': "https://www.dropbox.com/s/py25khzjc0gkmlz/Sales%20Orders%20Part%207%20-%20Swap%20Model%20Number.mp4?dl=0"
    },
    {
        'title': "Sales Orders Part 8 - Allocate",
        'video_link': "https://www.dropbox.com/s/i3ylsl159qpchqx/Sales%20Orders%20Part%208%20-%20Allocate.mp4?dl=0"
    },
    {
        'title': "Sales Orders Part 9 - Multi-Warehouse Allocation",
        'video_link': "https://www.dropbox.com/s/6naty0ee6pwfdse/Sales%20Orders%20Part%209%20-%20Multi-Warehouse%20Allocation.mp4?dl=0"
    }
]

#delete existing data
# index = pinecone.Index('langchain-oodle')
# index.delete(deleteAll=True)

# Update the Pinecode index (in the Cloud) 
docsearch = Pinecone.from_texts([d.page_content for d in data], embeddings, index_name=index_name, metadatas=metadata)

end = time.perf_counter()

duration = end - start

print(str(datetime.timedelta(seconds=duration)))