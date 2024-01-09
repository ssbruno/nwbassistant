import openai
import time

openai.api_key = "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"
#NWBAssistantKey

class OpenAI:
    def generate_ai_response(prompt):
        response = openai.Completion.create(
            engine = "text-davinci-003",
            prompt = prompt,
            max_tokens = 1000,
            n = 1,
            stop = None,
            temperature = 0.5
        )
        return response["choices"][0]["text"]
    
    def start_conversation(self):
        response = self.generate_ai_response('greet me pleasantly')
        response.replace('Absolutely!', '').replace('Of course!').trim()
        return response