import os
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key-not-real")

import llm_client

    
class FakeBlock:
    def __init__(self, type, text=""):
        self.type = type
        self.text = text


class FakeResponse:
    def __init__(self, blocks):
        self.content = blocks
        self.stop_reason = "end_turn"
        self.usage = type("U", (), {"input_tokens": 10, "output_tokens": 5})()


class FakeClient:
    def __init__(self, blocks):
        self.blocks = blocks
        self.last_params = None
        self.messages = self      

    def create(self, **params):
        self.last_params = params
        return FakeResponse(self.blocks)


def test_two_text_blocks_are_joined(monkeypatch):
    fake = FakeClient([FakeBlock("text", "Hello "), FakeBlock("text", "world")])
    monkeypatch.setattr(llm_client, "client", fake)
    assert llm_client.ask_llm("hi") == "Hello world"


def test_thinking_block_is_ignored(monkeypatch):
    fake = FakeClient([FakeBlock("thinking", "secret reasoning"), FakeBlock("text", "Answer")])
    monkeypatch.setattr(llm_client, "client", fake)
    assert llm_client.ask_llm("hi") == "Answer"


def test_no_text_block_returns_fallback(monkeypatch):
    fake = FakeClient([FakeBlock("thinking")])
    monkeypatch.setattr(llm_client, "client", fake)
    assert llm_client.ask_llm("hi") == "No answer came back."


def test_system_prompt_only_sent_when_given(monkeypatch):
    fake = FakeClient([FakeBlock("text", "ok")])
    monkeypatch.setattr(llm_client, "client", fake)
    llm_client.ask_llm("hi")
    assert "system" not in fake.last_params
    llm_client.ask_llm("hi", system="rules")
    assert fake.last_params["system"] == "rules"