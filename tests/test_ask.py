from types import SimpleNamespace
import sys
import weakref

import app.ask as ask_module


def test_ask_prints_input_and_output_token_counts(monkeypatch, capsys):
    response = SimpleNamespace(
        text="回答",
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=8),
    )
    chat = SimpleNamespace(send_message=lambda question: response)

    assert ask_module.ask("質問", chat) == "回答"
    assert "[usage] input_tokens=12 output_tokens=8" in capsys.readouterr().out


def test_main_keeps_one_chat_for_follow_up_questions(monkeypatch, capsys):
    class Client:
        def __init__(self):
            self.created_chats = []
            self.chats = SimpleNamespace(create=self.create_chat)

        def create_chat(self, model):
            chat = Chat(weakref.ref(self))
            self.created_chats.append(chat)
            return chat

    class Chat:
        def __init__(self, client_ref):
            self.questions = []
            self.client_ref = client_ref

        def send_message(self, question):
            assert self.client_ref() is not None
            self.questions.append(question)
            return SimpleNamespace(
                text=f"{question}への回答",
                usage_metadata=SimpleNamespace(
                    prompt_token_count=12, candidates_token_count=8
                ),
            )

    client = Client()
    questions = iter(["続きの質問", "exit"])
    monkeypatch.setattr(sys, "argv", ["app.ask"])
    monkeypatch.setattr(ask_module, "create_client", lambda: client)
    monkeypatch.setattr("builtins.input", lambda _prompt: next(questions))

    ask_module.main()

    assert len(client.created_chats) == 1
    assert client.created_chats[0].questions == [
        ask_module.DEFAULT_QUESTION,
        "続きの質問",
    ]
    output = capsys.readouterr().out
    assert "への回答" in output
