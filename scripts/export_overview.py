#!/usr/bin/env python3
"""Assemble the collaborator-facing overview doc from the vault.

The vault (vault/) is the source of truth; this builds build/overview.md,
which gets pushed to the shared Google Doc (see vault/07 Production/Sync
Workflow.md). Wikilinks become plain bold text; frontmatter is stripped.

Usage: python3 scripts/export_overview.py
"""
import os
import re
import subprocess
from datetime import date

ROOT = os.path.join(os.path.dirname(__file__), "..")
VAULT = os.path.join(ROOT, "vault")

# Order of sections in the Doc (vault-relative paths)
SECTIONS = [
    "01 Overview/Premise.md",
    "01 Overview/Themes & Pillars.md",
    "01 Overview/Story Structure.md",
    "01 Overview/Game Systems.md",
    "02 Characters/Ash El.md",
    "02 Characters/Lay-Lay.md",
    "02 Characters/Xochtl.md",
    "02 Characters/The Player.md",
    "02 Characters/Maya.md",
    "02 Characters/Jordan.md",
    "02 Characters/Alex.md",
    "02 Characters/Vera.md",
    "02 Characters/Spectre.md",
    "02 Characters/Atlas.md",
    "03 Chapters/Chapter 1 - Genesis Block.md",
    "03 Chapters/Chapter 2 - Token Generation Event.md",
    "03 Chapters/Chapter 3 - Governance Wars.md",
    "03 Chapters/Chapter 4 - The Attack.md",
    "03 Chapters/Chapter 5 - Resolution.md",
    "04 Endings/Endings Overview.md",
    "05 Lessons/Lessons Index.md",
    "06 Assets/Art Style Guide.md",
    "06 Assets/Asset List.md",
]


def clean(md):
    md = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S)          # frontmatter
    md = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"**\2**", md)     # [[x|y]] -> y
    md = re.sub(r"\[\[([^\]]+)\]\]", r"**\1**", md)                # [[x]] -> x
    md = re.sub(r"```mermaid\n(.*?)```", r"```\n\1```", md, flags=re.S)  # plain code fence
    # demote headings one level so the doc title stays the only H1
    md = re.sub(r"^(#{1,5}) ", r"#\1 ", md, flags=re.M)
    # Google Docs markdown import chokes on these two: emoji outside the BMP
    # arrive mojibake'd, and bold inside table cells renders as literal \*\*.
    md = re.sub(r"[\U00010000-\U0010FFFF]", "", md)                # strip astral emoji
    md = "\n".join(
        line.replace("**", "") if line.lstrip().startswith("|") else line
        for line in md.split("\n")
    )
    return md.strip()


def main():
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        sha = "uncommitted"
    parts = [
        "# DAOCUBATOR / \"Get Rich Together\" — Visual Novel Overview\n",
        f"*Generated from the Obsidian vault on {date.today().isoformat()} "
        f"(git {sha}). The vault is the source of truth — comment freely here; "
        "edits get folded back into the vault on each design pass. "
        "See vault/07 Production/Sync Workflow.md.*\n",
    ]
    for rel in SECTIONS:
        path = os.path.join(VAULT, rel)
        with open(path, encoding="utf-8") as f:
            parts.append(clean(f.read()))
        parts.append("\n---\n")
    out_dir = os.path.join(ROOT, "build")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "overview.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print(out, f"({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
