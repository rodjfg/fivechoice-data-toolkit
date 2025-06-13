# five-choice-extractors

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

## ⚙️ Installation

1. Clone this repo  
   ```bash
   git clone https://github.com/yourusername/five-choice-extractors.git
   cd five-choice-extractors
