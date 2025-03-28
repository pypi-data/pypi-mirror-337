#!/usr/bin/env python3
"""
github_storage.py

A more robust file-based storage system on GitHub. Provides:

- Store, read, update, delete files
- Optional chunking for large files
- Optional compression(zlib)
- Optional AES encryption
- List commit history (versions)
- Revert a file to a previous commit
- A CLI for demonstration

Dependencies:
    pip install PyGithub pycryptodome
"""

import os
import sys
import base64
import zlib
import argparse
from typing import Optional, Union, List, Dict

try:
    from github import Github, GithubException, ContentFile
except ImportError as e:
    raise ImportError("PyGithub is required. Install via 'pip install PyGithub'") from e

try:
    from Crypto.Cipher import AES
except ImportError as e:
    raise ImportError("pycryptodome is required for encryption. Install via 'pip install pycryptodome'") from e


class GitHubStorageError(Exception):
    """Custom exception for GitHubStorage-related errors."""
    pass


def _encrypt(key: bytes, data: bytes) -> bytes:
    """
    Encrypt data using AES (CTR mode) with the given key.
    Returns nonce + ciphertext. Nonce is 16 bytes.
    """
    if len(key) not in (16, 24, 32):
        raise ValueError("Key must be 128, 192, or 256 bits in length.")

    # Use 16-byte random nonce for CTR
    from Crypto.Random import get_random_bytes
    nonce = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    ciphertext = cipher.encrypt(data)
    return nonce + ciphertext


def _decrypt(key: bytes, enc_data: bytes) -> bytes:
    """
    Decrypt data using AES (CTR mode). Expects first 16 bytes as nonce.
    """
    if len(enc_data) < 16:
        raise ValueError("Encrypted data is too short or missing nonce.")
    nonce = enc_data[:16]
    ciphertext = enc_data[16:]
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    return cipher.decrypt(ciphertext)


