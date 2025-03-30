from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="magapy",
    version="0.1.2",
    author="Georges Khawam",
    author_email="your.email@example.com",
    description="Music library management tool for organizing and downloading high-quality audio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geooooooorges/magapy",
    project_urls={
        "Bug Tracker": "https://github.com/geooooooorges/magapy/issues",
        "Documentation": "https://github.com/geooooooorges/magapy",
        "Source Code": "https://github.com/geooooooorges/magapy",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Multimedia :: Sound/Audio",
    ],
    python_requires=">=3.7",
    install_requires=[
        "tqdm>=4.64.0",
        "mutagen>=1.45.1",
        "beets>=1.6.0",
        "pathlib>=1.0.1",
        "pytest>=7.0.0",
        "Pillow>=9.0.0",
        "requests>=2.28.0",
    ],
    entry_points={
        "console_scripts": [
            "magapy=magapy.cli:main",
        ],
    },
    include_package_data=True,
)
