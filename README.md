# Anti-away-MSTeams

## What it does

This utility opens a small GUI and repeatedly types one character into the
currently focused application. Press **F6** to start or stop typing.

## Requirements

- Python 3
- `pynput`
- A graphical desktop session

Install the dependency:

```bash
python -m pip install pynput
```

## Usage

1. Start the program:

   ```bash
   python single_letter_autotyper.py
   ```

2. Set the letter, interval, count, and start delay in the window.
3. Open and focus the application or text field where the character should be
   entered.
4. Press **F6** to start typing after the configured delay.
5. Press **F6** again to stop. A count of `0` means unlimited typing until
   stopped.

The program types into whichever application has focus. Test it in a safe text
field before using it elsewhere.

## Disclaimer

Before running this tool, make sure your IT/security policies allow you to run
a Python script and that your IT department does not monitor or restrict your
local files or keyboard input. You are responsible for obtaining all required
authorization and for how this tool is used. The author provides this tool
without warranty and accepts no responsibility or liability for anyone running
it, including any monitoring, policy violations, data loss, or other consequences.