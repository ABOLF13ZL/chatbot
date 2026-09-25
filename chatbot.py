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

    def handle_command(self, user_input):
        command = user_input.lower().strip()
        result = ''
        system_messages = [
            m for m in self.messages if m['role'] == 'system']
        user_messages = [
            m for m in self.messages if m['role'] == 'user']
        assistant_messages = [
            m for m in self.messages if m['role'] == 'assistant']
        if command == '/clear':
            self.messages = [*system_messages]
            return 'Conversation history cleared.'

        elif command == '/history':
            for history in self.messages:
                result += (f'{history['role'].title()}: {history['content']}\n')

            return result

        elif command == '/help':
            return 'Available commands:\n\n/help      Show commands\n/clear     Clear conversation\n/history   Show conversation\n/q         Exit'

        elif command == '/stats':
            return f'Messages: {len(self.messages)}\nSystem messages: {len(system_messages)}\nUser messages: {len(user_messages)}\nAssistant messages: {len(assistant_messages)}'

        elif command == '/q':
            return True

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
                'Ask something(Enter "/q" to terminate): ')
            result = self.handle_command(user_input)

            if result is True:
                break
            if result != None:
                print(result)
                continue

            bot_answer = self.get_response(user_input)
            print(bot_answer)


def main():
    chatbot = ChatBot()
    chatbot.chat()


if __name__ == '__main__':
    main()
