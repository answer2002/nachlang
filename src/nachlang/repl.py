"""
REPL interactivo de NachLang.
"""

from .transpiler import transpile_code

try:
    import openai
except ImportError:
    openai = None


def run_repl():
    print("NachLang REPL — Ctrl-D para salir")
    env: dict[str, object] = {}
    buffer: list[str] = []
    while True:
        prompt = '... ' if buffer else 'nacho > '
        try:
            line = input(prompt)
        except EOFError:
            print()
            break
        if buffer:
            if not line.strip():
                code = '\n'.join(buffer) + '\n'
                buffer = []
                try:
                    py_code = transpile_code(code)
                    exec(py_code, env)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                buffer.append(line)
            continue
        if not line.strip():
            continue
        if line.strip().endswith(':'):
            buffer.append(line)
            continue
        low = line.strip().lower()
        for prefix in ('ia:', 'ia ', 'ai:', 'ai '):
            if low.startswith(prefix):
                prompt = line.strip()[len(prefix):].strip()
                if openai is None:
                    print(
                        'Error: openai library not installed. '
                        'Instala el extra opcional "ai" con '
                        '`pip install nachlang[ai]`.'
                    )
                else:
                    try:
                        resp = openai.ChatCompletion.create(
                            model='gpt-3.5-turbo',
                            messages=[
                                {'role': 'system',
                                 'content': 'Eres un asistente de programación para NachLang.'},
                                {'role': 'user', 'content': prompt},
                            ],
                            temperature=0.0,
                        )
                        content = resp.choices[0].message.content
                    except Exception as e:
                        print(f'Error al solicitar IA: {e}')
                    else:
                        print(content)
                break
        else:
            code = line + '\n'
            try:
                py_code = transpile_code(code)
                exec(py_code, env)
            except Exception as e:
                print(f"Error: {e}")