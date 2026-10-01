from openai import OpenAI, OpenAIError
from pathlib import Path
import dotenv
import json
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
            {'role': 'system', 'content': '''You are a helpful AI assistant for an online store.
Answer the user's questions using the provided product information.
Never invent or guess product details such as price, stock, name, or product code.
If the provided information is not enough to answer the question, clearly say that the information is not available.
Keep your answers short and clear.'''}
        ]
        self.product_manager = ProductManager()

    def handle_command(self, user_input):
        command = user_input.lower().strip()
        parts = user_input.split()
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
            return 'Available commands:\n\n/help      Show commands\n/clear     Clear conversation\n/history   Show conversation\n/product "Code" Get product\n/q         Exit'

        elif command == '/stats':
            return f'Messages: {len(self.messages)}\nSystem messages: {len(system_messages)}\nUser messages: {len(user_messages)}\nAssistant messages: {len(assistant_messages)}'

        elif len(parts) == 2 and parts[0].lower() == '/product':
            product = self.product_manager.get_product_by_code(parts[1])
            if product is None:
                return 'This product does not exist.'
            return product

        elif command == '/q':
            return True

    def get_product_by_code(self, code):
        return self.product_manager.get_product_by_code(code)

    def format_product(self, product):
        return f'Product code: {product['code']}\nProduct name: {product['name']}\nPrice: {product['price']}\nStock: {product['stock']}'

    def get_product_context(self, code='', name=''):
        product_code = self.get_product_by_code(code)
        product_name = self.get_product_by_name(name)
        if product_code is None:
            if product_name is None:
                return ('This product does not exist.')
            return self.format_product(product_name)
        else:
            return self.format_product(product_code)

    def extract_product_code(self, message):
        text = message.split()
        for word in text:
            word = word.strip("'s/,;?:")

            if word.startswith('N') and word[1:].isdigit():
                return word

    def get_product_by_name(self, name):
        return self.product_manager.get_product_by_name(name)

    def extract_product_name(self, message):
        text = message.lower()
        products = self.product_manager.load_products()
        for product in products:
            if product['name'] in text:
                return product['name']

    def get_response(self, message, context=''):
        try:
            messages = [*self.messages, {'role': 'system', 'content': context}]
            messages.append({'role': 'user', 'content': message})
            response = self.client.chat.completions.create(
                model='openai/gpt-oss-120b',
                temperature=0.7,
                messages=messages
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
            if result is not None:
                print(result)
                continue

            product_code = self.extract_product_code(user_input)
            product_name = self.extract_product_name(user_input)
            context = ''
            if product_code is not None:
                context = self.get_product_context(code=product_code)
            elif product_name is not None:
                context = self.get_product_context(name=product_name)
            bot_answer = self.get_response(user_input, context)
            print(bot_answer)


class ProductManager:
    def __init__(self):
        self.path = Path(r'data\products.json')

    def load_products(self):
        data = self.path.read_text()
        load_data = json.loads(data)
        return load_data

    def get_product_by_code(self, code):
        for product in self.load_products():
            if product['code'] == code:
                return product
        else:
            return None

    def get_product_by_name(self, name):
        for product in self.load_products():
            if product['name'] == name:
                return product
        else:
            return None

    def is_available(self, code):
        for product in self.load_products():
            if product['code'] == code:
                if int(product['stock']) > 0:
                    return True
                elif int(product['stock']) == 0:
                    return False
                else:
                    return None

    def get_available_products(self):
        available_products = []
        for product in self.load_products():
            if int(product['stock']) > 0:
                available_products.append(product)
        return available_products


def main():
    chatbot = ChatBot()
    chatbot.chat()


if __name__ == '__main__':
    main()
