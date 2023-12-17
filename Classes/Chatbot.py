from nltk.chat.util import Chat

class CustomChatbot:
    def __init__(self):
        self.responses = [
            [
                r"hi|hello|hey",
                ["Hello!", "Hi there!", "Hey!"]
            ],
            [
                r"how are you|how's it going|how are things",
                ["I'm doing well, thank you!", "I'm good! How about you?", "Things are great! How can I help you?"]
            ],
            [
                r"What is the capital of France?",
                ["The capital of France is Paris."]
            ],
            [
                r"How does photosynthesis work?",
                ["Photosynthesis is the process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll."]
            ],
            [
                r"Who is the current President of the United States?",
                ["As of my last knowledge update in January 2022, Joe Biden is the President of the United States."]
            ],
            [
                r"What is the meaning of life?",
                ["The meaning of life is a philosophical question and varies based on individual beliefs and perspectives."]
            ],
            [
                r"How does the internet work?",
                ["The internet is a global network of interconnected computers that communicate through standard protocols, allowing the sharing of information and resources."]
            ],
            [
                r"What are the symptoms of COVID-19?",
                ["Common symptoms of COVID-19 include fever, cough, and difficulty breathing. It's important to stay updated with health authorities for the latest information."]
            ],
            [
                r"Who wrote \"Romeo and Juliet\"?",
                ["\"Romeo and Juliet\" was written by William Shakespeare."]
            ],
            [
                r"How does a computer work?",
                ["A computer processes information using a central processing unit (CPU), memory, and input/output devices. It follows instructions from software to perform tasks."]
            ],
            [
                r"What is global warming?",
                ["Global warming refers to the long-term increase in Earth's average surface temperature due to human activities, such as the emission of greenhouse gases."]
            ],
            [
                r"How to lose weight in a healthy way?",
                ["Healthy weight loss involves a balanced diet, regular exercise, staying hydrated, and getting enough sleep. Consult a healthcare professional for personalized advice."]
            ],
            [
                r"(.*)",
                ["I'm sorry, I don't have information on that. Please ask another question."]
            ],
        ]
        self.chat = Chat(self.responses)

    def get_response(self, user_input):
        return self.chat.respond(user_input)
    
    

