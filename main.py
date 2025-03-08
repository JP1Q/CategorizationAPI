from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests
import uvicorn

# Ollama API URL
OLLAMA_API = "http://127.0.0.1:11434/api/generate"

# FastAPI instance
app = FastAPI(
    title="Problem Categorization API",
    description="API for categorizing problems and matching mentors or coaches using Ollama",
    version="0.0.1"
)

# System Prompt for AI Categorization
SYSTEM_PROMPT = """
You are an AI assistant that categorizes user-submitted problems into predefined categories. 

### Instructions:
1. **Read the problem description** carefully and determine the most relevant category.
2. **Return only the category name(s)**, separated by commas if there are multiple relevant categories, without any explanations or extra text.
3. If the problem fits multiple categories, choose the most specific one.
4. If no category fits, return "Uncategorized".

### Available Categories:
- Software Development
- Hardware Issues
- Networking & Security
- AI & Machine Learning
- Business & Management
- Education & Tutoring
- Healthcare & Medicine
- Legal & Compliance
- Finance & Accounting
- Uncategorized (if none apply)
"""

# Mentor and Coach mapping
MENTOR_MAPPING = {
    "Software Development": "Alice - Expert in Python, Java, and Web Dev",
    "Hardware Issues": "Bob - PC building and troubleshooting expert",
    "Networking & Security": "Charlie - Cybersecurity and network engineer",
    "AI & Machine Learning": "Diana - AI researcher and ML engineer",
    "Business & Management": "Emma - Business consultant and startup advisor",
    "Education & Tutoring": "Frank - Teaching specialist in STEM subjects",
    "Healthcare & Medicine": "Grace - Doctor and medical advisor",
    "Legal & Compliance": "Henry - Corporate lawyer and compliance expert",
    "Finance & Accounting": "Ivy - Chartered accountant and financial planner",
    "Uncategorized": "No mentor available"
}

COACH_MAPPING = {
    "Software Development": "Jake - Agile coach for software teams",
    "Business & Management": "Liam - Leadership and business coach",
    "Education & Tutoring": "Sophia - Academic performance coach",
    "Healthcare & Medicine": "Olivia - Wellness and mental health coach",
    "Finance & Accounting": "Ethan - Financial independence coach",
    "Uncategorized": "No coach available"
}

# Pydantic model for request validation
class ProblemRequest(BaseModel):
    description: str

CAT_ASCII_ART = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome to the Problem Categorization API</title>
  <style>
    body {
      margin: 0;
      font-family: monospace;
      background-color: #000;
      color: #fff;
      text-align: center;
      padding: 50px;
    }
    /* Fullscreen canvas for particles.js */
    #particles-js {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: -1;
      background-color: #000;
    }
    .container {
      display: inline-block;
      text-align: left;
      max-width: 600px;
      border: 3px solid #fff;
      padding: 30px;
      background-color: rgba(0, 0, 0, 0.8);
      position: relative;
      z-index: 1;
    }
    h1, h2 {
      color: #fff;
      margin: 10px 0;
      text-transform: uppercase;
    }
    pre {
      margin: 20px 0;
      font-size: 16px;
    }
    ul {
      list-style-type: none;
      padding: 0;
    }
    li {
      margin: 5px 0;
    }
    button.example, button.run, button.docs {
      background-color: #fff;
      color: #000;
      border: 3px solid #fff;
      padding: 10px 20px;
      text-transform: uppercase;
      font-weight: bold;
      font-size: 14px;
      letter-spacing: 1px;
      margin: 5px 0;
      cursor: pointer;
      transition: background-color 0.2s, color 0.2s;
      width: 100%;
    }
    button.example:hover, button.run:hover, button.docs:hover {
      background-color: #000;
      color: #fff;
    }
    textarea {
      width: 100%;
      font-family: monospace;
      font-size: 14px;
      background-color: #000;
      color: #fff;
      border: 3px solid #fff;
      padding: 10px;
      margin-top: 10px;
      box-sizing: border-box;
    }
    #result {
      margin-top: 20px;
      background-color: #000;
      border: 3px solid #fff;
      padding: 10px;
      white-space: pre-wrap;
      color: #fff;
      font-family: monospace;
    }
  </style>
