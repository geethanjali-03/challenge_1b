## Challenge 1B - AI-Powered Document Understanding Solution

This repository contains the complete solution for Challenge 1B of the [Adobe India Hackathon 2025 / similar event]. It demonstrates how to extract structured insights from a set of input documents using large language models (LLMs) and supporting libraries.
## Problem Statement

The task is to build an intelligent system that:

    Accepts multiple PDF documents and a persona (e.g., Travel Planner, Student, Researcher).

    Extracts relevant sections based on the persona’s needs.

    Returns a structured JSON output containing metadata, input document references, relevant sections, and subsection analyses.

##  Project Structure

Challenge_1b/
├── input/                  # Folder containing persona.txt and PDF documents
├── output/                 # Folder containing result.json
├── models/                 # Pretrained models (if any)
├── src/                    # Source code for processing
│   ├── main.py             # Main script to run the pipeline
│   ├── extractor.py        # Code for section/subsection extraction
│   ├── utils.py            # Helper functions
│   └── config.py           # Configuration and parameters
├── requirements.txt        # Python dependencies
└── README.md               # Documentation

## Libraries Used                     Library Purpose
PyMuPDF (fitz) or pdfplumber	    Extract text and metadata from PDF documents
transformers	                    Use pre-trained language models like BERT, T5, or GPT
openai	                            Interface with OpenAI models (e.g., GPT-3.5, GPT-4) if using API
langchain	                    (Optional) Chaining LLM operations and memory
llama-index	                    (Optional) Indexing PDFs and querying them using LLMs
tqdm	                            Visual progress bars for loops or processing tasks
json	                            Parse and write JSON output
os, re, glob	                    File handling, regex matching, and file discovery
datetime	                    Add timestamps in output metadata
argparse	                    Handle command-line arguments (if applicable)
typing	                            Support static typing for better code structure
dotenv	                            Load API keys and secrets securely from .env files
