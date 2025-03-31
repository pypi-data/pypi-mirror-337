from setuptools import setup, find_packages

setup(
    name='APIShift',
    version='0.1.0',
    description='A package for managing multiple LLM providers with automatic key shifting to bypass rate limits and quotas while maintaining conversation context',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Aditya190803',
    author_email='adityamer.work@gmail.com',
    url='https://github.com/Aditya190803/APIShift',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    extras_require={
        'gemini': ['google-generativeai'],
        'groq': ['groq'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='llm api management multi-provider',
    python_requires='>=3.8',
)
