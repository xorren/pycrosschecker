# Python Source Code Plagiarism Similarity Cross-Checker Using Bytecode

This tool detects code plagiarism by comparing `.py` source files and `.pyc` bytecode files.
It supports multiple file formats and comparison directions, allowing you to verify code similarity even when the original source is unavailable.

## Supported File Types

This tool supports analyzing and comparing the following Python-related file types:

- `.py` – Python source code files
- `.pyc` – Compiled Python bytecode files

**Supported Comparison Combinations**

| File Type A | File Type B | Supported | Notes         |
| ----------- | ----------- | --------- | ------------- |
| `.py`     | `.py`     | ✅        |               |
| `.pyc`    | `.py`     | ✅        |               |
| `.pyc`    | `.pyc`    | ✅        |               |
| `.exe`    | `.py`     | ❌        | Not supported |
| `.exe`    | `.pyc`    | ❌        | Not supported |
| `.exe`    | `.exe`    | ❌        | Not supported |

To analyze `.exe` files, please extract `.pyc` files with external tools such as `pyinstxtractor`.

## Installation

```bash
git clone https://github.com/xorren/pycrosschecker.git
cd pycrosschecker
```

## Usage

```bash
python pycrosschecker.py fileA.py fileB.py

or

python pycrosschecker.py fileA.py fileB.pyc

or

python pycrosschecker.py fileA.pyc fileB.pyc
```

## Related Publications

This tool is based on the following research publication.For details on the algorithm and methodology, please refer to the paper below.

> **Implementation of a similarity analysis tool to prevent Python code theft**
> _Heewan Park, Jaeuk Ko, Seongmin Kim, Seungyeon Park, & Junhwi Park_, Proceedings of the Korean Society of Computer Information Conference, 2024-07-11
> [🔗 Link](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE11926165)

## License

This project is licensed under the [AGPLv3 License](LICENSE).

You can redistribute and/or modify it under the terms of the AGPLv3.

This program comes WITHOUT ANY WARRANTY; see [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/) for details.
