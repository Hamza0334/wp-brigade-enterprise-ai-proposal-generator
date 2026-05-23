# Wp Brigade ENTERPRISE AI PROPOSAL GENERATOR
# IMPORTS

from dotenv import load_dotenv
import os
import logging
import requests
import uvicorn
import shutil
from pathlib import Path
from threading import RLock

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from pydantic import (
    BaseModel,
    Field
)

from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_community.vectorstores import (
    FAISS
)

from langchain_core.prompts import (
    PromptTemplate
)

from langchain_groq import (
    ChatGroq
)

# ENV VARIABLES
load_dotenv(dotenv_path=".env")

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

TEAMS_WEBHOOK_URL = os.getenv(
    "TEAMS_WEBHOOK_URL"
)

if not GROQ_API_KEY:

    raise RuntimeError(
        "GROQ_API_KEY Missing in .env"
    )
# CONSTANTS
PDF_FOLDER = "data"

VECTOR_DB_PATH = "vectorstore"

MAX_FILE_SIZE = 20 * 1024 * 1024

TOP_K_RESULTS = 2

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 150

MAX_CONTENT_LENGTH = 400

# THREAD LOCK   
vector_lock = RLock()

# LOGGING
logging.basicConfig(

    level=logging.INFO,

    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    )
)

logger = logging.getLogger(__name__)
# CREATE FOLDERS
os.makedirs(

    PDF_FOLDER,

    exist_ok=True
)
# FASTAPI APP
app = FastAPI(

    title="Enterprise AI Proposal Generator",

    version="6.0.0"
)

# CORS
app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "*"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# LOAD LLM
logger.info(
    "Loading Groq LLM..."
)

try:

    llm = ChatGroq(

        groq_api_key=GROQ_API_KEY,

        model_name="llama-3.1-8b-instant",

        temperature=0.3,

        max_tokens=2000
    )

    logger.info(
        "Groq LLM Loaded Successfully"
    )

except Exception as e:

    logger.error(
        f"LLM Load Error: {e}"
    )

    llm = None

# LOAD EMBEDDINGS
logger.info(
    "Loading Embeddings..."
)

try:

    embeddings = HuggingFaceEmbeddings(

        model_name=(
            "sentence-transformers/"
            "all-MiniLM-L6-v2"
        )
    )

    logger.info(
        "Embeddings Loaded Successfully"
    )

except Exception as e:

    logger.error(
        f"Embedding Error: {e}"
    )

    embeddings = None

# VALIDATE STARTUP
if llm is None:

    raise RuntimeError(
        "LLM failed to initialize."
    )

if embeddings is None:

    raise RuntimeError(
        "Embeddings failed to initialize."
    )

# LOAD PDF FILES
def load_pdf_files():

    all_documents = []

    try:

        files = os.listdir(
            PDF_FOLDER
        )

        pdf_files = [

            file for file in files

            if file.lower().endswith(".pdf")
        ]

        if len(pdf_files) == 0:

            logger.warning(
                "No PDF files found."
            )

            return []

        for file in pdf_files:

            try:

                pdf_path = os.path.join(
                    PDF_FOLDER,
                    file
                )

                loader = PyPDFLoader(
                    pdf_path
                )

                docs = loader.load()

                if len(docs) == 0:

                    logger.warning(
                        f"Empty PDF skipped: {file}"
                    )

                    continue

                all_documents.extend(
                    docs
                )

                logger.info(
                    f"Loaded PDF: {file}"
                )

            except Exception as e:

                logger.error(
                    f"PDF Error {file}: {e}"
                )

    except Exception as e:

        logger.error(
            f"Folder Error: {e}"
        )

    return all_documents

# SPLIT DOCUMENTS
def split_documents(documents):

    splitter = (
        RecursiveCharacterTextSplitter(

            chunk_size=CHUNK_SIZE,

            chunk_overlap=CHUNK_OVERLAP
        )
    )

    return splitter.split_documents(
        documents
    )

