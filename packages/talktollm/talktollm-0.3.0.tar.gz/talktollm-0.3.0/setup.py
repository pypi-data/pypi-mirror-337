from setuptools import setup, find_packages
import os

# Function to read the README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='talktollm',
    version='0.3.0',
    author="Alex M",
    # Add author_email for better metadata
    author_email="your_email@example.com", # Replace with actual email if desired
    description="A Python utility for interacting with large language models (LLMs) via web automation",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/AMAMazing/talktollm",
    # Add some relevant keywords
    keywords=["llm", "automation", "gui", "pyautogui", "gemini", "deepseek", "clipboard"],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        # Correct glob pattern: '*' for files in 'images', '**/*' for recursive
        'talktollm': ['images/deepseek/*', 'images/gemini/*'],
    },
    install_requires=[
        'pywin32',
        'pyautogui',
        'pillow',
        'optimisewait'
    ],
    entry_points={
        'console_scripts': [
            # Correct entry point syntax for function within __init__.py
            'talktollm=talktollm.__init__:talkto',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows", # Be more specific if it's Windows-only
        "Development Status :: 4 - Beta", # Example status
        "Intended Audience :: Developers",
        "Topic :: Communications :: Chat",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires=">=3.6",
)
