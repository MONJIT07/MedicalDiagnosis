import os
import time
import asyncio
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from fastapi import UploadFile

from pinecone import Pinecone, ServerlessSpec

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from ..config.db import reports_collection

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medicaldiagnosis")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploaded_reports")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY or ""

os.makedirs(UPLOAD_DIR, exist_ok=True)

# -----------------------------
# Initialize Pinecone
# -----------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)

existing_indexes = pc.list_indexes().names()

if PINECONE_INDEX_NAME not in existing_indexes:

    print("Creating Pinecone Index...")

    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=3072,
        metric="dotproduct",
        spec=ServerlessSpec(
            cloud="aws",
            region=PINECONE_ENV,
        ),
    )

    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)

index = pc.Index(PINECONE_INDEX_NAME)

# -----------------------------
# Embedding Model
# -----------------------------
embed_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)
# -----------------------------
# Upload + Embed
# -----------------------------
async def load_vectorstore(
    uploaded_files: List[UploadFile],
    uploaded: str,
    doc_id: str,
):

    print("=" * 80)
    print("VECTORSTORE DOC_ID :", doc_id)
    print("UPLOADER :", uploaded)
    print("=" * 80)

    for file in uploaded_files:

        filename = Path(file.filename).name
        save_path = Path(UPLOAD_DIR) / f"{doc_id}_{filename}"

        # Save uploaded PDF
        content = await file.read()

        with open(save_path, "wb") as f:
            f.write(content)

        # Load PDF
        loader = PyPDFLoader(str(save_path))
        documents = loader.load()

        # Better chunking for medical reports
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ],
        )

        chunks = splitter.split_documents(documents)

        print(f"Total chunks created: {len(chunks)}")

        texts = [chunk.page_content for chunk in chunks]

        ids = [
            f"{doc_id}-{i}"
            for i in range(len(chunks))
        ]

        metadatas = [
            {
                "source": filename,
                "doc_id": doc_id,
                "uploader": uploaded,
                "page": chunk.metadata.get("page"),
                "text": chunk.page_content[:2000],
            }
            for chunk in chunks
        ]

        print(f"Embedding {len(chunks)} chunks...")

        embeddings = await asyncio.to_thread(
            embed_model.embed_documents,
            texts,
        )
        print("=" * 80)
        print("UPSERT DOC_ID :", doc_id)
        print("VECTOR IDS :", ids)
        print("FIRST METADATA :", metadatas[0])
        print("Embedding Dimension :", len(embeddings[0]))
        print("=" * 80)

        print("Uploading vectors to Pinecone...")

        await asyncio.to_thread(
            index.upsert,
            vectors=list(zip(ids, embeddings, metadatas)),
        )

        print("Checking upload...")

        fetch_result = await asyncio.to_thread(
            index.fetch,
            ids=[ids[0]]
        )

        print("=" * 80)
        print("FETCH RESULT")
        print(fetch_result)
        print("=" * 80)

        print("Vectors uploaded successfully.")

        reports_collection.insert_one(
            {
                "doc_id": doc_id,
                "filename": filename,
                "uploader": uploaded,
                "num_chunks": len(chunks),
                "uploaded_at": time.time(),
            }
        )

        print("MongoDB metadata saved.")