class GitHubStorage:
    """
    A robust GitHub-based file storage system with optional chunking, compression, and encryption.
    """

    MAX_GITHUB_FILE_SIZE = 95 * 1024 * 1024  # ~95MB safe limit before hitting GitHub's 100MB limit

    def __init__(
        self,
        token: str,
        repo_name: str,
        branch: str = "main",
        chunk_size: int = 50 * 1024 * 1024,
        compression: bool = False,
        encryption_key: Optional[bytes] = None,
    ):
        """
        :param token: A GitHub personal access token (PAT) with repo permissions.
        :param repo_name: "username/repo"
        :param branch: GitHub branch to read/write files.
        :param chunk_size: If >0, files bigger than this are automatically split into multiple parts.
        :param compression: If True, compress data with zlib before storing.
        :param encryption_key: Optional AES key (128/192/256 bits). If provided, data is encrypted.
        """
        self.token = token
        self.repo_name = repo_name
        self.branch = branch
        self.chunk_size = chunk_size
        self.compression = compression
        self.encryption_key = encryption_key

        self._github = Github(token)
        try:
            self._repo = self._github.get_repo(repo_name)
        except GithubException as e:
            raise GitHubStorageError(f"Could not access repo '{repo_name}' with provided token.") from e

    def store_file(self, repo_path: str, local_file_path: str, commit_message: str = "Store file") -> None:
        """
        Upload or update a local file in the GitHub repository. If the file is
        larger than chunk_size, automatically split into chunks.

        :param repo_path: Path in the repo where the file (or chunk folder) will be stored, e.g. "data/video.mp4".
        :param local_file_path: Local file path.
        :param commit_message: Git commit message.
        """
        with open(local_file_path, "rb") as f:
            content = f.read()
        self.store_bytes(repo_path, content, commit_message)

    def store_bytes(self, repo_path: str, data: bytes, commit_message: str = "Store bytes") -> None:
        """
        Upload or update raw bytes as a file in the GitHub repository. Automatically handle
        chunking, compression, and encryption if configured.

        :param repo_path: Where to store the file or chunk directory in the repo.
        :param data: Raw bytes to store.
        :param commit_message: Git commit message.
        """
        # 1) compress if requested
        if self.compression:
            data = zlib.compress(data)

        # 2) encrypt if key provided
        if self.encryption_key:
            data = _encrypt(self.encryption_key, data)

        # 3) If chunk_size is 0 or data below chunk_size, store in a single file
        if self.chunk_size <= 0 or len(data) <= self.chunk_size:
            self._upload_single(repo_path, data, commit_message)
            # delete old chunk folder if it exists
            self._cleanup_chunk_folder(repo_path)
            return

        # Else store as multiple chunks in a dedicated folder
        folder = repo_path + ".chunks"
        # delete existing single file if exists
        self._delete_file(repo_path, "Remove old single file for chunked storage.")

        # chunk the data
        chunks = [data[i : i + self.chunk_size] for i in range(0, len(data), self.chunk_size)]
        # upload each chunk
        for idx, chunk in enumerate(chunks):
            chunk_path = f"{folder}/part_{idx}"
            self._upload_single(chunk_path, chunk, f"{commit_message} (part {idx}/{len(chunks)-1})")

        # optionally, store a small "manifest" with metadata
        manifest_data = f"num_chunks={len(chunks)}\noriginal_name={os.path.basename(repo_path)}"
        self._upload_single(f"{folder}/manifest.txt", manifest_data.encode("utf-8"), f"Upload manifest for {repo_path}")

    def read_file(self, repo_path: str) -> bytes:
        """
        Read a file (or chunked file) from GitHub and return as raw bytes.
        Decompress/decrypt if needed.

        :param repo_path: Path in the repo where the file or chunk folder lives.
        :return: The raw file content as bytes.
        :raises FileNotFoundError if the file or chunk folder doesn't exist.
        """
        # first check if chunk folder exists
        folder = repo_path + ".chunks"
        try:
            chunk_listing = self._repo.get_contents(folder, ref=self.branch)
            if not isinstance(chunk_listing, list):
                chunk_listing = [chunk_listing]
            # We have a chunked file
            # read all parts, sort them by part_{idx}
            parts = [c for c in chunk_listing if c.type == "file" and c.path.endswith("part_")]
            # sort by the part index
            parts_sorted = sorted(parts, key=lambda x: int(x.path.split("_")[-1]))
            data = b""
            for p in parts_sorted:
                part_bytes = p.decoded_content
                data += part_bytes

            # Decompress decrypt
            data = self._postprocess(data)
            return data
        except GithubException as e:
            # If 404, maybe it's a single file. We'll handle that next.
            if e.status != 404:
                raise GitHubStorageError(f"Failed to read chunk folder '{folder}'") from e

        # single file fallback
        try:
            file_content = self._repo.get_contents(repo_path, ref=self.branch)
            raw = file_content.decoded_content
            return self._postprocess(raw)
        except GithubException as e:
            if e.status == 404:
                raise FileNotFoundError(f"File or chunk folder '{repo_path}' not found on branch '{self.branch}'.")
            raise GitHubStorageError(f"Error reading file '{repo_path}'") from e

    def delete_file(self, repo_path: str, commit_message: str = "Delete file") -> None:
        """
        Delete a file or chunk folder from the GitHub repository.

        :param repo_path: Path (single file) or chunk folder name without .chunks suffix.
        :param commit_message: Git commit message.
        """
        # If chunk folder exists, remove that
        folder = repo_path + ".chunks"
        try:
            self._delete_folder(folder, commit_message)
        except FileNotFoundError:
            pass  # no chunk folder
        # Also try single file
        try:
            self._delete_file(repo_path, commit_message)
        except FileNotFoundError:
            pass  # already doesn't exist

    def list_versions(self, repo_path: str, limit: int = 10) -> List[Dict[str, str]]:
        """
        List recent commit history (versions) for a file *or* a chunk folder.

        :param repo_path: The path in the repo to examine. e.g. "data/file.txt".
        :param limit: How many commit entries to return.
        :return: A list of dicts with keys: "sha", "author", "date", "message"
        """
        path_to_check = repo_path
        # If chunk folder exists, prefer listing that
        if self._path_exists(repo_path + ".chunks"):
            path_to_check = repo_path + ".chunks"

        # Retrieve commit history for the path
        commits = self._repo.get_commits(path=path_to_check, sha=self.branch)[:limit]
        history = []
        for c in commits:
            history.append({
                "sha": c.sha,
                "author": c.author.login if c.author else "unknown",
                "date": c.commit.author.date.isoformat(),
                "message": c.commit.message
            })
        return history

    def revert_to_version(self, repo_path: str, sha: str, commit_message: str = "Revert file to older version") -> None:
        """
        Revert a file (or chunk folder) to an older commit. This effectively fetches
        the older content and re-uploads it as a new commit.

        :param repo_path: Path or base path if chunked.
        :param sha: The commit SHA to revert to.
        :param commit_message: New commit message for the reversion.
        """
        # read old content
        # checkout (or get) the content from that SHA.
        path_to_check = repo_path
        if self._path_exists(repo_path + ".chunks"):
            path_to_check = repo_path + ".chunks"

        # get file/folder from that older commit
        try:
            # We can fetch the old tree via get_git_tree, but let's do simpler approach:
            # 1) get the old commit
            commit = self._repo.get_commit(sha=sha)
        except GithubException as e:
            raise GitHubStorageError(f"Commit with SHA={sha} not found.") from e

        # We'll attempt to read from that commit's tree. Let's do a fallback approach:
        old_data = self._download_from_commit(commit, path_to_check)

        # Now we store it again at the same path
        # If chunked, we store the entire folder data. If single, store single file.
        # However, this approach lumps all chunks into one big bytes object if chunked.
        # If we want chunked output again, we can re-chunk it via store_bytes.
        if path_to_check.endswith(".chunks"):
            # it's chunked
            # no single direct file at this path
            # We'll re-store as chunked automatically if needed
            self.store_bytes(repo_path, old_data, commit_message)
        else:
            # single file
            self.store_bytes(repo_path, old_data, commit_message)

    # ----------------- Internal Helpers ----------------- #

    def _upload_single(self, path: str, content: bytes, commit_message: str) -> None:
        """
        Upload or update a single file (no chunk splitting) in the repo.
        Raises an exception if there's a commit conflict.
        """
        try:
            existing_file = self._repo.get_contents(path, ref=self.branch)
            # If it exists, update it
            self._repo.update_file(
                path=existing_file.path,
                message=commit_message,
                content=content,
                sha=existing_file.sha,
                branch=self.branch
            )
        except GithubException as e:
            if e.status == 404:
                # create new
                self._repo.create_file(
                    path, commit_message, content, branch=self.branch
                )
            else:
                # Possibly a conflict or other error
                raise GitHubStorageError(f"Failed to upload/update '{path}'") from e

    def _delete_file(self, path: str, commit_message: str) -> None:
        """
        Delete a single file (no chunk folder) from the repo.
        Raises FileNotFoundError if the file is missing.
        """
        try:
            existing_file = self._repo.get_contents(path, ref=self.branch)
            self._repo.delete_file(
                path=existing_file.path,
                message=commit_message,
                sha=existing_file.sha,
                branch=self.branch
            )
        except GithubException as e:
            if e.status == 404:
                raise FileNotFoundError(f"File '{path}' not found.")
            raise GitHubStorageError(f"Failed to delete '{path}'") from e

    def _delete_folder(self, folder_path: str, commit_message: str) -> None:
        """
        Recursively delete a folder in the repo by listing contents and deleting each file.
        Raises FileNotFoundError if the folder doesn't exist.
        """
        try:
            contents = self._repo.get_contents(folder_path, ref=self.branch)
            if not isinstance(contents, list):
                contents = [contents]
        except GithubException as e:
            if e.status == 404:
                raise FileNotFoundError(f"Folder '{folder_path}' not found.")
            raise GitHubStorageError(f"Error reading folder '{folder_path}'") from e

        for c in contents:
            if c.type == "dir":
                self._delete_folder(c.path, commit_message)
            else:
                try:
                    self._repo.delete_file(
                        path=c.path,
                        message=commit_message,
                        sha=c.sha,
                        branch=self.branch
                    )
                except GithubException as e:
                    if e.status != 404:
                        raise GitHubStorageError(f"Failed to delete '{c.path}'") from e

    def _cleanup_chunk_folder(self, repo_path: str) -> None:
        """If a chunk folder exists for the given path, remove it."""
        folder = repo_path + ".chunks"
        try:
            self._delete_folder(folder, commit_message="Removing old chunk folder")
        except FileNotFoundError:
            pass

    def _path_exists(self, path: str) -> bool:
        """Check if a file or folder path exists in the repo."""
        try:
            self._repo.get_contents(path, ref=self.branch)
            return True
        except GithubException as e:
            if e.status == 404:
                return False
            raise

    def _postprocess(self, data: bytes) -> bytes:
        """
        Decrypt (if needed) and decompress (if needed) in the correct order.
        """
        if self.encryption_key:
            data = _decrypt(self.encryption_key, data)
        if self.compression:
            data = zlib.decompress(data)
        return data

    def _download_from_commit(self, commit, path: str) -> bytes:
        """
        Recursively read all files in `path` from a specific commit's tree, combine them (for chunked),
        and return as bytes. If single file, just return that file content.
        """
        # Check if path is a folder in that commit or single file
        tree = commit.commit.tree
        # We can walk the tree looking for path
        # For chunked data, path is a folder
        # For single file, path is a single item
        path_parts = path.split("/")
        item = self._find_in_tree(tree, path_parts)
        if item is None:
            raise FileNotFoundError(f"Path '{path}' not found in commit {commit.sha}.")

        if item.type == "blob":
            # single file
            content = item.decoded_content
            return content
        elif item.type == "tree":
            # chunk folder
            # gather all parts
            # load them in sorted order
            chunk_blobs = [child for child in item._tree if child.type == "blob" and child.path.endswith("part_")]
            chunk_blobs_sorted = sorted(chunk_blobs, key=lambda x: int(x.path.split("_")[-1]))
            data = b""
            for blob in chunk_blobs_sorted:
                data += blob.decoded_content
            return data
        else:
            raise GitHubStorageError(f"Cannot download from item type '{item.type}'")

    def _find_in_tree(self, tree, path_parts: List[str]):
        """
        Navigate the Git tree objects based on path_parts and return the final object (blob or tree).
        Returns None if not found.
        """
        if not path_parts:
            return None
        head = path_parts[0]
        rest = path_parts[1:]
        for element in tree._tree:
            if element.path == head:
                if rest:
                    if element.type == "tree":
                        return self._find_in_tree(element, rest)
                    return None
                else:
                    return element
        return None


