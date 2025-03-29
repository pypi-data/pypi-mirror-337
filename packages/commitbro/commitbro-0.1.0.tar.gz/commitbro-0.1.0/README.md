# 🧠 CommitBro

CommitBro is a privacy-first, local-friendly Git commit message generator that uses modern LLMs like Mistral, Starling, or TinyLlama — all running locally via [Ollama](https://ollama.com), or optionally via a hosted FastAPI backend.

---

## ✨ Features

- 🔐 100% privacy-first — no data leaves your machine
- 🤖 Generates commit messages from `git diff --cached`
- 🎯 Instruction-tuned LLMs: Mistral, TinyLlama, Starling, Gemma, etc.
- 🧠 Optional training from your own commit history
- 🧰 FastAPI backend included (for training and expansion)
- 🌍 Supports multi-language commit messages
- 🐳 Docker-ready for container lovers

---

## 📦 Installation

### 1. Clone and Install (Dev Mode)

```bash
git clone https://github.com/yourusername/commitbro.git
cd commitbro
pip install -e .
```

> Requires Python 3.12+, [Ollama](https://ollama.com), and `git`.

### 2. Run Setup

```bash
commitbro-setup
```

Choose:
- Your preferred language (e.g. English, Spanish, Hindi)
- Whether to train models (locally, remotely, or skip)
- Your preferred model (`mistral`, `tinyllama`, etc.)

---

## 🚀 Usage

1. Stage your changes:
   ```bash
   git add .
   ```

2. Generate commit message:
   ```bash
   commitbro
   ```

3. Accept, regenerate, or cancel:
   ```
   Suggested Commit Message:
   > Fix user login state handling on timeout

   ✅ Accept this? [y/n/r]: 
   ```

4. If accepted, CommitBro will automatically commit your changes.

---

## ⚙️ Configuration

CommitBro stores user settings in:

```bash
~/.commitgen/config.json
```

Sample config:
```json
{
  "language": "English",
  "training": "none",
  "remote_training_url": "",
  "model": "mistral"
}
```

You can change the model, language, or training config anytime by rerunning:
```bash
commitbro-setup
```

---

## 🧠 Model Support (via Ollama)

Run any local model supported by [Ollama](https://ollama.com):

| Model         | Size   | Speed | Notes                    |
|---------------|--------|-------|--------------------------|
| `tinyllama`   | ~1.1B  | ⚡⚡⚡   | Very fast, small commits |
| `mistral`     | 7B     | ⚡     | General purpose, accurate |
| `starling`    | 7B     | ⚡     | Optimized for dialogue   |
| `phi`         | 2.7B   | ⚡⚡    | Compact + reasoning      |
| `gemma:2b`    | 2B     | ⚡⚡    | Google’s latest compact model |

To pull models:
```bash
ollama pull mistral
ollama run mistral
```

---

## 🛠️ Training

Extract commit history and send to remote training server:

```bash
commitbro-train
```

Only enabled if you selected `remote` or `both` training during setup.

> You can use the included FastAPI server for training endpoints (see below).

---

## 🌐 FastAPI Backend (Optional)

A minimal FastAPI server is included for collecting commit training data.

### Run it locally:
```bash
cd fastapi_server
uvicorn main:app --reload
```

### Available Endpoint:
- `POST /train` — Accepts commit history for training

```json
{
  "commits": [
    {
      "hash": "abc123",
      "message": "Fix bug in login flow",
      "body": "Adjusted redirect logic in session manager"
    }
  ]
}
```

---

## 🐳 Docker Support

Run CommitBro inside a container (CLI mode):

```bash
docker build -t commitbro .
docker run --rm -v $(pwd):/app commitbro
```

Or to expose FastAPI:

```bash
docker run -p 8000:8000 commitbro uvicorn fastapi_server.main:app --host 0.0.0.0 --port 8000
```

---

## 📁 Project Structure

```
commitbro/
  ├── cli.py              # Main CLI logic
  ├── core.py             # Git diff + model API
  ├── train.py            # Training script
  ├── setup_config.py     # First-time setup wizard

fastapi_server/
  └── main.py             # Remote training API

pyproject.toml            # Modern packaging config
Dockerfile                # Optional container setup
README.md                 # You're reading it!
```

---

## 🧰 Packaging & Build

Uses `hatchling` and `pyproject.toml` (PEP 621).

### Install locally:
```bash
pip install -e .
```

---

## 🧪 Roadmap

- [x] CLI with diff-based message generation
- [x] Language + training setup wizard
- [x] Remote FastAPI training backend
- [ ] VS Code extension
- [ ] Frontend (Next.js + ShadCN UI)
- [ ] Auth + analytics-free SaaS version

---

## 🧑‍💻 Author

Built with 💚 by [@aidataguy](https://github.com/aidataguy)

---

## 📜 License

MIT License — do whatever you want, just keep it open.