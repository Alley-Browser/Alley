"""
Unit tests for a custom chatbot class.

Tests the chatbot's response to various inputs like greetings, empty
strings, and unsupported questions. This allows us to validate the 
chatbot's responses match what we expect for common use cases.

The tests are part of the module so they can access the chatbot class 
directly. But they are designed to test the class as a black box 
by only interacting with the public API.
"""
import unittest
from src.CustomChatbot import CustomChatbot

class TestCustomChatbot(unittest.TestCase):

    def setUp(self):
        self.chatbot = CustomChatbot()

    def test_get_response_hello(self):
        user_input = "hello"
        response = self.chatbot.get_response(user_input)
        self.assertIn(response, ["Hello!", "Hi there!", "Hey!"])

    def test_get_response_empty(self):
        user_input = ""
        response = self.chatbot.get_response(user_input)
        self.assertEqual(response, "I'm sorry, I don't have information on that. Please ask another question.")

    def test_get_response_no_match(self):
        user_input = "Tell me about quantum physics"
        response = self.chatbot.get_response(user_input)
        self.assertEqual(response, "I'm sorry, I don't have information on that. Please ask another question.")

if __name__ == '__main__':
    unittest.main()
