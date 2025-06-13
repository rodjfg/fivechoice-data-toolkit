# Five‐Choice Data Extractors
A small collection of Python functions to parse MED-PC “Five-Choice” session text files and build ready-to-analyze DataFrames.
Extract, clean, and export MED-PC “5-Choice” session data (A, D, G, K blocks) into tidy pandas DataFrames and Excel workbooks.

## 📖 Overview

Behavioral neuroscience labs using MED-PC often store session metadata and trial results in plain-text “A:”, “D:”, “G:”, and “K:” blocks. These scripts:

- **Scan** a folder for any `!*.txt` session files  
- **Parse** each block into separate pandas DataFrames  
  - **A**: control & session parameters  
  - **D**: summary response statistics  
  - **G**: summary latencies  
  - **K**: trial-by-trial details  
- **Label** each column with meaningful variable names  
- **Save** everything to one multi-sheet Excel file  
---

## Overview

### `extract_a(folder)`
Reads all files whose names begin with `!` in `folder` and pulls out the `A:` control parameters:

- **Trials to Run**  
- **Limited-Hold Time (sec)**  
- **Time-Out (sec)**  
- **Reward Type**  
- **Reward Duration (sec)**  
- **Session Duration (min)**  

### `extract_g(folder)`
Reads the same files and pulls the `G:` latency summaries, producing per-subject averages and totals:

- **Avg latency to correct / incorrect / reward**  
- **Total latency to correct / incorrect / reward**  

### `extract_d(folder)`
Reads the same files and pulls the `D:` summary response statistics:

- **Correct**, **Incorrect**, **Omissions**, **Premature**, **Perseverant**, **Time-out** counts  
- **Total head entries**  
- **Percent correct**, **Percent incorrect**, **Percent omissions**  

### `extract_k(folder)`
Reads the same files and pulls the trial-by-trial block `K:`, unstacking every 22 values per trial into columns such as:

- **Trial number**  
- **Stimulus location**  
- **First response**, **latencies**, **errors**, **perseverative pokes**, **ITI pokes**, etc.  

All four functions return a **pandas.DataFrame** sorted by **Subject** and **Date**.

---

## Installation

```bash
pip install pandas openpyxl

1. Clone this repo  
   ```bash
   git clone https://github.com/yourusername/five-choice-extractors.git
   cd five-choice-extractors
