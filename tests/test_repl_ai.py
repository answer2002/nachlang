import os
import sys

# Agregar ruta al paquete src para importaciones
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

import builtins

import pytest

import nachlang.repl as repl


def test_repl_ai_not_installed(monkeypatch, capsys):
    repl.openai = None
    inputs = iter(["ia: mejora esta función", ""])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))
    repl.run_repl()
    out = capsys.readouterr().out
    assert "openai library not installed" in out.lower()


class DummyChoice:
    def __init__(self):
        self.message = type("M", (), {"content": "Sugerencia IA"})


class DummyResponse:
    def __init__(self):
        self.choices = [DummyChoice()]


def test_repl_ai_success(monkeypatch, capsys):
    class DummyChatCompletion:
        @staticmethod
        def create(model, messages, temperature):
            return DummyResponse()

    dummy_openai = type("OpenAI", (), {"ChatCompletion": DummyChatCompletion})
    repl.openai = dummy_openai
    inputs = iter(["ai: analiza esta función", ""])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))
    repl.run_repl()
    out = capsys.readouterr().out
    assert "Sugerencia IA" in out
