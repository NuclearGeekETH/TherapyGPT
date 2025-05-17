# TherapyGPT

> **Author:** [NuclearGeekETH](https://github.com/NuclearGeekETH)  
> **License:** MIT  
> **Status:** Beta

TherapyGPT is an advanced AI-powered therapy assistant. It provides a **secure, private, records-based support environment** for mental health professionals and individuals. Combining a customizable intake form, private session notes, and a cutting-edge chatbot interface, the app enables highly personalized, context-aware therapeutic conversations.

---
  
## Features

- **Comprehensive Intake Form**  
  Collect, update, and store detailed patient history — structured to robust clinical standards across mental, medical, social, cultural, and family domains.

- **Dynamic Chat Interface**  
  Chat with TherapyGPT — an AI therapist whose responses always include your latest patient history and past memories as part of the system prompt, ensuring maximum context.

- **Persistent Patient Data**  
  All history and chat context are stored privately and persist between sessions.

- **Modern UX** powered by [Gradio](https://www.gradio.app/) (`blocks`, `tabs`, `chatbot`, live dataframes, and more).

- **Configurable Model Selector**  
  Swap between OpenAI & provisioned models (e.g., GPT-4o, GPT-4.1, O4 series, ChatGPT, and more) via a dropdown.

- **Easy Local Deployment**  
  Launch with a single script. Optionally, enable authentication and remote sharing.

---

## ⚠️ Important Notice

TherapyGPT is **not a medical device or a substitute for professional diagnosis, advice, or treatment**. All AI output may be inaccurate or hallucinated.  
_**Never rely on TherapyGPT for crisis intervention, diagnosis, or medical emergencies!**_  
**Always consult with a licensed mental health professional.**

---

## Requirements

- **Python 3.9+**  
- **[OpenAI API key](https://platform.openai.com/account/api-keys)** (set as an environment variable: `OPENAI_API_KEY`)
- **pip**

### Python dependencies

```
pip install -r requirements.txt
```
This will install:  
- `openai`  
- `gradio`

---

## Quickstart

**1. Clone the repository:**
```bash
git clone https://github.com/NuclearGeekETH/TherapyGPT.git
cd TherapyGPT
```

**2. Set your OpenAI API key:**
```bash
set OPENAI_API_KEY=sk-...             # On Windows (cmd.exe)
# or
export OPENAI_API_KEY=sk-...          # On Mac/Linux
```

**3. Launch the app:**

### Windows:
Double-click `startup_chat.bat` (auto-creates a virtualenv and launches `main.py`),  
**or** run:
```bash
python main.py
```

### Mac/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Open [http://localhost:7860/](http://localhost:7860/) in your web browser.

---

## File Structure

```
TherapyGPT/
│
├── main.py                        # Main Gradio UI application
├── requirements.txt               # Python dependencies
├── startup_chat.bat               # (Windows) autocreates venv, runs app
│
├── modules/
│   ├── get_openai_response.py     # Streaming OpenAI chat backend
│   ├── patient_form_utility.py    # Intake form data IO/flattening/marshalling
│   ├── memory_utility.py          # Memory form data IO/flattening/marshalling
│   ├── data.json                  # Single-patient persistent data store (JSON)
│   └── memory.json                # memory persistent data store (JSON)
│
└── README.md                      # ← This file!
```

---

## Usage

1. **Fill Out Intake Form:**  
   Enter as much or as little patient data as required across all sections (intake, history, trauma, strengths, family, etc).

2. **Save Changes:**  
   Click &quot;Save Changes&quot; to persist your data to `modules/data.json`.

3. **Chat with TherapyGPT:**  
   The chatbot will use **your latest patient history** to tailor initial responses and all subsequent session chats. Memoris can be stored and edited on the Memories tab.

4. **Change Models or System Message:**  
   Use the dropdown to switch models (requires the appropriate OpenAI access), and optionally edit the system message/context sent to the model.

---

## Screenshots

<details>
<summary>Click to show screenshot</summary>

**Text Chat:**  
![TherapyGPT Text Chat](https://github.com/user-attachments/assets/fe365af3-7d4c-4b57-b4c5-5e11c955cecc)
**Patient Data Form:** 
![TherapyGPT Patient Data](https://github.com/user-attachments/assets/0d941706-d218-47f7-b6da-988ad70b04b8)
**Memory Bank:** 
![TherapyGPT Memories](https://github.com/user-attachments/assets/95b299fc-7def-4def-9e64-527c1a406a86)


</details>

---

## Customization

- **Adding new fields:**  
  - Modify `main.py` and parallel `modules/utility.py` data flatten/unflatten functions as needed.
- **Multi-user/multi-patient support:**  
  - Each patient would need a separate JSON file (`data_{id}.json`); backend logic can be extended.
- **Security:**  
  - For true confidentiality, **always run on a secured, encrypted system**.
  - For remote access or team use, **enable Gradio authentication** in `main.py`'s `demo.launch(auth=...)`.

---

## Security and Privacy

- **Data stored locally** in `modules/data.json` and `modules/memories.json` by default. **No cloud sync** unless you add it.
- **No patient data is sent to OpenAI** except through your chat input/history/system prompt _which you control_.
- **HIPAA Compliance:**  
  This project is **not** certified for HIPAA.  
  Use at your own discretion; do your own security diligence for real medical/behavioral health deployments.

---

## Troubleshooting

- **Key not found:**  
  `OPENAI_API_KEY` must be set in your environment for the chatbot to work.

- **Port conflicts:**  
  If port `7860` is busy, set `server_port=XXXX` in `demo.launch`.

- **Module Not Found:**  
  Make sure you start the app with the working directory set to the project root.

---

## Contributing

Pull requests welcome! For new features or bug fixes:
- Please lint your code & add meaningful comments.
- Describe your changes and their rationale.
- For major structural changes, open an issue first.

---

## License

MIT

---

## Citation

If you use TherapyGPT in a paper or project, please cite or link to [this repository](https://github.com/NuclearGeekETH/TherapyGPT).

---

### Stay safe. Be well.  
Brought to you by [@NuclearGeekETH](https://github.com/NuclearGeekETH).
