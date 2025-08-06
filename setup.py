from setuptools import setup, find_packages
import os

# Read README with proper encoding handling
def read_readme():
    """Read README.md with proper encoding handling for cross-platform compatibility."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "ECG Receiver with AI Heart Diagnosis - A comprehensive ECG monitoring and analysis system."
    except UnicodeDecodeError:
        # Fallback for systems with encoding issues
        try:
            with open(readme_path, 'r', encoding='gbk') as f:
                return f.read()
        except:
            return "ECG Receiver with AI Heart Diagnosis - A comprehensive ECG monitoring and analysis system."

setup(
    name="ecg_receiver",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        'pyserial>=3.5',
        'numpy>=1.24.0',
        'PyQt5>=5.15.0',
        'pyqtgraph>=0.13.0',
        'requests>=2.28.0',
        'python-dotenv>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'ecg-receiver=ecg_receiver.main:main',
        ],
    },
    author="qiao",
    author_email="126.com",
    description="A comprehensive ECG receiver with AI-powered heart diagnosis using Gemini 2.5 Flash",
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url="https://github.com/GanQiao1990/ecm_llm",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
