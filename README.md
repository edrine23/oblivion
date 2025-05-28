# Oblivion v3.0

Oblivion is a modern web penetration testing tool designed for ethical security researchers. Version **3.0** introduces:

- ⚡ Asynchronous operations
- 🔌 A modular plugin system
- 📄 Rich reporting capabilities
- 🧠 Advanced modules for recon, web attacks, brute-forcing, OSINT, and utilities

---

## 🚀 Installation
```bash
pip install -r requirements.txt
```

---

## 🧰 Usage
```bash
python oblivion.py start
```

---

## 🧩 Modules

### 🔍 Recon
- Subdomain enumeration
- Cloud asset discovery
- Certificate transparency log parsing

### 🌐 Web
- GraphQL testing
- API security fuzzing
- WebSocket testing
- SQL injection
- XSS detection

### 🔐 Brute
- Parallel login brute-forcing
- Smart wordlist generation

### 🕵️ OSINT
- Social media profiling
- Dark web search
- Email breach lookups

### 🛠 Utils
- Password generator
- Payload generator
- JWT tester
- File fuzzer

---

## 🔌 Plugins
To extend Oblivion, drop your plugins into the `plugins/` directory.

**Example Plugin**:
```python
from core.plugin_loader import Plugin
import click

class SamplePlugin(Plugin):
    def execute(self, args: dict) -> None:
        click.echo(f"Executing with args: {args}")

    def register_commands(self, cli_group: click.Group) -> None:
        @cli_group.command(name="sample")
        @click.option('--target', type=str)
        def sample_command(target: str) -> None:
            self.execute({"target": target})
```

---

## 🧪 Testing
Run unit tests with:
```bash
pytest tests/
```

---

## ⚠️ Ethical Usage
Oblivion is intended strictly for **authorized security testing** only.

> 🚨 Use it only on systems you own or have **explicit written permission** to test. Unauthorized use is illegal.

---

## 🤝 Contributing
- Fork the repo and submit PRs
- Add plugins under `plugins/`
- Propose and contribute new modules

---

## 📄 License
MIT License
