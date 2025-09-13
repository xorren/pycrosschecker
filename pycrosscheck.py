"""
Python Source Code Plagiarism Similarity Cross-Checker Using Bytecode v2.0

Author  : zcake1113@naver.com
Date    : 2025-09-13
URL     : https://github.com/xorren/python-similarity-using-bytecode

A bytecode-level cross-checking tool to detect code similarity and potential plagiarism between Python source (.py) and compiled (.pyc) files using startline-based comparison.
Executable files (.exe) are not supported. To analyze .exe files, extract .pyc files using tools like pyinstxtractor.

Usage: Put this code in the same folder as the file to compare, then run the following.

python pycodeplagcheck.py fileA.py fileB.py
python pycodeplagcheck.py fileA.py fileB.pyc
python pycodeplagcheck.py fileA.pyc fileB.pyc


Licensed under the GNU Affero General Public License v3 or later.
You can redistribute and/or modify it under the terms of the AGPLv3.
This program comes WITHOUT ANY WARRANTY; see <https://www.gnu.org/licenses/> for details.
"""


import sys
import os
import dis
import marshal
import types


def load_code_object(file_path):
    ext = os.path.splitext(file_path)[1]
    try:
        if ext == '.py':
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            return compile(code, file_path, 'exec')
        elif ext == '.pyc':
            with open(file_path, 'rb') as f:
                f.read(16)
                return marshal.load(f)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    except Exception as e:
        print(f"[Error] {e}")
        sys.exit(1)


def extract_opnames(code_obj):
    opnames = []

    def _extract(code, line=None):
        for instr in dis.Bytecode(code):
            opnames.append((instr.starts_line, instr.opname))
            if isinstance(instr.argval, types.CodeType):
                _extract(instr.argval)

    _extract(code_obj)
    return opnames


def group_by_line(opname_seq):
    sgrams = []
    current = []

    for line, opname in opname_seq:
        if line is not None:
            if current:
                sgrams.append(current)
            current = [opname]
        else:
            current.append(opname)

    if current:
        sgrams.append(current)

    return sgrams


def longest_common_subsequence(seq1, seq2):
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m):
        for j in range(n):
            if seq1[i] == seq2[j]:
                dp[i+1][j+1] = dp[i][j] + 1
            else:
                dp[i+1][j+1] = max(dp[i][j+1], dp[i+1][j])

    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if seq1[i-1] == seq2[j-1]:
            lcs.append(seq1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] >= dp[i][j-1]:
            i -= 1
        else:
            j -= 1

    lcs.reverse()
    return lcs


def compute_similarity(sgram1, sgram2, lcs):
    len1 = sum(len(s) for s in sgram1)
    len2 = sum(len(s) for s in sgram2)
    lcs_len = sum(len(s) for s in lcs)

    denominator = min(len1, len2)
    similarity = lcs_len / denominator if denominator else 0
    return similarity, lcs_len, len1, len2


def analyze_files(file1, file2):
    code1 = load_code_object(file1)
    code2 = load_code_object(file2)

    opnames1 = extract_opnames(code1)
    opnames2 = extract_opnames(code2)

    sgram1 = group_by_line(opnames1)
    sgram2 = group_by_line(opnames2)

    lcs = longest_common_subsequence(sgram1, sgram2)

    similarity, lcs_weight, weight1, weight2 = compute_similarity(sgram1, sgram2, lcs)

    return similarity, lcs_weight, weight1, weight2


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare.py <file1.py/pyc> <file2.py/pyc>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    sim, lcs_len, w1, w2 = analyze_files(file1, file2)
    print(f"{file1} vs {file2} - LCS Similarity: {sim:.4f} "
          f"(LCS length: {lcs_len}, file1: {w1}, file2: {w2})")
