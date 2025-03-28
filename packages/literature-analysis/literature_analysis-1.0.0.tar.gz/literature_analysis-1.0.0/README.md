# Literature Analysis Tool

A comprehensive tool for analyzing scientific literature.

## Installation

```bash
pip install literature-analysis
```

## Usage

```bash
# Run complete analysis
literature-analysis run-all --ncbi-key YOUR_NCBI_KEY --dashscope-key YOUR_DASHSCOPE_KEY --term "your search term"

# Or run individual steps
literature-analysis search --ncbi-key YOUR_NCBI_KEY --term "your search term"
literature-analysis analyze --dashscope-key YOUR_DASHSCOPE_KEY --input-file result1.json
literature-analysis process --input-file result1_analysis.json
literature-analysis analyze-final --dashscope-key YOUR_DASHSCOPE_KEY --input-file result1_analysis_processed.json
literature-analysis visualize --input-file result1_analysis_final.json
```

## Requirements

- Python 3.6+
- See requirements.txt for package dependencies
