import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nlp_date_parser",  # Replace with your package name
    version="0.0.1",  # You can update this version as necessary
    author="Vivek Agarwal",  # Replace with your name or organization's name
    author_email="ec.vivek@gmail.com",  # Replace with your email
    description="A simple NLP-based date parser to extract dates from text.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/viv1ag/nlp_date_parser",  # Your package's GitHub URL
    packages=setuptools.find_packages(),  # Automatically finds packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Specify your license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Adjust the minimum Python version based on your requirements
    install_requires=[  # List any dependencies your package requires
        "parse",
        "dateparser",
        "spacy",
    ],
)
