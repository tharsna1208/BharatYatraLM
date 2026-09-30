# BharatYatraLM

## AI-Powered India Tourism Assistant

BharatYatraLM is an AI-powered tourism assistant designed specifically for exploring India.

It combines a compact domain-focused Transformer language model trained from scratch with Retrieval-Augmented Generation (RAG), semantic retrieval, personalized recommendations, geospatial intelligence, and itinerary generation.

The system allows users to ask natural-language travel questions and receive tourism-focused responses based on a structured India tourism dataset.

## Live Demo

https://bharatyatralm.onrender.com

## Overview

Traditional tourism applications usually provide predefined search and recommendation features.

BharatYatraLM focuses on natural-language interaction.

A user can ask questions such as:

- "Plan a 4 day trip to Goa for a couple who love culture"
- "Recommend peaceful beach destinations"
- "What places are near Goa?"
- "What should I explore in Goa?"
- "Plan a trip to Hampi"
- "What can I do in Manali?"

The system identifies the user's intent and routes the request to the appropriate tourism intelligence module.

## Key Features

### AI Tourism Chatbot

Natural-language tourism interaction through a FastAPI-powered chatbot.

The chatbot supports:

- General tourism questions
- Destination exploration
- Trip planning
- Destination recommendations
- Nearby destination discovery
- Personalized itineraries
- Conversational interactions

### Transformer Language Model

BharatYatraLM includes a compact decoder-only Transformer language model trained from scratch.

Model architecture:

- Decoder-only Transformer
- 4 Transformer blocks
- 4 attention heads
- Embedding dimension: 128
- Feed-forward dimension: 512
- Context length: 128
- GELU activation
- Layer normalization
- Random initialization
- Domain-focused tourism training corpus

The model is intentionally compact so that the project can be developed and experimented with on CPU-based hardware.

It is not intended to compete with large foundation models. Instead, it demonstrates the complete process of building and training a small domain-focused language model from scratch.

## Model Training

The model was trained using a tourism-focused corpus with a train/validation split.

Training progression included multiple iterations of:

- Dataset cleaning
- Vocabulary refinement
- Train/validation splitting
- Model training
- Validation
- Perplexity evaluation
- Generation testing

Final held-out validation perplexity:

**~67.50**

The model is combined with retrieval-based components to ground tourism information in structured data.

## Retrieval-Augmented Generation

BharatYatraLM uses a RAG pipeline to improve factual tourism responses.

The retrieval pipeline:

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
