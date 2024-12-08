## Setup

1. Clone the repository:
```bash
git clone <your-repository-url>
cd food_ordering_chatbot
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  
# On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
# if satisfied dependencies are not install by requirements.txt file
pip install streamlit langchain langchain-community python-dotenv openai
```

4. Create .env file with your OpenAI API key:
```
OPENAI_API_KEY=your_key_here
```

5. Run the application:
```bash
streamlit run src/frontend/app.py
```