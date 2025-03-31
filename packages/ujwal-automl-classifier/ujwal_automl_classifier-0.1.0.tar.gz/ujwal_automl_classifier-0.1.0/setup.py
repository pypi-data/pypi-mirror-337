#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from setuptools import setup, find_packages

setup(
    name="ujwal_automl_classifier",  # Package name
    version="0.1.0",  # Package version
    author="Ujwal Watgule",
    author_email="ujwalwatgule@gmail.com",
    description="AutoML for Classification.Simplify model training with automatic hyperparameter tuning and model selection.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/UjwalWtg/automl_classifier",  # GitHub repo link
    packages=find_packages(),
    install_requires=[
        "numpy",
        "sklearn",
        "pandas"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

