import os
import asyncio

from dotenv import load_dotenv

from pinecone import Pinecone

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
    "medicaldiagnosis",
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# ==========================================================
# Pinecone
# ==========================================================

pc = Pinecone(api_key=PINECONE_API_KEY)

index = pc.Index(PINECONE_INDEX_NAME)

# ==========================================================
# Embedding Model
# ==========================================================

embed_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

# ==========================================================
# LLM
# ==========================================================

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.2,
)

# ==========================================================
# Prompt
# ==========================================================

prompt = PromptTemplate.from_template(
"""
You are an expert AI Medical Assistant.

Your job is to answer ONLY from the uploaded medical report.

Never use outside medical knowledge.

Never hallucinate.

If the answer is not present inside the report, say exactly:

"This information is not available in the uploaded report."

Always answer professionally.

Medical Report
--------------
{context}

User Question
-------------
{question}

Your response MUST follow this format.

## Direct Answer

Answer the user's question directly.

## Supporting Evidence

Quote only the relevant findings from the report.

## Medical Interpretation

Explain the findings in simple language.

## Recommended Next Steps

Provide only general medical recommendations.

Never prescribe medicines.
"""
)

rag_chain = prompt | llm
# ==========================================================
# Diagnosis Function
# ==========================================================

async def diagnosis_report(
    user: str,
    doc_id: str,
    question: str,
):

    print("=" * 80)
    print("USER :", user)
    print("DOC ID :", doc_id)
    print("QUESTION :", question)
    print("=" * 80)

    try:

        # --------------------------------------------------
        # Create Query Embedding
        # --------------------------------------------------

        embedding = await asyncio.to_thread(
            embed_model.embed_query,
            question,
        )

        # --------------------------------------------------
        # Search Pinecone
        # --------------------------------------------------

        results = await asyncio.to_thread(
            index.query,
            vector=embedding,
            top_k=15,
            include_metadata=True,
            filter={
                "doc_id": {
                    "$eq": doc_id
                }
            }
        )

        matches = results.get("matches", [])

        print("=" * 80)
        print("Retrieved Chunks :", len(matches))
        print("=" * 80)

        contexts = []
        sources = set()

        for i, match in enumerate(matches, start=1):

            metadata = match.get("metadata", {})

            score = match.get("score", 0)

            print(
                f"Chunk {i} | Score : {score:.4f} | Source : {metadata.get('source')}"
            )

            text = metadata.get("text", "")

            print("-" * 80)
            print(text[:300])
            print("-" * 80)

            if text.strip():
                contexts.append(text)

            source = metadata.get("source")

            if source:
                sources.add(source)

        print("=" * 80)
        print("Total Contexts :", len(contexts))
        print("=" * 80)

        # --------------------------------------------------
        # Remove Duplicate Chunks
        # --------------------------------------------------

        contexts = list(dict.fromkeys(contexts))

        # --------------------------------------------------
        # No Context Found
        # --------------------------------------------------

        if len(contexts) == 0:

            return {
                "diagnosis": None,
                "sources": [],
                "explanation": "No relevant information found in the uploaded report."
            }

        # --------------------------------------------------
        # Limit Context Size
        # --------------------------------------------------

        MAX_CHUNKS = 12

        contexts = contexts[:MAX_CHUNKS]

        # --------------------------------------------------
        # Merge Context
        # --------------------------------------------------

        context = "\n\n-----------------------------\n\n".join(
            contexts
        )

        print("=" * 80)
        print("Chunks Sent To LLM :", len(contexts))
        print("Context Length :", len(context))
        print("=" * 80)
                # --------------------------------------------------
        # Ask LLM
        # --------------------------------------------------

        response = await asyncio.to_thread(
            rag_chain.invoke,
            {
                "context": context,
                "question": question,
            },
        )

        print("=" * 80)
        print("LLM RESPONSE")
        print("=" * 80)
        print(response.content)
        print("=" * 80)

        return {
            "diagnosis": response.content.strip(),
            "sources": sorted(list(sources)),
            "context_chunks": len(contexts),
        }

    except Exception as e:

        print("=" * 80)
        print("ERROR OCCURRED")
        print(type(e).__name__)
        print(str(e))
        print("=" * 80)

        return {
            "diagnosis": None,
            "sources": [],
            "context_chunks": 0,
            "explanation": str(e),
        }