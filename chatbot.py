from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re
from textblob import TextBlob
from database import store_chat_message
from datetime import datetime
import speech_recognition as sr  # Library for speech-to-text

# Load once globally
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Maintain chat + sentiment history per user
user_histories = {}
user_sentiments = {}

def therapist_chat(user_id, prompt, history=None, sentiment_score=None):
    """
    Chatbot function with expanded empathy, sentiment tracking, and crisis detection.
    """
    try:
        prompt_lower = prompt.lower().strip()

        # === Emotion Detection === #
        blob = TextBlob(prompt)
        sentiment = blob.sentiment.polarity  # Ranges from -1 (negative) to 1 (positive)
        
        # Store chat message with sentiment
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        store_chat_message(user_id, prompt, sentiment, current_date)

        # === Enhanced Crisis Detection === #
        crisis_patterns = [
            r"(?:i\s)?don[’']?t want to live",
            r"suicid(?:e|al)?", r"end it all", r"hopeless", r"want to die",
            r"can[’']?t go on", r"no reason to live", r"worthless", r"feel dead", r"kill myself",
            r"ending everything", r"nothing matters", r"lost the will", r"i give up"
        ]
        is_crisis = any(re.search(pattern, prompt_lower) for pattern in crisis_patterns)

        print(f"Debug: Prompt: '{prompt_lower}', Is Crisis: {is_crisis}, Sentiment: {sentiment}")  # Debug print

        if is_crisis:
            return (
                "I'm really sorry you're feeling this way. You're not alone in this. 💛\n"
                "I'm not a professional therapist—please reach out for help:\n"
                "📞 US: 988 | UK: 116 123 | India: +91 9820466726\n"
                "You matter more than you know, and there are people ready to support you. 🤝"
            )

        # === Track sentiment history === #
        if sentiment_score is not None:
            if user_id not in user_sentiments:
                user_sentiments[user_id] = []
            user_sentiments[user_id].append(sentiment_score)

        # === Predefined Empathetic Responses === #
        empathetic_responses = {
            ("hi", "hello", "hey"): "Hey there! 👋 I’m here to support you. What’s on your mind today? 😊",
            ("sad", "unhappy", "teary"): "I’m really sorry you’re feeling sad. Want to talk about what’s been making you feel this way? 💙",
            ("anxious", "nervous", "panic", "overwhelmed"): "It sounds like anxiety might be weighing on you. Want to walk through it together? No pressure. 🫂",
            ("lonely", "alone"): "Feeling lonely can be really tough. You’re not alone here. Want to share what’s been going on? 🤗",
            ("burnout", "tired", "exhausted"): "Burnout is real and heavy. You've been doing so much. It's okay to pause. 💆‍♀️",
            ("happy", "excited"): "That’s so great to hear! 🎉 What’s been going well? Let’s celebrate the joy.",
            ("fight", "fought", "argument"): "Friendship fights can really hurt. Want to talk about what happened? I’m listening. 💭",
            ("rude", "mean", "prejudiced"): "That’s painful to go through. No one deserves to be treated unfairly. I’m here if you want to share more. 🫶",
        }

        for keywords, response_text in empathetic_responses.items():
            if any(word in prompt_lower for word in keywords):
                return response_text

        # === Build context from recent journal === #
        context = ""
        if history and history[-1:]:
            entry, sentiment, date = history[-1]
            context = f"[{date}] Journal (sentiment: {sentiment:.2f}): {entry}\n"
            if len(context) > 300:
                context = context[-300:]

        full_prompt = f"{context}User: {prompt}" if context else prompt
        if len(full_prompt) > 300:
            full_prompt = full_prompt[-300:]

        # === Tokenize and generate response === #
        new_input_ids = tokenizer.encode(full_prompt + tokenizer.eos_token_id, return_tensors='pt')
        chat_history_ids = user_histories.get(user_id)
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids

        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=200,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=20,
            top_p=0.85,
            temperature=0.3,
        )

        user_histories[user_id] = chat_history_ids

        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

        # Final safety net for crisis
        if is_crisis:
            return (
                "I'm really sorry you're feeling this way. You're not alone in this. 💛\n"
                "I'm not a professional therapist—please reach out for help:\n"
                "📞 US: 988 | UK: 116 123 | India: +91 9820466726\n"
                "You matter more than you know, and there are people ready to support you. 🤝"
            )

        return response

    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I’m having trouble responding right now. Please try again later."

def voice_chat(user_id, history=None):
    """
    Simple voice input function to capture speech and interact with the chatbot.
    """
    print("Speak to chat. Say 'exit' to stop.")
    
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                prompt = recognizer.recognize_google(audio)
                print(f"You said: {prompt}")

            if prompt.lower().strip() == "exit":
                print("Goodbye!")
                break

            response = therapist_chat(user_id, prompt, history)
            print(f"Therapist: {response}")

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand. Please speak again.")
        except sr.RequestError:
            print("Speech recognition failed. Try again.")
        except sr.WaitTimeoutError:
            print("No speech detected. Please speak.")

# Example usage
if __name__ == "__main__":
    user_id = "user123"
    history = []
    voice_chat(user_id, history)