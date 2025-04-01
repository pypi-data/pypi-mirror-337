from setuptools import setup, find_packages

setup(
    name='n2w_Copilot',
    version='0.1.3',
    description='Modulo Python per convertire numeri in parole',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='[Marino Bruschini]',
    author_email='[marino.bruschini@gmail.com]',
    url='https://github.com/marinobruschini/Python_Projects',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)