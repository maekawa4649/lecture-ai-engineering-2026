"""第1回: 素のLLMに会話しながら質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 既定の質問から会話を始める

質問を続けると会話履歴を保ったまま応答する。終了するときは exit または quit を入力する。

ツールを持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def create_client():
    return genai.Client(api_key=get_api_key())


def create_chat(client):
    return client.chats.create(model=MODEL)


def ask(question: str, chat=None) -> str:
    if chat is None:
        client = create_client()
        chat = create_chat(client)

    response = chat.send_message(question)
    usage = response.usage_metadata
    if usage is None:
        print("[usage] input_tokens=不明 output_tokens=不明")
    else:
        input_tokens = usage.prompt_token_count
        output_tokens = usage.candidates_token_count
        print(
            f"[usage] input_tokens={input_tokens if input_tokens is not None else '不明'} "
            f"output_tokens={output_tokens if output_tokens is not None else '不明'}"
        )

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    try:
        client = create_client()
        chat = create_chat(client)
        question = args.question
        while True:
            print(f"[質問] {question}\n")
            print(ask(question, chat))
            while True:
                try:
                    question = input(
                        "\n続けて質問できます（終了: exit / quit）: "
                    ).strip()
                except EOFError:
                    return
                if question.lower() in {"exit", "quit"}:
                    return
                if question:
                    break
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
