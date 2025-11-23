import os
import re
from typing import Dict, Iterable, Tuple

import pandas as pd


def _iter_sessions(folder: str) -> Iterable[Tuple[str, str, str]]:
    """Yield (subject, date, text block) for each session in the folder."""
    for fn in os.listdir(folder):
        if fn.startswith("!") and fn.lower().endswith(".txt"):
            with open(os.path.join(folder, fn), encoding="utf8") as f:
                text = f.read()
            for blk in re.split(r"(?=Start Date:)", text):
                if not blk.strip().startswith("Start Date:"):
                    continue
                m_date = re.search(r"Start Date:\s*(\d\d)/(\d\d)/(\d\d)", blk)
                subj = re.search(r"Subject:\s*(\S+)", blk).group(1)
                date = f"20{m_date.group(3)}-{m_date.group(1)}-{m_date.group(2)}"
                yield subj, date, blk


def _parse_letter_block(block: str, letter: str) -> Dict[int, float]:
    """Return a mapping of index->value for a given lettered section (e.g., D:, G:)."""
    values: Dict[int, float] = {}
    in_section = False
    for line in block.splitlines():
        if line.startswith(f"{letter}:"):
            in_section = True
            continue
        if not in_section:
            continue
        if not line.startswith("    "):
            break
        mi = re.match(r"\s*(\d+):\s*(.*)", line)
        if not mi:
            continue
        idx = int(mi.group(1))
        nums = [float(x) for x in mi.group(2).split()]
        for offset, val in enumerate(nums):
            values[idx + offset] = val
    return values


# Control/session parameters (A)
A_NAMES = [
    "Trials to Run",
    "Response (Limited Hold) Time (sec)",
    "Time Out (sec)",
    "Reward (1=Pellet  2=Dipper)",
    "Reward Duration (sec)",
    "Session Time (min)",
]


def extract_a(folder: str) -> pd.DataFrame:
    """Parse all !*.txt files in folder for "A:" blocks (control vars)."""
    rows = []
    for subj, date, blk in _iter_sessions(folder):
        avals = _parse_letter_block(blk, "A")
        row = {"Subject": subj, "Date": date}
        for i, name in enumerate(A_NAMES):
            row[name] = avals.get(i)
        rows.append(row)
    return pd.DataFrame(rows).sort_values(["Subject", "Date"]).reset_index(drop=True)


# Summary response stats (D)
D_NAMES = [
    "Correct Responses",
    "Incorrect Responses",
    "Omissions",
    "Premature ITI Wall Responses",
    "Perseverant Responses",
    "Time Out Responses",
    "Total Receptacle Head Entries",
    "Total Wall Entries",
    "D8_NotUsed",
    "D9_NotUsed",
    "D10_NotUsed",
    "D11_NotUsed",
    "D12_NotUsed",
    "Reward Port Head Entries During TimeOut (Incorrect/Omission)",
    "Wall Head Entries During TimeOut (Incorrect/Omission)",
    "Reward Port Head Entries During TimeOut (Premature)",
    "Wall Head Entries During TimeOut (Premature)",
    "Reward Port Head Entries During Tone Trials",
    "Wall Head Entries During Tone Trials",
    "Initiated Trials",
    "Passive Trials",
    "Time (sec)",
]


def extract_d(folder: str) -> pd.DataFrame:
    """Parse all !*.txt files in folder for "D:" summary stats."""
    sessions = []
    for subj, date, blk in _iter_sessions(folder):
        dvals = _parse_letter_block(blk, "D")
        row = {"Subject": subj, "Date": date}
        for i, name in enumerate(D_NAMES):
            row[name] = dvals.get(i)
        sessions.append(row)
    return pd.DataFrame(sessions).sort_values(["Subject", "Date"]).reset_index(drop=True)


# Summary latency data (G)
G_NAMES = [
    "Average Latency to Correct Response",
    "Average Latency to Incorrect Response",
    "Average Latency to Reward",
    "G3_NotUsed",
    "G4_NotUsed",
    "Total Latency Time to Correct Response",
    "Total Latency Time to Incorrect Response",
    "Total Latency Time to Reward",
]


def extract_g(folder: str) -> pd.DataFrame:
    """Parse all !*.txt files in folder for "G:" latency blocks."""
    rows = []
    for subj, date, blk in _iter_sessions(folder):
        gvals = _parse_letter_block(blk, "G")
        row = {"Subject": subj, "Date": date}
        for i, name in enumerate(G_NAMES):
            row[name] = gvals.get(i)
        rows.append(row)
    return pd.DataFrame(rows).sort_values(["Subject", "Date"]).reset_index(drop=True)


# Trial-by-trial (K)
K_NAMES = [
    "Trial Number",
    "Nose Poke Stimulus Location (1-5)",
    "First Response to Stimulus (1-5,0=Omission)",
    "Correct Response Latency",
    "Incorrect Response Latency",
    "Latency to Reward",
    "Omission Error",
    "Perseverant Responses to NP #1",
    "Perseverant Responses to NP #2",
    "Perseverant Responses to NP #3",
    "Perseverant Responses to NP #4",
    "Perseverant Responses to NP #5",
    "Trial type Tone or No Tone (0=No Tone,1=Tone)",
    "Timestamp of Light Cue Onset",
    "Timestamp of Tone Onset",
    "Tipo de recompensa (0=small,1=large)",
    "Premature ITI Responses",
    "Time Out Responses",
    "All Receptacle Head Entries (Trial By Trial)",
    "Cue Duration",
    "ITI Duration",
    "Modo de ensayo (0=SIMPLE,1=DUAL)",
    "Trial type (1 normal, 0 forced)",
    "Timestamp of Trial Start",
    "Reward Retrieval Omission (1=yes,0=no)",
    "Number of Times Dipper Goes Up",
    "Timestamp of Head Entry to Reward Port After Correct Response",
    "Head Entries to Reward During Time Out (trial level)",
    "Head Entries to Wall During Time Out (trial level)",
    "Head Entries to Reward During Time Out for Premature Trials",
    "Head Entries to Wall During Time Out for Premature Trials",
    "Head Entries to Reward Port During Tone-Only Trials",
    "Head Entries to Wall During Tone-Only Trials",
    "Prior Trial Initiation Entries into Reward Port",
    "Prior Trial Initiation Entries into Wall",
    "Timestamp of End of Trial",
]


def extract_k(folder: str) -> pd.DataFrame:
    """Parse all !*.txt files in folder for "K:" trial-by-trial blocks."""
    rows = []
    for subj, date, blk in _iter_sessions(folder):
        kvals = _parse_letter_block(blk, "K")
        if not kvals:
            continue
        max_idx = max(kvals)
        values = [None] * (max_idx + 1)
        for idx, val in kvals.items():
            values[idx] = val
        for i in range(0, len(values), len(K_NAMES)):
            row_vals = values[i : i + len(K_NAMES)]
            if all(v is None for v in row_vals):
                continue
            row = {"Subject": subj, "Date": date}
            for j, name in enumerate(K_NAMES):
                row[name] = row_vals[j] if j < len(row_vals) else None
            rows.append(row)
    return (
        pd.DataFrame(rows)
        .sort_values(["Subject", "Date", "Trial Number"])
        .reset_index(drop=True)
    )
