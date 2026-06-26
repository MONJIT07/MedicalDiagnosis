# 🩺 AI-Powered Medical Diagnosis System using RAG

> An end-to-end AI-powered medical diagnosis platform that leverages Retrieval-Augmented Generation (RAG), Google Gemini Embeddings, Pinecone Vector Database, and FastAPI to provide intelligent medical report analysis.

# 📌 Overview

Medical reports often contain complex clinical terminology that can be difficult to interpret. This project uses **Retrieval-Augmented Generation (RAG)** to intelligently analyze uploaded medical reports and generate context-aware responses using Google's Gemini models.

The application converts uploaded PDF reports into semantic embeddings, stores them in Pinecone Vector Database, retrieves the most relevant medical information, and uses Large Language Models (LLMs) to assist in diagnosis and report understanding.

---

# ✨ Features

* 🔐 User Authentication
* 📄 Upload Medical Reports (PDF)
* 📚 Automatic PDF Text Extraction
* ✂ Intelligent Text Chunking
* 🧠 Google Gemini Embeddings
* ⚡ Pinecone Vector Database
* 🗄 MongoDB Metadata Storage
* 🔍 Semantic Search
* 🤖 AI-powered Diagnosis using RAG
* ⚙ REST APIs with FastAPI
* 📈 Scalable Vector Search Architecture

---

# 🏗 System Architecture

```text
                  User
                    │
                    ▼
          Upload Medical Report
                    │
                    ▼
             FastAPI Backend
                    │
                    ▼
          PDF Text Extraction
                    │
                    ▼
      Recursive Text Chunking
                    │
                    ▼
      Google Gemini Embeddings
                    │
                    ▼
      Pinecone Vector Database
                    │
                    ▼
      Semantic Similarity Search
                    │
                    ▼
     Retrieved Medical Context
                    │
                    ▼
      Gemini Large Language Model
                    │
                    ▼
          AI Diagnosis Response
```

---

# 🛠 Tech Stack

## Backend

* FastAPI
* Python 3.13
* AsyncIO

## Artificial Intelligence

* Google Gemini
* Google Gemini Embeddings
* LangChain
* Retrieval-Augmented Generation (RAG)

## Databases

* MongoDB
* Pinecone Vector Database

## Document Processing

* PyPDFLoader
* RecursiveCharacterTextSplitter

## Development Tools

* Uvicorn
* Postman
* Git
* GitHub
* VS Code

---

# 📂 Project Structure

```text
MedicalDiagnosis/
│
├── server/
│   ├── auth/
│   │   ├── hash_utils.py
│   │   ├── models.py
│   │   └── route.py
│   │
│   ├── reports/
│   │   ├── route.py
│   │   └── vectorstore.py
│   │
│   ├── diagnosis/
│   │   ├── query.py
│   │   └── route.py
│   │
│   ├── config/
│   │   └── db.py
│   │
│   ├── models/
│   │   └── db_models.py
│   │
│   └── main.py
│
├── uploaded_reports/
├── requirements.txt
├── README.md
└── .env
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/MONJIT07/MedicalDiagnosis.git
```

Move into the project

```bash
cd MedicalDiagnosis
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirement.txt
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY

PINECONE_API_KEY=YOUR_PINECONE_API_KEY

PINECONE_ENVIRONMENT=us-east-1

PINECONE_INDEX_NAME=medicaldiagnosis

MONGODB_URI=YOUR_MONGODB_CONNECTION_STRING
```

---

# ▶ Running the Application

```bash
uvicorn server.main:app --reload
```

Open API documentation

```text
http://127.0.0.1:8000/docs
```

---

# 📡 API Endpoints

## Authentication

| Method | Endpoint       | Description         |
| ------ | -------------- | ------------------- |
| POST   | /auth/register | Register a new user |
| POST   | /auth/login    | User Login          |

## Reports

| Method | Endpoint        | Description           |
| ------ | --------------- | --------------------- |
| POST   | /reports/upload | Upload Medical Report |

## Diagnosis

| Method | Endpoint         | Description        |
| ------ | ---------------- | ------------------ |
| POST   | /diagnosis/query | AI Diagnosis Query |

---

# 🔄 Workflow

1. User uploads a medical report.
2. PDF text is extracted.
3. Text is divided into semantic chunks.
4. Google Gemini generates embeddings.
5. Embeddings are stored in Pinecone.
6. Metadata is stored in MongoDB.
7. User asks a diagnosis-related question.
8. Relevant chunks are retrieved.
9. Gemini generates a context-aware medical response.

---

# 📈 Future Enhancements

* Streamlit Frontend
* JWT Authentication
* Role-Based Access Control (RBAC)
* Medical Chatbot
* Multi-document Support
* Conversation Memory
* Patient Dashboard
* Doctor Dashboard
* Docker Deployment
* CI/CD Pipeline
* AWS Deployment

---

# 📸 Demo

> Demo screenshots and walkthrough video will be added soon.

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

### Monjit Tamuli

**B.Tech, Electrical Engineering**

National Institute of Technology Silchar

* GitHub: https://github.com/MONJIT07

---

⭐ If you found this project helpful, consider giving it a star!
