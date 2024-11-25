from setuptools import setup, find_packages

setup(
    name="key_bpm_renamer",  # The name of your package
    version="0.1.2",  # The version of your package
    packages=find_packages(),
    install_requires=[
        "eyed3", "tinytag", "pydub", "essentia",  # add any dependencies
    ],
    entry_points={
        "console_scripts": [
            "key_bpm_renamer=key_bpm_renamer.renamer:main",  # Adjust based on your script
        ],
    },
    author="komly",
    author_email="komly@yandex.ru",
    description="A tool to rename audio files based on their key and BPM",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/komly/key_bpm_renamer",  # Change to your GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)