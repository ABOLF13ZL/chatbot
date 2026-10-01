# NeliShop AI Product Assistant

A simple AI-powered product assistant for an online store, built with Python and an LLM API.

The chatbot can answer product-related questions using real product information stored in a JSON file, while reducing the risk of hallucinating product details such as price, stock, and product code.

## Features

* 🤖 LLM-powered conversational chatbot
* 🛍️ Product lookup by product code
* 🔎 Product lookup by product name
* 💬 Natural-language product questions
* 📦 Product information from a local JSON file
* 🧠 Product context provided to the LLM
* 🛡️ Prevents the model from inventing unavailable product information
* 💾 Conversation history
* 🧹 Clear conversation history
* 📊 Conversation statistics
* 🆘 Built-in help command
* ❌ Graceful handling of API errors

## Commands

| Command           | Description                  |
| ----------------- | ---------------------------- |
| `/help`           | Show available commands      |
| `/clear`          | Clear conversation history   |
| `/history`        | Show conversation history    |
| `/stats`          | Show conversation statistics |
| `/product <code>` | Get a product by its code    |
| `/q`              | Exit the chatbot             |

## Example

The user can ask questions such as:

```text
What is N005's price?
```

or:

```text
What is shal toori's price?
```

The chatbot retrieves the corresponding product information from `products.json` and provides it to the LLM as context.

Example response:

```text
The price of the shal toori is 250,000.
```

If the requested product does not exist, the chatbot does not invent product information.

```text
What is N999's price?

I'm sorry, but I don't have any information about a product with the code N999.
```

## Project Structure

```text
NeliShop/
│
├── chatbot.py
├── data/
│   └── products.json
├── .env
├── .gitignore
└── README.md
```

## Technologies

* Python
* OpenAI Python SDK
* Groq API
* JSON
* pathlib
* python-dotenv
* Object-Oriented Programming (OOP)

## How It Works

The basic flow of the application is:

```text
User Question
      ↓
Product Code / Name Extraction
      ↓
ProductManager
      ↓
products.json
      ↓
Product Context
      ↓
LLM
      ↓
Assistant Response
```

The product information is retrieved locally instead of asking the LLM to guess product details.

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_api_key_here
```

The API key is loaded using `python-dotenv`.

Make sure `.env` is included in `.gitignore` and is never committed to the repository.

## Installation

Clone the repository and install the required packages:

```bash
pip install openai python-dotenv
```

Then configure your `.env` file and run:

```bash
python chatbot.py
```

## Project Purpose

This project was built as a practical Python and AI Engineering project to practice:

* Working with LLM APIs
* Prompting and system instructions
* Managing conversation history
* Object-Oriented Programming
* Reading and processing JSON data
* Connecting deterministic Python logic with an LLM
* Providing external context to an LLM
* Building a small AI-powered application

## Future Improvements

Possible future improvements include:

* Intent detection
* Support for multiple-product queries
* RAG with embeddings and a vector database
* Database integration
* Web/API deployment
* Store website integration
* More advanced product search
