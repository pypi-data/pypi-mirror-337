import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mindspore-json",
    version="0.1.2",
    author="dq77",
    description="MindSpore JSON utilities and machine learning models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dq77/mindspore-json",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires='>=3.7',
    install_requires=[],
    setup_requires=['wheel'],
)
