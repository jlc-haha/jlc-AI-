#!/usr/bin/env python3
"""Claude Code statusline script.
Reads JSON from stdin, outputs a formatted status line.
"""
import sys
import json

def main():
    raw = sys.stdin.buffer.read()
    # Handle BOM if present
    if raw and raw[0:3] == b'\xef\xbb\xbf':
        raw = raw[3:]

    try:
        data = json.loads(raw.decode('utf-8'))
    except Exception:
        print("(statusline: invalid input)", file=sys.stderr)
        return

    ws = data.get('workspace', {})
    model = data.get('model', {})
    ctx = data.get('context_window', {})

    cwd = ws.get('current_dir', '?')
    model_name = model.get('display_name', '?')
    remaining = ctx.get('remaining_percentage')

    if remaining is not None and remaining > 0:
        n = max(1, min(10, int(remaining / 10 + 0.5)))
        bar = '█' * n + '░' * (10 - n)
        print(f'{cwd}  |  {model_name}  |  Context: [{bar}] {remaining}%')
    else:
        print(f'{cwd}  |  {model_name}')

if __name__ == '__main__':
    main()
