Here is a template for your GitHub README file based on the provided code:

---

# Problem Categorization API

## Overview

The **Problem Categorization API** is a web service designed to categorize user-submitted problems and recommend mentors or coaches based on those categories. It leverages the **Ollama** AI model to analyze the descriptions provided by users and categorize them into predefined categories such as **Software Development**, **Hardware Issues**, **AI & Machine Learning**, **Business & Management**, and others.

## Features

- Categorizes problems into predefined categories using the Ollama AI model.
- Recommends mentors and coaches based on the problem category.
- Provides easy integration for categorization into your own applications.
- Interactive front-end interface for testing problem categorization.

## Categories

The available categories for categorization are:

- Software Development
- Hardware Issues
- Networking & Security
- AI & Machine Learning
- Business & Management
- Education & Tutoring
- Healthcare & Medicine
- Legal & Compliance
- Finance & Accounting
- Uncategorized

## Mentors & Coaches

Each category is linked with a relevant mentor or coach:

- **Mentors** provide guidance in the form of expert advice and tutoring.
- **Coaches** specialize in supporting personal and professional development within specific areas.

## API Endpoints

### 1. `/`

A health check endpoint that returns a welcome message and ASCII art in HTML format. This is the default endpoint that serves as an introduction to the Problem Categorization API.

#### Example Response:
```html
<!DOCTYPE html>...
```

### 2. `/mentor_categorize`

This endpoint receives a problem description, categorizes it using Ollama AI, and assigns a relevant mentor based on the category.

#### Method: `POST`

#### Request Body:
```json
{
  "description": "Your problem description here"
}
```

#### Example Response:
```json
{
  "category": "Software Development",
  "mentor": "Alice - Expert in Python, Java, and Web Dev"
}
```

### 3. `/coach_categorize`

This endpoint receives a problem description, categorizes it using Ollama AI, and assigns a relevant coach based on the category.

#### Method: `POST`

#### Request Body:
```json
{
  "description": "Your problem description here"
}
```

#### Example Response:
```json
{
  "category": "Business & Management",
  "coach": "Liam - Leadership and business coach"
}
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/problem-categorization-api.git
cd problem-categorization-api
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
uvicorn main:app --host 127.0.0.1 --port 4100 --reload
```

The API will be available at `http://127.0.0.1:4100/`.

## Front-End Interface

A simple interactive front-end interface is available at the root endpoint `/`. This allows users to enter problem descriptions and see categorized results in real-time.

## Dependencies

- **FastAPI**: Web framework for building APIs.
- **Uvicorn**: ASGI server for running the FastAPI app.
- **requests**: For making API calls to Ollama for categorization.
- **pydantic**: Data validation for API request and response bodies.

