class QAProcessor:
    def __init__(self):
        pass

    def generate_qa_prompt(self, chapter_summary, chat_history):
        """
        Generates a prompt for the tutoring AI based on the chapter summary and chat history.

        Args:
            chapter_summary (str): Summary of the chapter content.
            chat_history (list): List of dictionaries containing user and agent messages.

        Returns:
            str: Formatted prompt for the AI to process.
        """
        prompt = f"""
SYSTEM
You are an AI tutor designed to help students understand course material.

Below is the chapter summary you will use to answer the user's question:
{chapter_summary}

Conversation History:
{self.format_chat_history(chat_history)}

Respond concisely and accurately to the latest question. If the question is unclear or not covered in the summary, ask for clarification or provide general guidance. Provide only the answer.
"""
        return prompt.strip()

    def format_chat_history(self, chat_history: list):
        """
        Formats the chat history into a conversation string.

        Args:
            chat_history (list): List of dictionaries containing user and agent messages.

        Returns:
            str: Formatted conversation history as a string.
        """
        return "\n".join([
            f"User: {msg['user']}" if 'user' in msg else f"Agent: {msg['agent']}"
            for msg in chat_history
        ])
