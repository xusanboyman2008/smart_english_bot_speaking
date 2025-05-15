# question_player.py

from gtts import gTTS
import os

ielts_questions = {
    "Hometown": [
        "Where is your hometown?",
        "What do you like about your hometown?",
        "Is it a good place for young people?",
        "How has it changed over the years?"
    ],
    # Add more topics as needed
}

class QuestionManager:
    def __init__(self):
        self.topics = list(ielts_questions.items())
        self.topic_index = 0
        self.question_index = 0
        self.audio_file = "question.ogg"

    def get_next_question(self):
        if self.topic_index >= len(self.topics):
            return None, None

        topic, questions = self.topics[self.topic_index]
        if self.question_index >= len(questions):
            self.topic_index += 1
            self.question_index = 0
            return self.get_next_question()

        question = questions[self.question_index]
        self.question_index += 1

        tts = gTTS(text=question, lang='en')
        tts.save(self.audio_file)

        return question, self.audio_file

    def cleanup(self):
        if os.path.exists(self.audio_file):
            os.remove(self.audio_file)

qm = QuestionManager()
