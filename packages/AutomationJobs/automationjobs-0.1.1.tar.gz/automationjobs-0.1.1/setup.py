from setuptools import setup, find_packages

setup(
    name="AutomationJobs", 
    version="0.1.1",    # Initial version of your package
    description="A AutomationJobs package",  # Brief description of your package
    long_description=open('README.md').read(),  # Read the long description from your README
    long_description_content_type="text/markdown",  # Format of your long description (can be text or markdown)
    author="Viswanadh",  # Your name
    author_email="gowd7272@gmail.com",  # Your email 
    url="https://github.com/viswanadhGowd/AutomationJobs",  # URL of your project (GitHub or similar)
    packages=find_packages(),  # Automatically finds the package directories
    classifiers=[  # Optional classifiers to categorize your project
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6', 
    install_requires=[    
        "setuptools",
    ],
    # test_suite="tests",  # Where the tests are located
)
