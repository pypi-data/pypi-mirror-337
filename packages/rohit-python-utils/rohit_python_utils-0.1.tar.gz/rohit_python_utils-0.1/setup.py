from setuptools import setup, find_packages

setup(
    name="rohit-python-utils",  # Replace with your new unique package name
    version="0.1",  # Increment version if necessary
    author="Krishnamurthy Chandran",
    author_email="rohtihkrishna112002@gmail.com",
    description="A utility library for Python to perform common tasks",
    long_description=open("README.md").read(),  # Ensure you have a README.md for detailed description
    long_description_content_type="text/markdown",  # The format of your long description (Markdown in this case)
    url="https://github.com/yourusername/rohit-python-utils",  # Replace with your GitHub repo URL
    packages=find_packages(),  # Automatically find and include all packages in your project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # You can choose a different license if required
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Specify the Python versions your package supports
    install_requires=[
        # List any dependencies your package may have
        # Example:
        # "numpy",
        # "requests",
    ],
    include_package_data=True,  # Include files from MANIFEST.in (if applicable)
    entry_points={
        'console_scripts': [
            'my-library-cli=my_library.cli:main',  # Replace with any command-line tool entry point if needed
        ],
    },
)
