from setuptools import setup, find_packages

setup(
    name='autograder_js',
    version='0.1.8',
    description='Autograder para código JavaScript com feedback interativo usando a API do OpenAI.',
    author='Lucca Hiratsuca',
    author_email='luccahiratsuca@gmail.com',
    packages=find_packages(),
    install_requires=['requests', 'python-dotenv'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
