# Hugo-Lancery-Thesis
Thesis on Lunar and planetary photometry in collaboration with GEOPS and LATMOS from Paris Saclay University

### [Internship](./Internship/README.md)

### [Subject](./Thesis/SUBJECT.md)
## 📁 Project Structure

```text
thesis-project/
│
├── 📄 README.md                 # Project overview and how to use the repo
├── 📄 LICENSE                   # Choose an appropriate license (e.g., MIT, GPL)
├── 📄 .gitignore                # Ignore files like logs, temp files, etc.
│
├── 📁 docs/                     # Documentation (progress reports, plans, etc.)
│   ├── proposal.pdf
│   ├── progress_report_01.md
│   └── literature_review.md
│
├── 📁 thesis/                   # Main LaTeX or Markdown thesis source
│   ├── main.tex
│   ├── chapters/
│   │   ├── intro.tex
│   │   ├── related_work.tex
│   │   └── conclusion.tex
│   ├── figures/
│   └── bibliography.bib
│
├── 📁 experiments/              # Jupyter notebooks, test scripts
│   ├── notebook1.ipynb
│   ├── experiment_utils.py
│   └── results/
│       └── exp1_results.csv
│
├── 📁 src/                      # Source code for models, simulations, analysis
│   ├── __init__.py
│   ├── data_loader.py
│   ├── model.py
│   └── train.py
│
├── 📁 data/                     # Raw and processed datasets (keep .gitignore here)
│   ├── raw/
│   └── processed/
│
├── 📁 tests/                    # Unit tests and testing scripts
│   ├── test_model.py
│   └── test_utils.py
│
├── 📁 scripts/                  # Utility scripts (e.g., for plotting, automation)
│   └── plot_results.py
│
└── 📁 logs/                     # Logs from training/experiments (gitignored)
