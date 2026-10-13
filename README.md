# StudyFlow AI — Smart Study Planner

A beginner-friendly school exhibition project built with Python and Streamlit. It helps students organize assignments, prioritize work, generate focus-session timetables, and track completed tasks.

## Features
- **Overview dashboard:** open tasks, tasks due soon, estimated remaining effort, and completion rate.
- **Task management:** add subjects, tasks, deadlines, effort estimates, difficulty, and importance.
- **Search and filters:** find tasks and view all, open, or completed tasks.
- **Completion tracking:** mark work open or completed and see the progress charts update.
- **Smart schedule:** generates focus sessions based on deadlines, priority, daily study time, and session length.
- **Charts and CSV downloads:** export task lists and timetables for printing or sharing.
- **Learning guide:** explains the priority score, provides usage tips, and answers common questions.
- **Mobile friendly:** works on Android and iOS browsers with touch-sized controls, a 2x2 summary grid, task and timetable cards, and a settings panel that opens on the main page.
- **Privacy-conscious demo:** task information is processed locally by the app; no paid AI service is used.

## Important project note
This is a **rule-based, AI-inspired prototype**, not a trained machine-learning model. It uses an explainable scoring algorithm so students can understand why a task receives priority.

## Requirements
- Windows, macOS, or Linux computer
- Python 3.10 or newer
- Internet connection for the first installation of the Python packages

## Easiest launch on Windows
1. Download and extract `AI_Smart_Study_Planner_Exhibition_Package.zip`.
2. Open the extracted `AI_Smart_Study_Planner` folder.
3. Double-click `run_windows.bat`.
4. Wait for installation and startup. Open the local address shown in the terminal (usually `http://localhost:8501`) if the browser does not open automatically.
5. Keep the terminal open while using the app. Press `Ctrl+C` in the terminal to stop it.

## Launch from a terminal
Open a terminal inside this folder and run:

### Windows
```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Using it on an Android phone or iPhone
**Option A: same Wi-Fi (no extra cost, good for the exhibition).**
1. Start the app on the computer with `run_windows.bat` (or run `python -m streamlit run app.py --server.address 0.0.0.0`).
2. Connect the phone to the same Wi-Fi network as the computer.
3. On the phone, open Chrome (Android) or Safari (iPhone) and go to `http://<computer-IP>:8501`. Find the IP with `ipconfig` on Windows (the IPv4 address) or `ifconfig` / `ip a` on macOS/Linux.
4. If it does not load, allow Python through the Windows Firewall for private networks. Some school or guest Wi-Fi networks block device-to-device connections; a phone hotspot shared with the computer works well as a fallback.

**Option B: public link (works on any network).** Upload the project to GitHub and deploy it free on Streamlit Community Cloud (share.streamlit.io). Anyone with the link can then open it on a phone. Note that tasks stay only in each visitor's session.

**Add to home screen (looks like an app).**
- Android Chrome: menu (three dots) → *Add to Home screen* / *Install app*.
- iPhone Safari: Share button → *Add to Home Screen*.

Tip: tap **⚙️ Plan settings** at the top of the page to change the start date, plan length, and daily study time.

## Exhibition demonstration
1. Open the **Tasks** tab and restore the sample tasks.
2. Add a task of your own and explain its deadline, difficulty, and importance.
3. Search or filter the task list and mark a task completed.
4. Open the **Plan** tab and generate the timetable.
5. Explain the charts and download the timetable as CSV.
6. Open the **Progress** tab and explain how the priority score works.

## Tests
From the project folder, run:
```bash
python -m unittest discover -s tests -v
```
