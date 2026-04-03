# LinkedIn AI Factory Project

Welcome to the **LinkedIn AI Factory**! This project is a complete full-stack application that leverages advanced AI agents (using CrewAI and Groq API) to seamlessly research specific technology topics and generate professional, formatted LinkedIn posts—along with corresponding AI-generated image prompts!

This is built using:
- **Backend:** Python, FastAPI, and CrewAI
- **Frontend:** React and TailwindCSS

## 🚀 How to Set Up the Project Locally

Follow these step-by-step instructions to clone, set up, and run this application on your computer.

### Step 1: Clone the Repository
Open your terminal or command prompt and download the project to your local machine by running:
```bash
git clone https://github.com/tharindudhananjayaekanayaka-hub/linkdin_post_project.git
cd linkdin_post_project
```

### Step 2: Set Up the Backend (Python FastAPI)
The AI magic happens in the backend. You need to set up a Python virtual environment to run it.

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - **Windows:** 
     ```bash
     .\venv\Scripts\activate
     ```
   - **Mac/Linux:** 
     ```bash
     source venv/bin/activate
     ```
4. Install all required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up the Environment Variables:
   - Create a file named `.env` inside the `backend` folder.
   - Add the following keys inside the file:
     ```env
     GROQ_API_KEY=your_groq_api_key_here
     SERPER_API_KEY=your_serper_api_key_here
     ```
   *(You can obtain a Groq API key from [Groq Console](https://console.groq.com/) and a Serper API key from [Serper.dev](https://serper.dev/)).*

6. Start the Backend Server:
   ```bash
   python main.py
   ```
   *(The backend server will launch and listen on `http://127.0.0.1:8000`)*

### Step 3: Set Up the Frontend (React Application)
The frontend provides the user interface to interact with the AI logic. Open a **new, separate terminal window** (keep your backend running).

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the Node.js packages using npm:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open the link provided in your terminal (usually `http://localhost:5173` or `http://localhost:3000`) in your browser to interact with the LinkedIn AI Factory!

---

## 💡 How It Works
1. You input a **Topic** and desired **Language** (e.g. "English" or "Sinhala") in the frontend screen.
2. The **Researcher Agent** searches Google for the latest news on your topic and grabs recent technical summaries.
3. The **Content Strategist Agent** drafts a well-formatted LinkedIn post utilizing emojis, hashtags, bullet points, and a Call-To-Action.
4. The application returns the complete text, alongside an AI image generated perfectly to match your content!

Enjoy building with AI!