# CREATE VECTORSTORE
def create_vectorstore():

    global vector_store

    with vector_lock:

        try:

            logger.info(
                "Creating VectorStore..."
            )

            documents = load_pdf_files()

            if len(documents) == 0:

                logger.warning(
                    "No documents available."
                )

                return None

            docs = split_documents(
                documents
            )

            vector_store = FAISS.from_documents(

                docs,

                embeddings
            )

            vector_store.save_local(
                VECTOR_DB_PATH
            )

            logger.info(
                "VectorStore Created Successfully"
            )

            return vector_store

        except Exception as e:

            logger.error(
                f"VectorStore Error: {e}"
            )

            return None

# LOAD VECTORSTORE
def load_vectorstore():

    global vector_store

    with vector_lock:

        try:

            if embeddings is None:

                raise RuntimeError(
                    "Embeddings not initialized."
                )

            if not os.path.exists(
                VECTOR_DB_PATH
            ):

                logger.warning(
                    "VectorStore not found."
                )

                return create_vectorstore()

            vector_store = FAISS.load_local(

                VECTOR_DB_PATH,

                embeddings,

                allow_dangerous_deserialization=True
            )

            logger.info(
                "VectorStore Loaded Successfully"
            )

            return vector_store

        except Exception as e:

            logger.error(
                f"Load VectorStore Error: {e}"
            )

            return create_vectorstore()

# INITIALIZE VECTORSTORE
vector_store = load_vectorstore()

# PROMPT TEMPLATE
proposal_prompt = PromptTemplate(

    input_variables=[

        "requirement",

        "examples",

        "gap_analysis",

        "questions"
    ],

    template="""

You are an expert enterprise proposal consultant and AI solutions architect.

CLIENT REQUIREMENT:
{requirement}

REFERENCE PROPOSALS:
{examples}

GAP ANALYSIS:
{gap_analysis}

MISSING INFORMATION QUESTIONS:
{questions}

Generate a professional enterprise proposal.

Include:

1. Executive Summary
2. Problem Statement
3. Requirement Analysis
4. Proposed Solution
5. Features
6. AI Architecture
7. Technologies Used
8. Security
9. Timeline
10. Budget
11. Deliverables
12. Risks
13. Conclusion

Keep the proposal:
- Professional
- Concise
- Non-repetitive
- Enterprise-grade

"""
)

# RETRIEVE SIMILAR PROPOSALS
def retrieve_similar_proposals(
    requirement
):

    global vector_store

    with vector_lock:

        try:

            if vector_store is None:

                return (
                    "No proposal documents available."
                )

            retriever = (
                vector_store.as_retriever(

                    search_type="similarity",

                    search_kwargs={
                        "k": TOP_K_RESULTS
                    }
                )
            )

            docs = retriever.invoke(
                requirement
            )

            retrieved_text = ""

            for doc in docs:

                source = doc.metadata.get(
                    "source",
                    "Unknown"
                )

                page = doc.metadata.get(
                    "page",
                    "?"
                )

                content = (
                    doc.page_content[
                        :MAX_CONTENT_LENGTH
                    ]
                )

                retrieved_text += f"""

SOURCE: {source}
PAGE: {page}

{content}

"""

            return retrieved_text

        except Exception as e:

            logger.error(
                f"Retriever Error: {e}"
            )

            return (
                "Could not retrieve proposals."
            )

# GAP ANALYSIS
def generate_gap_analysis(

    requirement,

    retrieved_text
):

    try:

        prompt = f"""

Analyze the following.

CLIENT REQUIREMENT:
{requirement}

REFERENCE CONTENT:
{retrieved_text}

Identify:
1. Missing functionality
2. Technical gaps
3. Risks
4. Recommendations

"""

        response = llm.invoke(
            prompt
        )

        return response.content

    except Exception as e:

        logger.error(
            f"Gap Analysis Error: {e}"
        )

        return (
            "Gap analysis unavailable."
        )

