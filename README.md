# BharatYatraLM

## AI-Powered India Tourism Assistant

BharatYatraLM is an AI-powered tourism assistant built specifically for exploring India.

It combines a compact domain-focused Transformer language model trained from scratch with Retrieval-Augmented Generation (RAG), semantic retrieval, personalized recommendations, geospatial intelligence, and itinerary generation.

The system allows users to interact with India tourism information using natural language.

## Live Demo

https://bharatyatralm.onrender.com

## What Can BharatYatraLM Do?

Users can ask questions such as:

- Plan a 4 day trip to Goa for a couple who love culture
- Recommend peaceful beach destinations
- What places are near Goa?
- What should I explore in Goa?
- Plan a trip to Hampi
- What can I do in Manali?

BharatYatraLM identifies the user's request and routes it to the appropriate tourism intelligence component.

## Project Highlights

- AI-powered tourism chatbot
- Compact Transformer language model trained from scratch
- Retrieval-Augmented Generation
- Semantic retrieval
- Personalized destination recommendations
- Personalized itineraries
- Geospatial nearby-destination search
- Natural-language intent detection
- FastAPI backend
- Interactive web frontend
- Voice input
- Production deployment on Render

## Key Features

### 1. AI Tourism Chatbot

BharatYatraLM provides a natural-language chatbot for India tourism.

It can handle:

- General tourism questions
- Destination exploration
- Trip planning
- Destination recommendations
- Nearby destination discovery
- Personalized itineraries
- Basic conversation

### 2. Trip Planning

Users can provide:

- Destination
- Number of days
- Traveler type
- Interests

The system uses this information to create a personalized itinerary.

Example:

"Plan a 4 day trip to Goa for a couple who love culture"

### 3. Destination Recommendations

The recommendation system finds destinations based on user preferences.

It considers factors such as:

- Travel interests
- Trip duration
- Budget
- Destination similarity

### 4. Personalized Travel

BharatYatraLM supports different traveler types:

- Solo
- Couple
- Friends
- Family with kids
- Family with elderly travelers

The system adapts recommendations and itineraries according to the traveler's preferences.

### 5. Nearby Destination Discovery

Users can ask for destinations near a particular location.

The system calculates approximate geographic distances and returns nearby tourism destinations.

### 6. Voice Input

The frontend supports browser-based voice input so users can interact with the tourism assistant using their voice.

## AI and Machine Learning

### Compact Transformer Language Model

BharatYatraLM includes a compact decoder-only Transformer language model trained from scratch.

The model was designed to learn tourism-focused language patterns from the project's training corpus.

### Model Architecture

- Decoder-only Transformer
- 4 Transformer blocks
- 4 attention heads
- Embedding dimension: 128
- Feed-forward dimension: 512
- Context length: 128
- GELU activation
- Layer normalization
- Random initialization
- Word-level tokenizer

The model is intentionally compact so that it can be trained and experimented with using CPU-based hardware.

The goal is not to build a large foundation model, but to demonstrate the complete process of building and training a small domain-focused language model.

### Model Training

The training process included:

- Dataset preparation
- Text cleaning
- Vocabulary construction
- Tokenization
- Train/validation split
- Transformer training
- Validation
- Perplexity evaluation
- Text generation testing

The final held-out validation perplexity achieved during training was approximately:

**67.50**

### Why a Small Model?

The project was developed on consumer hardware without an NVIDIA GPU.

A compact architecture makes it possible to experiment with:

- Transformer architecture
- Language model training
- Tokenization
- Evaluation
- Text generation

while keeping the system practical for CPU-based development.

### AI Architecture

BharatYatraLM does not depend on only one AI component.

Instead, multiple components work together:

```text
User
 |
 v
Chat Interface
 |
 v
Intent Detection
 |
 +-------------------+
 |         |         |
 v         v         v
RAG    Recommendation  Itinerary
 |         |         |
 v         v         v
Tourism Knowledge Base
 |
 v
Tourism Response

## Retrieval-Augmented Generation

BharatYatraLM uses Retrieval-Augmented Generation (RAG) to ground tourism responses in structured tourism knowledge.

Instead of depending only on the language model, the system retrieves relevant tourism information and uses it to construct the response.

### RAG Pipeline

```text
User Query
     |
     v
Query Processing
     |
     v
Semantic Retrieval
     |
     v
Relevant Tourism Knowledge
     |
     v
Answer Construction
     |
     v
Tourism Response

## Geospatial Intelligence

BharatYatraLM includes a geospatial intelligence module for discovering destinations near another destination.

