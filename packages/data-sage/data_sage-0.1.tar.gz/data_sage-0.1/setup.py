from setuptools import setup, find_packages

setup(
    name="data_sage",
    version="0.1.0",
    description="A Python library for easy exploratory data analysis",
    author="aitechman",
    author_email="aitechman@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "seaborn",
        "matplotlib",
        "scipy",
        "statsmodels",
        "scikit-learn",
        "wordcloud",
        "ipython"
    ],
    python_requires=">=3.8",
)
