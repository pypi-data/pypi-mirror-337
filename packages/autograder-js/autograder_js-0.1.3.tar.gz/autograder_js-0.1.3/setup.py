from setuptools import setup, find_packages

setup(
    name='autograder_js',
    version='0.1.3',
    description='Autograder para código JavaScript com feedback interativo usando a API do OpenAI.',
    author='Seu Nome',
    author_email='seu.email@example.com',
    packages=find_packages(),
    install_requires=[
        'openai>=1.0.0',
        'python-dotenv',
        'ipywidgets'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
