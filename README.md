<div align="center">
    <img alt="senju logo" src="./docs/source/_static/kanji.png
" width="60%"/>
    <h1>千手 Senju</h1>
    <h3>🎋 Poetry in Motion 🎎</h3>
    <p>
        A web service for Haiku generation from text or from images and Haiku
        sharing
    </p>
    <br/>
    <a href="https://codecov.io/gh/senju1337/senju">
        <img src="https://codecov.io/gh/senju1337/senju/branch/master/graph/badge.svg" alt="Code Coverage"/>
    </a>
    <a href="https://github.com/senju1337/senju/actions">
        <img src="https://img.shields.io/github/actions/workflow/status/senju1337/senju/python.yml?label=Python%20CI" alt="Build Status"/>
    </a>
    <a href="https://github.com/senju1337/senju/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/senju1337/senju" alt="License"/>
    </a>
    <a href="https://github.com/senju1337/senju/releases">
        <img src="https://img.shields.io/github/v/release/senju1337/senju" alt="Release"/>
    </a>
    <br/>
    <a href="https://python.org">
        <img src="https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-blue?logo=python&logoColor=white" alt="Python Versions"/>
    </a>
    <a href="https://flask.palletsprojects.com/">
        <img src="https://img.shields.io/badge/Powered%20by-Flask-black?logo=flask&logoColor=white" alt="Powered by Flask"/>
    </a>
    <a href="https://pytorch.org/">
        <img src="https://img.shields.io/badge/AI-PyTorch-EE4C2C?logo=pytorch&logoColor=white" alt="AI PyTorch"/>
    </a>
</div>

## 🌊 Overview

Senju (千手, "thousand hands") is a web service for haiku poetry generation and sharing, with image-to-haiku functionality.

## ✨ Features

- **🎏 AI-Powered Haiku Generation**: Create beautiful three-line haiku poetry from text prompts
- **🖼️ Image-to-Haiku**: Turn uploaded images into poetic haiku (experimental)
- **🔍 Browse Existing Haiku**: Gallery view of previously generated poetry
- **💾 Persistent Storage**: All generated haiku are stored for future retrieval
- **🖥️ Web Interface**: Clean, efficient, minimalist user experience for human interaction

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/senju1337/senju.git
cd senju

docker compose up
```

### 📋 Dependencies

- Python
- Flask
- TinyDB
- PyTorch
- Transformers
- Pillow

See `pyproject.toml` for a complete list of dependencies.

## 🏯 Architecture

Senju is built around several key components:

- **Flask Application**: Core web framework providing routing and template rendering
- **Haiku Generator**: Interfaces with a machine learning model for poetry creation
- **Image Recognition**: Vision-language model for extracting descriptions from images
- **Storage Manager**: TinyDB-based persistence layer for haiku retrieval and storage

## 📝 Documentation

Senju is documented with sphinx. The documentation of the latest release is
available on [github-pages](https://senju1337.github.io/senju/).

It can be generated like this (after installing the dependencies, see above):

```bash
cd docs
bash auto_docu.sh
# now open the documentation with a web browser of your choice
firefox ./build/html/
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run tests with coverage
bash coverage.sh
```

## 📜 License

Distributed under the GPL-3 License. See `LICENSE` for more information.

## 🙏 Acknowledgements

- [Ollama](https://ollama.ai/) for providing the AI backend
- [BLIP](https://github.com/salesforce/BLIP) for the image captioning model
- [PyTorch](https://pytorch.org/) and [Transformers](https://huggingface.co/docs/transformers/index) for ML infrastructure
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [TinyDB](https://tinydb.readthedocs.io/) for the document database

<hr>

<div align="center">
    <i>Purple petals rise<br>
    Defying fragile beauty<br>
    Fiercely breathing life</i>
</div>
