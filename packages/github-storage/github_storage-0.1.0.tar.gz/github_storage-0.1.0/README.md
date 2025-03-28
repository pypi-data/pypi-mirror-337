
# GitHubStorage

A robust and extensible file-based storage system built on GitHub repositories. Supports large file handling with optional compression, encryption, chunking, and version control using commit history. Includes a powerful CLI for ease of use.

---

## ✨ Features

- ✅ Upload, update, read, and delete files in a GitHub repository
- 📦 Automatic chunking for large files (>50MB)
- 🗜️ Optional zlib compression
- 🔐 Optional AES encryption (CTR mode)
- 🕒 List version history via Git commit logs
- 🔄 Revert files to previous versions by commit SHA
- 🖥️ CLI for basic operations

---

## 📦 Installation

```bash
pip install github-storage
```

---

## 🚀 Getting Started

### 1. **Basic Usage (as a Python library)**

```python
from github_storage import GitHubStorage

storage = GitHubStorage(
    token="your_github_token",
    repo_name="username/repo",
    compression=True,
    encryption_key=b"16_or_24_or_32_byte_key"
)

# Upload file
storage.store_file("data/file.txt", "local/path/file.txt")

# Read file
data = storage.read_file("data/file.txt")

# Delete file
storage.delete_file("data/file.txt")

# List versions
versions = storage.list_versions("data/file.txt")

# Revert to specific version
storage.revert_to_version("data/file.txt", sha="commit_sha")
```

---

## 🧪 CLI Usage

```bash
python github_storage.py --token <GH_TOKEN> --repo <username/repo> [options] <command>
```

### CLI Arguments

| Flag                | Description                                         |
|---------------------|-----------------------------------------------------|
| `--token`           | Your GitHub Personal Access Token                  |
| `--repo`            | Target GitHub repo (e.g. `user/repo`)              |
| `--branch`          | Target branch (default: `main`)                    |
| `--compression`     | Enable compression (zlib)                          |
| `--encrypt-key`     | AES encryption key (hex-encoded string)           |

### CLI Commands

#### `store-file`

Upload a local file to GitHub.

```bash
python github_storage.py --token TOKEN --repo user/repo store-file <repo_path> <local_file_path> [--msg "commit message"]
```

#### `store-bytes`

Store a string as bytes in GitHub.

```bash
python github_storage.py --token TOKEN --repo user/repo store-bytes <repo_path> <content_string>
```

#### `read-file`

Read a file and print or save locally.

```bash
python github_storage.py --token TOKEN --repo user/repo read-file <repo_path> [--save-to local_path]
```

#### `delete-file`

Delete a file or chunked file.

```bash
python github_storage.py --token TOKEN --repo user/repo delete-file <repo_path>
```

#### `list-versions`

List recent commit history for a path.

```bash
python github_storage.py --token TOKEN --repo user/repo list-versions <repo_path> [--limit 5]
```

#### `revert`

Revert a file to a previous version using commit SHA.

```bash
python github_storage.py --token TOKEN --repo user/repo revert <repo_path> <commit_sha>
```

---

## 🔐 Encryption & Compression

- **Encryption**: AES in CTR mode; use 16, 24, or 32 byte key (128, 192, 256 bits).
- **Compression**: zlib compression; efficient for text or repetitive binary data.
- **Chunking**: Enabled automatically for files larger than `chunk_size` (default: 50MB).

---

## 📁 Chunking Behavior

- Files larger than `chunk_size` are split into parts and stored under a `.chunks` folder in the repo.
- A `manifest.txt` file is added to describe the chunked structure.
- Old single files or chunk folders are automatically cleaned up.

---

## ⚠️ Limitations

- Max GitHub file size: 100MB per file (we use 95MB to be safe).
- Requires a repo with appropriate write permissions via GitHub token.
- File size and repo quota limits still apply.

---

## ✅ Requirements

- Python 3.6+
- [`PyGithub`](https://pypi.org/project/PyGithub/)
- [`pycryptodome`](https://pypi.org/project/pycryptodome/)

Install them with:

```bash
pip install PyGithub pycryptodome
```

---

## 🧑‍💻 License

MIT License

---

## 📬 Contributing

Pull requests, issues, and suggestions are welcome! Open an issue or fork the project to contribute.

---
