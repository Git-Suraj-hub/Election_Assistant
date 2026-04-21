# 🗳️ Election Intelligence Assistant

Welcome to the **Election Intelligence Assistant**, a modern, interactive, and AI-powered SaaS dashboard designed to help users understand complex democratic processes across different countries in a simple, guided, and highly visual way.

---

## ✨ Key Features

### 💬 1. Context-Aware AI Chat Assistant
Powered by the **Google Gemini API**, this is not just a standard chatbot. It acts as a highly intelligent, contextual tutor.
*   **Adaptive Learning Engine:** Tailors explanations based on the user's chosen "Knowledge Level" (Beginner with analogies, Standard step-by-step, or Advanced with legal terminology).
*   **Contextual Memory:** The AI knows exactly which country's system you are exploring and what tab (Timeline, Simulator, or Chat) you are currently using.
*   **Smart Micro-Interactions:** Automatically includes progress indicators, structured summaries, and optional quick-quizzes.

### 📅 2. Dynamic Election Timeline
A custom CSS-animated, visually polished vertical timeline that breaks down the election sequence.
*   **SaaS Dashboard UI:** Features a sleek, dark-themed layout with glassmorphism cards, glowing neon purple accent markers, and smooth hover animations.
*   **Country Specific:** Automatically updates the timeline phases (e.g., from US Primaries to UK Parliament Dissolution) based on your selection.

### 🗳️ 3. Interactive Voting Simulator
A risk-free sandbox environment where users can practice the exact steps required to cast a ballot.
*   **Step-by-step Guidance:** Walks you through Checking In, Receiving a Ballot, Casting a Vote, and Verification.
*   **Realism Boost:** Accurately reflects country-specific mechanisms (e.g., using EVMs and VVPATs in India vs. Paper Ballots in the UK).

---

## 🎨 UI/UX Design

The application has been completely redesigned into a **Professional SaaS Dashboard**:
*   **Modern Dark Theme:** Utilizes deep background colors (`#0E1117`) with elevated surface cards (`#1E1E2F`).
*   **Neon Purple Accent:** High-contrast `#8B5CF6` highlights for active tabs, buttons, and timeline markers.
*   **Glassmorphism & Polish:** Soft box-shadows, rounded corners (`12px`), gradient text, and CSS-based slide-up animations create a premium user experience.

---

## 🚀 How to Run Locally

### Prerequisites
Make sure you have Python 3.9+ installed and a valid **Google Gemini API Key**.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Election_Assistant.git
   cd Election_Assistant
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App
1. Start the Streamlit server:
   ```bash
   streamlit run app.py
   ```
2. Open your browser and navigate to the local URL (usually `http://localhost:8501`).
3. **Important:** Paste your Google Gemini API key into the secure sidebar input field to activate the AI Chat Assistant.

---

## 🌐 Live Demo

You can try the live version of the application hosted on Streamlit Community Cloud here:

👉 **[Launch Election Intelligence Assistant](https://election-intelligence-assistant.streamlit.app/)** 

*(Note: Replace the link above with your actual deployed Streamlit Community Cloud URL once deployed).*

---

## 🛠️ Tech Stack

*   **Frontend & Framework:** [Streamlit](https://streamlit.io/)
*   **AI Engine:** [Google Generative AI (Gemini 2.5 Flash)](https://ai.google.dev/)
*   **Styling:** Custom injected HTML & CSS (Animations, Dark Theme, Flexbox)
*   **Language:** Python 3

---
*Built with ❤️ to make democracy easier to understand.*
