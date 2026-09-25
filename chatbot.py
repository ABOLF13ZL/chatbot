from openai import OpenAI, OpenAIError
import dotenv
import os

dotenv.load_dotenv()


class ChatBot:
    def __init__(self):
        api_key = os.getenv('GROQ_API_KEY')
        if api_key:
            self.client = OpenAI(
                api_key=api_key,
                base_url='https://api.groq.com/openai/v1'
            )
        else:
            raise OpenAIError('API key does not exist.')
        self.messages = [
            {'role': 'system', 'content': 'Give short answer.'}
        ]

    def get_response(self, message):
        try:
            self.messages.append({'role': 'user', 'content': message})
            response = self.client.chat.completions.create(
                model='openai/gpt-oss-120b',
                temperature=0.7,
                messages=self.messages
            )
            result = response.choices[0].message.content
            self.messages.append({'role': 'assistant', 'content': result})
            return result
        except OpenAIError:
            print('Please check your API or connection with internet.')
            return None

    def chat(self):
        while True:
            user_input = input(
                'Ask something(Enter "q" to terminate): ')
            if user_input.lower().strip() == 'q':
                print('Good luck')
                break

            bot_answer = self.get_response(user_input)
            print(bot_answer)


def main():
    chatbot = ChatBot()
    chatbot.chat()


if __name__ == '__main__':
    main()