</head>
<body>
  <div id="particles-js"></div>
  <div class="container">
    <h1>Welcome to the Problem Categorization API</h1>
    <pre>
  /\\_/\\  
 ( o.o ) 
  > ^ <
    </pre>
    <h2>Example Prompts</h2>
    <ul>
      <li>
        <button class="example" onclick="setPrompt('I am having trouble debugging my Python web application.')">
          Debugging Python Web App
        </button>
      </li>
      <li>
        <button class="example" onclick="setPrompt('My computer isn’t booting properly after a recent update.')">
          Computer Not Booting
        </button>
      </li>
      <li>
        <button class="example" onclick="setPrompt('I need advice on how to secure my home network.')">
          Secure Home Network
        </button>
      </li>
      <li>
        <button class="example" onclick="setPrompt('Looking for insights on AI and machine learning trends.')">
          AI & Machine Learning Trends
        </button>
      </li>
      <li>
        <button class="example" onclick="setPrompt('I require help with legal compliance for my business.')">
          Legal Compliance Advice
        </button>
      </li>
    </ul>
    <h2>Try It Out</h2>
    <textarea id="promptInput" rows="4" placeholder="Enter your problem description..."></textarea><br>
    <button class="run" onclick="runPrompt()">Run Prompt</button>
    <button class="docs" onclick="window.open('/docs', '_blank')">Check Documentation</button>
    <div id="result"></div>
  </div>
  <!-- Load particles.js from CDN -->
  <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
  <script>
    // Initialize particles.js with a configuration for white stars
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 80,
          "density": { "enable": true, "value_area": 800 }
        },
        "color": { "value": "#ffffff" },
        "shape": {
          "type": "circle",
          "stroke": { "width": 0, "color": "#000000" }
        },
        "opacity": { "value": 1, "random": false },
        "size": { "value": 2, "random": true },
        "line_linked": { "enable": false },
        "move": {
          "enable": true,
          "speed": 0.5,
          "direction": "none",
          "random": false,
          "straight": false,
          "out_mode": "out",
          "bounce": false
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": { "enable": true, "mode": "repulse" },
          "onclick": { "enable": true, "mode": "push" },
          "resize": true
        },
        "modes": {
          "repulse": { "distance": 100, "duration": 0.4 },
          "push": { "particles_nb": 4 }
        }
      },
      "retina_detect": true
    });
    
    function setPrompt(text) {
      document.getElementById('promptInput').value = text;
    }
    
    async function runPrompt() {
      var promptText = document.getElementById('promptInput').value;
      var resultDiv = document.getElementById('result');
      resultDiv.innerHTML = 'Running...';
      try {
        var response = await fetch('/mentor_categorize', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ description: promptText })
        });
        var data = await response.json();
        resultDiv.innerHTML = 'Response:\\n' + JSON.stringify(data, null, 2);
      } catch (error) {
        resultDiv.innerHTML = 'Error: ' + error;
      }
    }
  </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse, tags=["General"])
def index():
    """Health check endpoint that returns a welcome message and ASCII art in HTML format."""
    return HTMLResponse(content=CAT_ASCII_ART, status_code=200)

# Function to handle multiple categories in response
def get_most_relevant_category(categories):
    # Split categories by commas and strip extra spaces
    category_list = [category.strip() for category in categories.split(',')]
    
    # Select the most relevant category (the first in the list)
    if category_list:
        return category_list[0]
    return "Uncategorized"

# Categorization for mentors
@app.post("/mentor_categorize", tags=["Categorization"])
def categorize_mentor(problem: ProblemRequest):
    """Receives a problem description, categorizes it, and assigns a mentor."""
    payload = {
        "model": "mistral",  # Use "mistral", "gemma", or your custom model
        "prompt": f"{SYSTEM_PROMPT}\n\nUser Problem: {problem.description}\nCategory:",
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API, json=payload)
        response.raise_for_status()  # Ensure no errors from API

        # Get category from response
        categories = response.json().get("response", "Uncategorized").strip()
        category = get_most_relevant_category(categories)  # Handle multiple categories
        mentor = MENTOR_MAPPING.get(category, "No mentor available")

        return {
            "category": category,
            "mentor": mentor
        }

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to AI model: {str(e)}")

# Categorization for coaches
@app.post("/coach_categorize", tags=["Categorization"])
def categorize_coach(problem: ProblemRequest):
    """Receives a problem description, categorizes it, and assigns a coach."""
    payload = {
        "model": "mistral",  # Use "mistral", "gemma", or your custom model
        "prompt": f"{SYSTEM_PROMPT}\n\nUser Problem: {problem.description}\nCategory:",
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API, json=payload)
        response.raise_for_status()  # Ensure no errors from API

        # Get category from response
        categories = response.json().get("response", "Uncategorized").strip()
        category = get_most_relevant_category(categories)  # Handle multiple categories
        coach = COACH_MAPPING.get(category, "No coach available")

        return {
            "category": category,
            "coach": coach
        }

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to AI model: {str(e)}")

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4100, reload=True)
