from setuptools import setup, find_packages

setup(
    name="qmaze_cipher",
    version="1.0.0",
    author="[SanjiCo]",
    author_email="[i.ckl53@outlook.com]",
    description="Quantum-resistant chaos-based encryption algorithm",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SanjiCo/qmaze_cipher",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[],
    include_package_data=True,
)