The system uses geographic coordinates and the Haversine distance formula to calculate approximate distances between destinations.

Example:

```text
Goa
 |
 +-- Hidden Goa Coves
 +-- Amboli Ghat
 +-- Gokarna
 +-- Maravanthe
 +-- Agumbe

## Tourism Dataset

BharatYatraLM uses a structured India tourism dataset as its main tourism knowledge source.

The dataset contains:

- 100 destinations
- 459 tourist spots
- 30 states
- 78 districts
- 9 regions
- 54 destination-related fields

The dataset contains information such as:

- Destination name
- State
- District
- Region
- Geographic coordinates
- Popularity
- Accessibility
- Transportation
- Budget
- Trip types
- Attractions
- Activities
- Unique experiences
- Hidden gems
- Seasons
- Weather
- Traveler suitability
- Suggested trip duration
- Suggested itinerary
- Accommodation
- Food
- Safety
- Connectivity
- Language
- Culture
- Festivals
- Shopping
- Cuisine
- Sustainability
- Tourism developments

## Technology Stack

### Programming

- Python

### Machine Learning and NLP

- PyTorch
- Transformers
- Scikit-learn
- NumPy
- Pandas
- Sentence Transformers

### Backend

- FastAPI
- Uvicorn
- Pydantic

### Frontend

- HTML
- CSS
- JavaScript
- Browser Voice Input

### Deployment

- Render

### Version Control

- Git
- GitHub

## Project Structure

```text
BharatYatraLM
│
├── api/
│   ├── main.py
│   ├── router.py
│   ├── request_handler.py
│   ├── request_parser.py
│   └── schemas.py
│
├── data/
│   ├── india_tourism_dataset.json
│   ├── dataset_schema.json
│   ├── Tourist_Spots.csv
│   ├── geo_utils.py
│   ├── geospatial_engine.py
│   ├── geo_personalized_recommendation.py
│   └── itinerary_engine.py
│
├── rag/
│   ├── rag_chatbot.py
│   └── recommendation_engine.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── notebooks/
│   └── features.csv
│
├── models/
│
├── tokenizer/
│
├── requirements.txt
│
└── README.md

## API Endpoints

BharatYatraLM provides a FastAPI backend for interacting with the tourism intelligence system.

### Health Check

```text
GET /health

## Hardware and Performance

BharatYatraLM was developed and tested on CPU-based hardware without an NVIDIA GPU.

Because of the available hardware, the project focuses on:

- Compact Transformer architecture
- Lightweight retrieval
- Efficient recommendation logic
- Structured tourism knowledge
- CPU-compatible development
- Modular AI components

The compact architecture makes it practical to experiment with the system on consumer hardware.

## Limitations

BharatYatraLM is a project-scale tourism AI system and has some limitations.

- The Transformer language model is intentionally small.
- The tourism dataset does not cover every destination in India.
- Tourism information depends on the available dataset.
- Real-time hotel, flight, weather, traffic, and booking information is not currently integrated.
- Geographic distances are approximate.
- Recommendations are based on the available tourism information.
- Important travel decisions should be verified using current official information.

## Future Improvements

Future versions could include:

- A larger tourism training corpus
- A larger domain-specific language model
- Multilingual Indian-language support
- Real-time weather integration
- Hotel and flight APIs
- Live maps integration
- Booking integrations
- More advanced conversational memory
- User accounts and saved trips
- Mobile application
- Improved hallucination evaluation
- Tourism knowledge graphs
- Real-time destination information
- Multimodal tourism assistance

## What I Learned

Building BharatYatraLM provided practical experience in developing an end-to-end AI application.

The project involved:

- Transformer architecture
- Language model training
- Tokenization
- Model evaluation
- Perplexity
- Semantic retrieval
- Retrieval-Augmented Generation
- NLP intent detection
- Recommendation systems
- Personalization
- Geospatial algorithms
- FastAPI development
- Frontend integration
- Voice input
- Production deployment
- Deployment debugging
- Git and GitHub workflows

## Project Goal

The goal of BharatYatraLM is to explore how domain-specific AI systems can combine language models, structured knowledge, retrieval, recommendation systems, personalization, and geospatial intelligence to create a practical tourism assistant.

Instead of relying on a single AI component, the project demonstrates how multiple AI technologies can work together as one end-to-end system.

## Project Status

**Completed and Deployed**

Live application:

https://bharatyatralm.onrender.com

## Author

**Tharun K**

AI / ML Developer

Built with Python, PyTorch, FastAPI, NLP, RAG, Recommendation Systems, Personalization, and Geospatial Intelligence.