# -----------------------------------------------------------
# OPTIONAL: A simple CLI for demonstration
# -----------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="GitHub Storage CLI")
    parser.add_argument("--token", required=True, help="GitHub Personal Access Token")
    parser.add_argument("--repo", required=True, help="GitHub repo name, e.g. username/myrepo")
    parser.add_argument("--branch", default="main", help="Branch name, default=main")
    parser.add_argument("--compression", action="store_true", help="Enable zlib compression")
    parser.add_argument("--encrypt-key", help="Hex-encoded AES key for encryption (128/192/256 bits).")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # store-file
    store_file_parser = subparsers.add_parser("store-file", help="Upload a local file to the repo.")
    store_file_parser.add_argument("repo_path", help="Path in the repo to store the file.")
    store_file_parser.add_argument("local_file_path", help="Local file to read from.")
    store_file_parser.add_argument("--msg", default="Store file", help="Commit message.")

    # store-bytes (like store-file, but from a string)
    store_bytes_parser = subparsers.add_parser("store-bytes", help="Store raw bytes (from a string).")
    store_bytes_parser.add_argument("repo_path", help="Path in the repo.")
    store_bytes_parser.add_argument("content_string", help="String to store. Will be converted to bytes.")
    store_bytes_parser.add_argument("--msg", default="Store bytes", help="Commit message.")

    # read-file
    read_parser = subparsers.add_parser("read-file", help="Read file from the repo and print to stdout.")
    read_parser.add_argument("repo_path", help="Path in the repo to read.")
    read_parser.add_argument("--save-to", help="Optional local file to save the content.")

    # delete-file
    delete_parser = subparsers.add_parser("delete-file", help="Delete file or chunk folder from the repo.")
    delete_parser.add_argument("repo_path", help="Path in the repo to delete.")
    delete_parser.add_argument("--msg", default="Delete file", help="Commit message.")

    # list-versions
    history_parser = subparsers.add_parser("list-versions", help="List commit history for a path.")
    history_parser.add_argument("repo_path", help="Repo path to check.")
    history_parser.add_argument("--limit", type=int, default=10, help="Number of history entries.")

    # revert
    revert_parser = subparsers.add_parser("revert", help="Revert a file to a previous commit (by SHA).")
    revert_parser.add_argument("repo_path", help="Path to revert.")
    revert_parser.add_argument("sha", help="Commit SHA to revert to.")
    revert_parser.add_argument("--msg", default="Revert file to older version", help="Commit message.")

    args = parser.parse_args()

    # Build encryption key if provided
    encryption_key = None
    if args.encrypt_key:
        try:
            encryption_key = bytes.fromhex(args.encrypt_key)
        except ValueError:
            print("Invalid encryption key hex. Must be hex-encoded string.")
            sys.exit(1)

    storage = GitHubStorage(
        token=args.token,
        repo_name=args.repo,
        branch=args.branch,
        compression=args.compression,
        encryption_key=encryption_key
    )

    if args.command == "store-file":
        storage.store_file(args.repo_path, args.local_file_path, args.msg)

    elif args.command == "store-bytes":
        storage.store_bytes(args.repo_path, args.content_string.encode("utf-8"), args.msg)

    elif args.command == "read-file":
        content = storage.read_file(args.repo_path)
        if args.save_to:
            with open(args.save_to, "wb") as f:
                f.write(content)
            print(f"Saved to {args.save_to}")
        else:
            # print as string if it's likely text, else base64
            try:
                as_str = content.decode("utf-8")
                print(as_str)
            except UnicodeDecodeError:
                print(base64.b64encode(content).decode("utf-8"))

    elif args.command == "delete-file":
        storage.delete_file(args.repo_path, args.msg)

    elif args.command == "list-versions":
        history = storage.list_versions(args.repo_path, args.limit)
        for entry in history:
            print(f"{entry['sha']} | {entry['author']} | {entry['date']} | {entry['message']}")

    elif args.command == "revert":
        storage.revert_to_version(args.repo_path, args.sha, args.msg)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
