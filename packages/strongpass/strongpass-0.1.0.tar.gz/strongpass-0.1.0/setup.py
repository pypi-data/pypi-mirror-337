from setuptools import setup, find_packages

# Read README.md with UTF-8 encoding
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="strongpass",
    version="0.1.0",
    author="Hemal Pandya",
    author_email="your-email@example.com",  # Replace with your email
    description="A secure and flexible password generator with customizable options.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/password_generator",  # Replace with your GitHub URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Or any other license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",  # Update as per your minimum Python version
)
