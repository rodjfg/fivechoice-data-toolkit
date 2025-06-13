import os
import re
import pandas as pd

# Control/session parameters (A)
A_NAMES = [
    "Trials to Run", "Response (Limited Hold) Time (sec)",
    "Time Out (sec)", "Reward (1=Pellet  2=Dipper)",
    "Reward Duration (sec)", "Session Time (min)"
]

def extract_a(folder: str) -> pd.DataFrame:
    """
    Parse all !*.txt files in folder for 'A:' blocks (control vars) and return DataFrame.
    """
    rows = []
    for fn in os.listdir(folder):
        if fn.startswith('!') and fn.lower().endswith('.txt'):
            text = open(os.path.join(folder, fn), encoding='utf8').read()
            parts = re.split(r'(?=Start Date:)', text)
            for blk in parts:
                if not blk.strip().startswith("Start Date:"): continue
                m_date = re.search(r"Start Date:\s*(\d\d)/(\d\d)/(\d\d)", blk)
                date = f"20{m_date.group(3)}-{m_date.group(1)}-{m_date.group(2)}"
                subj = re.search(r"Subject:\s*(\S+)", blk).group(1)
                avals = {}
                inA = False
                for line in blk.splitlines():
                    if line.startswith("A:"): inA = True; continue
                    if inA:
                        if not line.startswith("    "): break
                        mi = re.match(r"\s*(\d+):\s*(.*)", line)
                        if not mi: continue
                        idx = int(mi.group(1))
                        vals = [float(x) for x in mi.group(2).split()]
                        for off, v in enumerate(vals):
                            avals[idx+off] = v
                row = {"Subject": subj, "Date": date}
                for i, name in enumerate(A_NAMES):
                    row[name] = avals.get(i)
                rows.append(row)
    return pd.DataFrame(rows).sort_values(["Subject","Date"]).reset_index(drop=True)

# Summary response stats (D)
D_NAMES = [
    "Correct Responses", "Incorrect Responses", "Omissions",
    "Premature ITI Responses", "Perseverant Responses", "Time Out Responses",
    "Total Receptacle Head Entries", "D7_NotUsed", "D8_NotUsed", "D9_NotUsed",
    "% Correct", "% Incorrect", "% Omission"
]

def extract_d(folder: str) -> pd.DataFrame:
    """
    Parse all !*.txt files in folder for 'D:' summary stats and return DataFrame.
    """
    sessions = []
    for fn in os.listdir(folder):
        if fn.startswith('!') and fn.lower().endswith('.txt'):
            text = open(os.path.join(folder, fn), encoding='utf8').read()
            parts = re.split(r'(?=Start Date:)', text)
            for blk in parts:
                if not blk.strip().startswith("Start Date:"): continue
                m = re.search(r"Start Date:\s*(\d\d)/(\d\d)/(\d\d)", blk)
                date = f"20{m.group(3)}-{m.group(1)}-{m.group(2)}"
                subj = re.search(r"Subject:\s*(\S+)", blk).group(1)
                Dvals = {}
                inD = False
                for line in blk.splitlines():
                    if line.startswith("D:"): inD = True; continue
                    if inD:
                        if not line.startswith("    "): break
                        mi = re.match(r"\s*(\d+):\s*(.*)", line)
                        if not mi: continue
                        idx = int(mi.group(1))
                        nums = [float(x) for x in mi.group(2).split()]
                        for off, v in enumerate(nums):
                            Dvals[idx+off] = v
                row = {"Subject": subj, "Date": date}
                for i, name in enumerate(D_NAMES):
                    row[name] = Dvals.get(i)
                sessions.append(row)
    return pd.DataFrame(sessions).sort_values(["Subject","Date"]).reset_index(drop=True)

# Summary latency data (G)
G_NAMES = [
    "Avg Latency to Correct Response", "Avg Latency to Incorrect Response",
    "Avg Latency to Reward", "G3_NotUsed", "G4_NotUsed",
    "Total Latency to Correct Response", "Total Latency to Incorrect Response",
    "Total Latency to Reward"
]

