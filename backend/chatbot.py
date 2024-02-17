import openai
import os
import io
import pygame
import random

class Chatbot:
    def __init__(self):
        self.key_path = "openai_key.txt"
        self.key = self.load_openai_key()
        os.environ['OPENAI_API_KEY'] = self.key
        self.client = openai.OpenAI()

        self.memory = []
        self.load_personality("brief_guru")

    def load_openai_key(self):
        try:
            with open(self.key_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"File not found: {self.key_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def load_personality(self, persona='default'):
        default_personality = "You are a friendly AI chatbot that responds to questions in 50 words or less."
        brief_guru_personality = """You are a wise and kind meditation guru. You narrate brief but enchanting
        guided meditations from the perspecive of the object that the user tells you to be. You
        pride yourself on the fact that the guided mediations are only 50 words long or less."""
        guru_personality = """You are a wise and kind meditation guru. You narrate brief but enchanting
        guided meditations from the perspecive of the object that the user tells you to be."""
        if persona == "guru":
            personality = guru_personality
        elif persona == "brief_guru":
            personality = brief_guru_personality
        else:
            personality = default_personality
        self.memory.append({"role": "system", "content": personality})

    def answer(self, prompt, ver="gpt-4-1106-preview"):
        self.memory.append({"role": "user", "content": prompt})
        completion = self.client.chat.completions.create(
            model=ver,
            messages=self.memory
        )
        # Amnesia
        self.memory.pop()
        return completion.choices[0].message.content

    def text_to_audio(self, text, voice="random", language="en"):
        voice = voice.lower()
        if voice == "random":
            roll = random.randint(0, 5)
            voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
            voice = voices[roll]

        speech_file_path = os.path.join(os.path.dirname(__file__), "audio", "speech.mp3")
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )

        with open(speech_file_path, 'wb') as f:
            f.write(response.content)

        return speech_file_path
    
    def speak(self, speech_file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(speech_file_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        os.remove(speech_file_path)
        pygame.mixer.quit()
        return
    
    def run(self):
        prompt = input("Enter prompt:\n")
        answer = self.answer(prompt)
        speech_file_path = self.text_to_audio(answer)
        self.speak(speech_file_path)

if __name__ == '__main__':
    chatbot = Chatbot()
    chatbot.run()
