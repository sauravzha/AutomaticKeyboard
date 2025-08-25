🖥️ Virtual Floating Keyboard

A Virtual Floating Keyboard Desktop Application built with Python.
This app allows you to:

Use a floating on-screen keyboard GUI.

Copy & paste text directly into the keyboard.

Automatically type the text into any active window where your cursor is placed.

Control the typing speed with both slider-based fine control and predefined custom speeds (0.5s, 1s, 1.5s, 2s).

Optionally manually type with virtual keys (A–Z, numbers, Enter, Backspace, etc.).

🚀 Features

✅ Floating on-screen keyboard
✅ Copy & Paste integration with clipboard
✅ Auto typing into any application (Notepad, Word, browser, etc.)
✅ Custom typing speeds:

Slider → 0.01s – 0.5s per character

Dropdown → 0.5s, 1s, 1.5s, 2s
✅ Pause, Resume, Stop typing while in progress
✅ Threading support → GUI stays responsive
✅ Clear text box button
✅ Settings persistence (remembers last speed preference)
✅ Cross-platform: Works on Windows, Linux, macOS
✅ Simple, modern UI built with Tkinter

📌 Use Cases

Auto-fill long forms with stored text

Quickly paste paragraphs into documents without manual typing

Simulate typing for presentations or testing

Fun automation tool for writing with a “human-like” typing effect

🛠️ Tech Stack

Python 3.8+

Libraries:

tkinter → GUI (floating keyboard interface)

pyautogui / keyboard → Typing simulation

pyperclip → Clipboard integration

threading → Background typing process

configparser / JSON → Save/load preferences

🖼️ GUI Layout (Wireframe)
 --------------------------------------------------
| Virtual Floating Keyboard                       |
|-------------------------------------------------|
| [ Text Box - Multi Line ]                       |
|                                                 |
| Lorem ipsum dolor sit amet...                   |
|                                                 |
|-------------------------------------------------|
| [Paste] [Copy] [Start Typing] [Pause/Resume] [Stop] [Clear] |
|-------------------------------------------------|
| Typing Speed: [Slider: 0.01s ---- 0.5s]         |
| Predefined Speed: [Dropdown: 0.5s | 1s | 1.5s | 2s] |
|-------------------------------------------------|
| [A][B][C]...[Z] [0-9] [Space] [Enter] [Backspace] |
 --------------------------------------------------

⚙️ Installation
1. Clone Repository
git clone https://github.com/yourusername/virtual-floating-keyboard.git
cd virtual-floating-keyboard

2. Create Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3. Install Dependencies
pip install pyautogui pyperclip keyboard

▶️ Usage

Run the application:

python keyboard_app.py


Use the floating keyboard:

Click Paste to fetch clipboard content.

Adjust typing speed using slider or dropdown.

Place cursor in target application (Notepad, Word, etc.).

Click Start Typing → The text will type automatically.

Use Pause/Resume/Stop to control typing.

Use virtual keys (A–Z, numbers, etc.) to type manually if needed.

🎯 Example Workflow

Copy a paragraph from browser.

Open the virtual keyboard → Click Paste.

Select typing speed: 1s delay per character.

Place cursor inside MS Word.

Click Start Typing.

After 2 seconds, the keyboard starts typing automatically.

Click Pause mid-way → then Resume.

Click Stop to cancel typing.

🧩 Project Structure
virtual-floating-keyboard/
│── keyboard_app.py       # Main application file
│── config.json           # Stores user preferences (speed, settings)
│── README.md             # Documentation
│── requirements.txt      # Dependencies

🛡️ Error Handling

If text box is empty → Show warning before typing.

If clipboard is empty or contains non-text → Show error message.

If user closes app while typing → Safely stop thread.

If invalid speed setting → Fall back to default (0.1s).

🔒 Security Notes

This app does not log keystrokes.

All typing actions are user-initiated only.

Safe to use for personal automation.

🔮 Future Enhancements

Word-by-word typing mode

Support for emojis and special symbols

Dark/Light theme

Snippet Manager → Save frequently used text

Multi-language support

Keyboard shortcuts (e.g., Ctrl+Alt+K to open app)

🤝 Contribution

Contributions are welcome!

Fork the repo

Create a new branch (feature-new)

Commit changes

Open a pull request

📜 License

MIT License – Free to use and modify.
