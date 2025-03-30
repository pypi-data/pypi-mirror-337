from setuptools import setup, find_packages

setup(
    name='autograder_js',  # Nome único para o seu pacote
    version='0.1.0',
    description='Autograder para código JavaScript com feedback sem entregar a resposta completa.',
    author='Lucca Hiratsuca',
    author_email='luccahiratsuca@gmail.com',
    packages=find_packages(),
    install_requires=[
        'openai',
        'python-dotenv'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
