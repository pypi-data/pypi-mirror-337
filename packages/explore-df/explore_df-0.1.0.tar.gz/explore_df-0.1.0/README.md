# Quick-EDA

📊 A powerful interactive Exploratory Data Analysis tool that launches a Streamlit interface for your pandas DataFrames with just one line of code.

## Installation

```bash
pip install quick-eda
```

## Quick Start

```python
import pandas as pd
from quick_eda import analyze

# Load your data
df = pd.read_csv('your_data.csv')  # or any pandas DataFrame

# Launch the EDA interface
analyze(df)
```

That's it! The tool will automatically:
1. Launch a Streamlit server
2. Open your default web browser to the EDA interface
3. Display interactive visualizations and analysis of your data

## Features

- 🚀 **One-Line Setup**: Just `analyze(df)` to start exploring
- 📊 **Interactive Visualizations**: Dynamic charts and plots
- 🔍 **Data Quality Analysis**:
  - Missing values detection
  - Outlier analysis
  - Data type validation
  - Consistency checks
- 📈 **Automated Insights**:
  - Distribution analysis
  - Correlation detection
  - Time series patterns
  - Text analysis
- 💡 **Smart Suggestions**: Get recommendations for data cleaning and transformation

## Advanced Usage

```python
from quick_eda import analyze

# Specify a custom port
analyze(df)
```

## Requirements

- Python 3.9+
- pandas 2.0.0+
- streamlit 1.44.0+

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE) 