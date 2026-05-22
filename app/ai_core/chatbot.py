import os
from typing import List, Dict
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# ✅ Load .env from project root (IMPORTANT!)
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

from google import genai
from google.genai import types


class AdvancedHealthChatbot:
    """
    Advanced AI Health Chatbot
    - Uses Gemini (google-genai SDK - NEW version)
    - Conversation memory
    - Symptom severity detection
    - Safety-first responses
    """

    # Critical symptoms (emergency)
    CRITICAL_SYMPTOMS = [
        "chest pain", "heart attack", "stroke", "severe bleeding",
        "difficulty breathing", "unconscious", "seizure",
        "poisoning", "overdose", "choking",
        "severe allergic reaction", "anaphylaxis",
        "suicide", "self harm"
    ]

    # Medium severity symptoms
    MEDIUM_SEVERITY = [
        "persistent fever", "blood in stool", "blood in urine",
        "severe headache", "vision loss", "hearing loss",
        "dizziness", "severe pain", "infection",
        "swelling", "rash", "vomiting blood"
    ]

    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("❌ GOOGLE_API_KEY not set in environment variables")

        # ✅ Initialize client with new google-genai SDK
        self.client = genai.Client(api_key=api_key)

        # Conversation memory
        self.conversations: Dict[str, List[Dict]] = {}
        
        # Available models - will be populated on first use
        self.available_models = None
        
        print("✅ HealthAI Chatbot initialized successfully")

    # --------------------------------------------------
    # INTERNAL HELPERS
    # --------------------------------------------------

    def _system_prompt(self) -> str:
        return (
            "You are HealthAI, a helpful and empathetic AI health assistant.\n\n"
            "IMPORTANT RULES:\n"
            "- Do NOT diagnose diseases or medical conditions\n"
            "- Do NOT prescribe medication or treatments\n"
            "- Always encourage consulting with qualified healthcare professionals\n"
            "- Be empathetic, clear, and supportive\n"
            "- Provide general health information and wellness tips\n"
            "- If symptoms seem serious, urge immediate medical attention\n\n"
            "Your role is to provide helpful health information and guidance, "
            "not to replace professional medical advice.\n"
        )

    def _detect_severity(self, text: str) -> str:
        """Detect severity level of symptoms mentioned"""
        text = text.lower()
        if any(s in text for s in self.CRITICAL_SYMPTOMS):
            return "critical"
        if any(s in text for s in self.MEDIUM_SEVERITY):
            return "medium"
        return "low"

    def _add_history(self, user_id: str, role: str, content: str):
        """Add message to conversation history"""
        self.conversations.setdefault(user_id, []).append({
            "role": role,
            "content": content,
            "time": datetime.now().isoformat()
        })
        # Keep only last 20 messages to manage memory
        self.conversations[user_id] = self.conversations[user_id][-20:]

    def _build_prompt(self, user_id: str, message: str) -> str:
        """Build prompt with conversation history"""
        history = self.conversations.get(user_id, [])
        convo = ""
        
        # Include last 10 messages for context
        for h in history[-10:]:
            convo += f"{h['role'].upper()}: {h['content']}\n"

        full_prompt = (
            f"{self._system_prompt()}\n"
            f"CONVERSATION HISTORY:\n{convo}\n"
            f"USER: {message}\n"
            f"ASSISTANT:"
        )
        
        return full_prompt

    def _get_available_models(self) -> List[str]:
        """Fetch and cache available models"""
        if self.available_models is not None:
            return self.available_models
        
        try:
            print("🔍 Fetching available models...")
            models = list(self.client.models.list())
            self.available_models = []
            
            for model in models:
                # Check if model supports generateContent
                if hasattr(model, 'supported_generation_methods'):
                    if 'generateContent' in model.supported_generation_methods:
                        self.available_models.append(model.name)
            
            # Sort to prioritize newer models
            priority_models = [
                'models/gemini-2.5-pro',
                'models/gemini-2.5-flash', 
                'models/gemini-2.0-flash-exp',
                'models/gemini-1.5-pro',
                'models/gemini-1.5-flash',
            ]
            
            # Reorder: priority models first, then others
            sorted_models = []
            for pm in priority_models:
                if pm in self.available_models:
                    sorted_models.append(pm)
                    print(f"  ✅ Found priority model: {pm}")
            
            # Add remaining models
            for m in self.available_models:
                if m not in sorted_models:
                    sorted_models.append(m)
            
            self.available_models = sorted_models if sorted_models else priority_models
            
            return self.available_models
            
        except Exception as e:
            print(f"⚠️ Could not fetch models: {e}")
            # Return default fallback models
            return [
                'models/gemini-2.5-flash',
                'models/gemini-2.5-pro',
                'models/gemini-2.0-flash-exp',
            ]

    # --------------------------------------------------
    # MAIN CHAT METHOD
    # --------------------------------------------------

    def chat(self, message: str, user_id: str = "default") -> Dict:
        """
        Main chat method - processes user message and returns AI response
        
        Args:
            message: User's message/question
            user_id: Unique identifier for user (for conversation history)
            
        Returns:
            Dict with success status, reply, severity level, and warnings
        """
        try:
            # Detect symptom severity
            severity = self._detect_severity(message)
            
            # Add user message to history
            self._add_history(user_id, "user", message)

            # Build prompt with context
            prompt = self._build_prompt(user_id, message)

            print(f"🤖 Processing message from user: {user_id}")
            
            # Get available models
            models_to_try = self._get_available_models()
            
            last_error = None
            
            # Try each model until one works
            for model_name in models_to_try:
                try:
                    print(f"🔄 Trying model: {model_name}")
                    
                    # ✅ Generate response using Gemini
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    
                    # Extract reply text
                    reply = response.text.strip()
                    
                    # Add assistant reply to history
                    self._add_history(user_id, "assistant", reply)

                    # ✅ Generate warning messages based on severity
                    warning = None
                    if severity == "critical":
                        warning = (
                            "⚠️ URGENT: The symptoms you described may be serious. "
                            "Please seek immediate medical attention or call emergency services (911)!"
                        )
                    elif severity == "medium":
                        warning = (
                            "⚠️ IMPORTANT: Please consult with a healthcare professional "
                            "about these symptoms as soon as possible."
                        )

                    print(f"✅ Response generated successfully with {model_name} (severity: {severity})")
                    
                    return {
                        "success": True,
                        "reply": reply,
                        "severity": severity,
                        "requires_doctor": severity in ["critical", "medium"],
                        "warning": warning,
                        "model_used": model_name,
                        "timestamp": datetime.now().isoformat()
                    }
                
                except Exception as e:
                    last_error = e
                    error_msg = str(e)
                    print(f"⚠️ Model {model_name} failed: {error_msg[:100]}...")
                    
                    # Check if we should continue trying
                    if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                        print(f"⏭️ Quota exceeded for {model_name}, trying next...")
                        continue
                    elif "404" in error_msg or "NOT_FOUND" in error_msg:
                        print(f"⏭️ Model {model_name} not found, trying next...")
                        continue
                    else:
                        continue
            
            # All models failed
            print(f"❌ All models failed. Last error: {last_error}")
            error_msg = str(last_error)
            
            # Provide helpful error messages
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                reply = (
                    "I'm experiencing high demand right now. "
                    "Please try again in a few moments. "
                    "If you have urgent health concerns, please consult a healthcare professional immediately."
                )
            elif "API key" in error_msg or "authentication" in error_msg.lower():
                reply = (
                    "There's a configuration issue with the AI service. "
                    "Please contact support. For immediate health concerns, "
                    "please consult a healthcare professional."
                )
            else:
                reply = (
                    "I'm temporarily unable to process your request. "
                    "Please try again later or consult a healthcare professional "
                    "for immediate assistance."
                )
            
            return {
                "success": False,
                "reply": reply,
                "error": error_msg,
                "requires_doctor": True,
                "severity": "unknown",
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Unexpected error: {error_msg}")
            
            return {
                "success": False,
                "reply": (
                    "An unexpected error occurred. "
                    "Please consult a healthcare professional for immediate assistance."
                ),
                "error": error_msg,
                "requires_doctor": True,
                "severity": "unknown",
                "timestamp": datetime.now().isoformat()
            }

    # --------------------------------------------------
    # UTILITY METHODS
    # --------------------------------------------------

    def get_conversation_history(self, user_id: str) -> List[Dict]:
        """Get full conversation history for a user"""
        return self.conversations.get(user_id, [])

    def get_conversation_summary(self, user_id: str) -> str:
        """Get a summary of the conversation"""
        history = self.conversations.get(user_id, [])
        if not history:
            return "No conversation history"
        
        return (
            f"Messages: {len(history)}, "
            f"Last activity: {history[-1]['time']}"
        )

    def clear_conversation(self, user_id: str) -> bool:
        """Clear conversation history for a user"""
        existed = user_id in self.conversations
        if existed:
            del self.conversations[user_id]
            print(f"🗑️ Cleared conversation history for user: {user_id}")
        return existed


# ✅ GLOBAL INSTANCE (singleton pattern for FastAPI)
chatbot = AdvancedHealthChatbot()


# --------------------------------------------------
# TESTING CODE
# --------------------------------------------------

if __name__ == "__main__":
    print("=" * 70)
    print("🤖 Advanced Health Chatbot - Testing Suite")
    print("=" * 70)
    print()
    
    # Test 1: General health question
    print("📋 Test 1: General health question")
    print("-" * 70)
    response = chatbot.chat(
        "What are some good foods for better sleep?",
        user_id="test_user_1"
    )
    print(f"Success: {response['success']}")
    if response['success']:
        print(f"Reply: {response['reply'][:200]}...")
        print(f"Severity: {response['severity']}")
    else:
        print(f"Error: {response.get('error', 'Unknown error')}")
    print()
    
    # Test 2: Medium severity symptom
    print("📋 Test 2: Medium severity symptom")
    print("-" * 70)
    response = chatbot.chat(
        "I've had a persistent fever for 3 days and feeling weak",
        user_id="test_user_2"
    )
    print(f"Success: {response['success']}")
    if response['success']:
        print(f"Reply: {response['reply'][:200]}...")
        print(f"Severity: {response['severity']}")
        print(f"Warning: {response.get('warning')}")
    else:
        print(f"Error: {response.get('error', 'Unknown error')}")
    print()
    
    print("=" * 70)
    print("✅ Testing completed!")
    print("=" * 70)