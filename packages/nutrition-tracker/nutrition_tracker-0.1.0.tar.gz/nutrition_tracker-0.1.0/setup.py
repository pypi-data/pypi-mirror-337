from setuptools import setup, find_packages

setup(
    name="nutrition_tracker",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Akhila Kandadi",
    author_email="akhilareddykandadi@gmail.com",
    description="A simple nutrition tracking library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nutrition_tracker",  # Update with your repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
