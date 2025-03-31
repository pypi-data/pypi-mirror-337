from setuptools import setup, find_packages

setup(
    name="tinyml_compress",
    version="1.0.1",
    description="A library for converting, optimizing, and saving/loading machine learning models.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Lawrence Menegus",
    author_email="lmenegus7@gmail.com",
    url="https://github.com/Lawrence-Menegus/tinyml_compress",
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.0',
        'torch>=1.6',
        'tensorflow-model-optimization', 
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)