# GENERATE QUESTIONS
def generate_questions(
    requirement
):

    try:

        prompt = f"""

Analyze the requirement.

Requirement:
{requirement}

Generate:
- Functional questions
- Security questions
- Deployment questions

"""

        response = llm.invoke(
            prompt
        )

        return response.content

    except Exception as e:

        logger.error(
            f"Question Generation Error: {e}"
        )

        return (
            "No questions generated."
        )

# GENERATE PROPOSAL
def generate_proposal(
    requirement
):

    try:

        retrieved_text = (
            retrieve_similar_proposals(
                requirement
            )
        )

        gap_analysis = (
            generate_gap_analysis(

                requirement,

                retrieved_text
            )
        )

        questions = (
            generate_questions(
                requirement
            )
        )

        prompt = proposal_prompt.format(

            requirement=requirement,

            examples=retrieved_text,

            gap_analysis=gap_analysis,

            questions=questions
        )

        logger.info(
            "Generating Proposal..."
        )

        response = llm.invoke(
            prompt
        )

        return getattr(

            response,

            "content",

            str(response)
        )

    except Exception as e:

        logger.error(
            f"Proposal Error: {e}"
        )

        return (
            f"Proposal Generation Error: {e}"
        )

# MICROSOFT TEAMS
def send_to_teams(message):

    if not TEAMS_WEBHOOK_URL:

        logger.warning(
            "Teams Webhook URL missing."
        )

        return

    try:

        payload = {
            "text": message
        }

        requests.post(

            TEAMS_WEBHOOK_URL,

            json=payload,

            timeout=10
        )

        logger.info(
            "Message sent to Teams."
        )

    except Exception as e:

        logger.error(
            f"Teams Error: {e}"
        )

# REQUEST MODEL
class ProposalRequest(
    BaseModel
):

    requirement: str = Field(

        min_length=20
    )


# HOME ROUTE
@app.get("/")

async def home():

    return {

        "message":
        "Enterprise AI Proposal Generator Running"
    }

# PDF UPLOAD API
@app.post("/upload-pdf")

async def upload_pdf(

    file: UploadFile = File(...)
):

    global vector_store

    try:

        if (

            not file.filename

            or

            not file.filename.lower().endswith(".pdf")
        ):

            raise HTTPException(

                status_code=400,

                detail=(
                    "Only PDF files allowed."
                )
            )

        # SAFE FILE NAME

        safe_filename = Path(
            file.filename
        ).name

        save_path = os.path.join(

            PDF_FOLDER,

            safe_filename
        )

        # DUPLICATE FILE CHECK

        if os.path.exists(save_path):

            raise HTTPException(

                status_code=400,

                detail=(
                    "PDF already exists."
                )
            )

        # READ FILE

        contents = await file.read()

        # FILE SIZE CHECK

        if len(contents) > MAX_FILE_SIZE:

            raise HTTPException(

                status_code=400,

                detail=(
                    "File too large. "
                    "Maximum 20MB allowed."
                )
            )

        # SAVE FILE

        with open(

            save_path,

            "wb"
        ) as buffer:

            buffer.write(
                contents
            )

        logger.info(
            f"Uploaded: {safe_filename}"
        )

        # REBUILD VECTORSTORE
        vector_store = (
            create_vectorstore()
        )

        return {

            "message":
            f"{safe_filename} uploaded successfully"
        }

    except HTTPException:

        raise

    except Exception as e:

        logger.error(
            f"Upload Error: {e}"
        )

        raise HTTPException(

            status_code=500,

            detail="Internal Server Error"
        )

# GENERATE PROPOSAL API
@app.post("/generate-proposal")

async def generate_proposal_api(

    request: ProposalRequest
):

    try:

        proposal = generate_proposal(
            request.requirement
        )

        send_to_teams(
            "New AI Proposal Generated Successfully."
        )

        return {

            "proposal":
            proposal
        }

    except HTTPException:

        raise

    except Exception as e:

        logger.error(
            f"API Error: {e}"
        )

        raise HTTPException(

            status_code=500,

            detail="Internal Server Error"
        )


# RUN SERVER
if __name__ == "__main__":

    uvicorn.run(

        "app:app",

        host="0.0.0.0",

        port=8000,

        reload=True
    )