def extract_g(folder: str) -> pd.DataFrame:
    """
    Parse all !*.txt files in folder for 'G:' latency blocks and return DataFrame.
    """
    rows = []
    for fn in os.listdir(folder):
        if fn.startswith('!') and fn.lower().endswith('.txt'):
            text = open(os.path.join(folder, fn), encoding='utf8').read()
            parts = re.split(r'(?=Start Date:)', text)
            for blk in parts:
                if not blk.strip().startswith("Start Date:"): continue
                m = re.search(r"Start Date:\s*(\d\d)/(\d\d)/(\d\d)", blk)
                date = f"20{m.group(3)}-{m.group(1)}-{m.group(2)}"
                subj = re.search(r"Subject:\s*(\S+)", blk).group(1)
                Gvals = {}
                inG = False
                for line in blk.splitlines():
                    if line.startswith("G:"): inG = True; continue
                    if inG:
                        if not line.startswith("    "): break
                        mi = re.match(r"\s*(\d+):\s*(.*)", line)
                        if not mi: continue
                        idx = int(mi.group(1))
                        nums = [float(x) for x in mi.group(2).split()]
                        for off, v in enumerate(nums):
                            Gvals[idx+off] = v
                row = {"Subject": subj, "Date": date}
                for i, name in enumerate(G_NAMES):
                    row[name] = Gvals.get(i)
                rows.append(row)
    return pd.DataFrame(rows).sort_values(["Subject","Date"]).reset_index(drop=True)

# Trial-by-trial (K)
K_NAMES = [
    "Trial Number", "Stimulus Location (1-5)", "First Response (1-5,0=Omission)",
    "Correct Response Latency", "Incorrect Response Latency", "Latency to Reward",
    "Omission Error", "Perseverant Resp NP1", "Perseverant Resp NP2",
    "Perseverant Resp NP3", "Perseverant Resp NP4", "Perseverant Resp NP5",
    "K12_NotUsed", "K13_NotUsed", "K14_NotUsed", "K15_NotUsed",
    "Premature ITI Responses", "Time Out Responses", "Receptacle Head Entries",
    "Cue Duration", "ITI Duration", "K21_NotUsed"
]

def extract_k(folder: str) -> pd.DataFrame:
    """
    Parse all !*.txt files in folder for 'K:' trial-by-trial blocks and return DataFrame.
    One row per trial.
    """
    rows = []
    for fn in os.listdir(folder):
        if fn.startswith('!') and fn.lower().endswith('.txt'):
            text = open(os.path.join(folder, fn), encoding='utf8').read()
            parts = re.split(r'(?=Start Date:)', text)
            for blk in parts:
                if not blk.strip().startswith("Start Date:"): continue
                m = re.search(r"Start Date:\s*(\d\d)/(\d\d)/(\d\d)", blk)
                date = f"20{m.group(3)}-{m.group(1)}-{m.group(2)}"
                subj = re.search(r"Subject:\s*(\S+)", blk).group(1)
                inK = False
                for line in blk.splitlines():
                    if line.startswith("K:"): inK = True; continue
                    if inK:
                        if not line.startswith("    "): break
                        mi = re.match(r"\s*(\d+):\s*(.*)", line)
                        if not mi: continue
                        start = int(mi.group(1))
                        nums = [float(x) for x in mi.group(2).split()]
                        # flatten two-row chunks manually in order
                        # collect 22 values sequence
                        vals = []
                        # current row
                        idxs = list(range(start, start+len(nums)))
                        vals = nums.copy()
                        # next line(s)
                        # look ahead for continuation lines
                        # simplistic: collect until len(vals)==22
                        # get subsequent lines
                        # store row
                        if len(vals)==len(nums):
                            row = {"Subject": subj, "Date": date}
                            for i,name in enumerate(K_NAMES):
                                row[name] = vals[i] if i<len(vals) else None
                            rows.append(row)
    return pd.DataFrame(rows).sort_values(["Subject","Date","Trial Number"]).reset_index(drop=True)
