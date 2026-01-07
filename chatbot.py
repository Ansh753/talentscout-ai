import openai
import re
from typing import List, Dict, Any

class HiringAssistant:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.candidate_info = {
            "full_name": "",
            "email": "",
            "phone": "",
            "years_experience": "",
            "desired_position": "",
            "current_location": "",
            "tech_stack": []
        }
        self.conversation_phase = "greeting"
        self.required_fields = ["full_name", "email", "phone", "years_experience", 
                               "desired_position", "current_location", "tech_stack"]
    
    def get_greeting(self) -> str:
        return """👋 Hello! I'm the **TalentScout Hiring Assistant**.

I'll help with your initial screening process. Let's start with some basic information:

**What's your full name?**"""
    
    def get_system_prompt(self) -> str:
        prompts = {
            "greeting": """You are a friendly hiring assistant for TalentScout, a tech recruitment agency.
            Your goal is to collect candidate information and assess technical skills.
            Start by greeting and asking for their name.""",
            
            "info_gathering": """You are collecting candidate information. Ask for these details ONE AT A TIME:
            1. Full Name
            2. Email Address
            3. Phone Number
            4. Years of Experience
            5. Desired Position/Role
            6. Current Location
            7. Tech Stack (programming languages, frameworks, tools)
            
            Be conversational. Validate inputs (check email format, etc.).
            After getting all info, move to technical questions.""",
            
            "tech_questions": """Generate 3-5 technical questions based on the candidate's tech stack.
            Make questions relevant to their experience level.
            Mix conceptual and practical questions.
            After asking questions, provide feedback and conclude.""",
            
            "conclusion": """Thank the candidate, explain next steps in hiring process.
            Mention they'll hear back within 3-5 business days."""
        }
        return prompts.get(self.conversation_phase, prompts["info_gathering"])
    
    def extract_info_from_message(self, message: str) -> None:
        """Extract and store candidate information from messages"""
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, message)
        if emails and not self.candidate_info["email"]:
            self.candidate_info["email"] = emails[0]
        
        # Extract phone (basic pattern)
        phone_pattern = r'\b\d{10}\b|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, message)
        if phones and not self.candidate_info["phone"]:
            self.candidate_info["phone"] = phones[0]
        
        # Extract years of experience
        exp_pattern = r'(\d+)\s*(?:year|yr|years)'
        exp_match = re.search(exp_pattern, message.lower())
        if exp_match and not self.candidate_info["years_experience"]:
            self.candidate_info["years_experience"] = exp_match.group(1)
    
    def detect_conversation_phase(self) -> str:
        """Determine current phase based on collected info"""
        missing_fields = [field for field in self.required_fields 
                         if not self.candidate_info[field]]
        
        if len(missing_fields) == len(self.required_fields):
            return "greeting"
        elif missing_fields:
            return "info_gathering"
        elif self.candidate_info["tech_stack"] and self.conversation_phase == "info_gathering":
            return "tech_questions"
        else:
            return "conclusion"
    
    def generate_tech_questions(self) -> str:
        """Generate technical questions based on tech stack"""
        if not self.candidate_info["tech_stack"]:
            return "I see you haven't specified your tech stack. Could you tell me what technologies you work with?"
        
        tech_list = ", ".join(self.candidate_info["tech_stack"])
        prompt = f"""Based on this tech stack: {tech_list}
        Experience: {self.candidate_info['years_experience']} years
        Role: {self.candidate_info['desired_position']}
        
        Generate 3-5 technical interview questions that are:
        1. Relevant to their experience level
        2. Mix of conceptual and practical
        3. Specific to their mentioned technologies
        
        Format as a numbered list with clear questions."""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a technical interviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content
        except:
            return f"Great! Now I have your info. Let me ask you some questions about {tech_list}."
    
    def process_message(self, user_message: str, conversation_history: List[Dict]) -> str:
        """Process user message and generate response"""
        # Update conversation phase
        self.conversation_phase = self.detect_conversation_phase()
        
        # Extract information from message
        self.extract_info_from_message(user_message)
        
        # Special handling for tech stack
        if "tech" in user_message.lower() or "stack" in user_message.lower():
            # Extract technologies mentioned
            tech_keywords = ["python", "java", "javascript", "react", "node", "django", 
                            "flask", "aws", "docker", "kubernetes", "sql", "mongodb",
                            "fastapi", "spring", "angular", "vue", "typescript"]
            mentioned_tech = [tech for tech in tech_keywords if tech in user_message.lower()]
            if mentioned_tech:
                self.candidate_info["tech_stack"] = mentioned_tech
        
        # Generate response based on phase
        if self.conversation_phase == "tech_questions":
            return self.generate_tech_questions()
        
        # Use OpenAI for other phases
        try:
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                *conversation_history[-6:],  # Last 6 messages for context
                {"role": "user", "content": user_message}
            ]
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=250
            )
            
            ai_response = response.choices[0].message.content
            
            # Check for conversation end
            if any(word in user_message.lower() for word in ["bye", "goodbye", "thanks", "thank you"]):
                ai_response += "\n\nThank you for your time! We'll contact you within 3-5 business days. Goodbye! 👋"
                self.conversation_phase = "conclusion"
            
            return ai_response
            
        except Exception as e:
            return f"I apologize, I encountered an error. Please try again. Error: {str(e)}"