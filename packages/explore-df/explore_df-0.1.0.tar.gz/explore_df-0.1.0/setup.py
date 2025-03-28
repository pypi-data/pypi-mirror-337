from setuptools import setup, find_packages

setup(
    name="explore-df",
    version="0.1.0",
    description="A quick and interactive EDA tool",
    author="Mandla Sibanda",
    author_email="mandla.sibanda@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pandas>=2.0.0",
        "streamlit>=1.44.0",
        "plotly>=5.14.0",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "statsmodels>=0.14.0",
        "scikit-learn>=1.3.0",
        "ruptures>=1.1.7",
        "wordcloud>=1.9.2",
        "requests>=2.31.0",
    ],
    entry_points={
        'console_scripts': [
            'explore-df=quick_eda.analyzer:main',
        ],
    },
    python_requires=">=3.9",
) 