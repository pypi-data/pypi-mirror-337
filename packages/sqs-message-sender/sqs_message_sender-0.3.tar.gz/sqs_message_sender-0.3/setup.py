from setuptools import setup, find_packages

setup(
    name='sqs_message_sender',
    version='0.3',
    description='A custom library for sending messages to AWS SQS',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Omkar Mahajan',
    author_email='mahajanomkar86@gmail.com',
    packages=find_packages(),
    install_requires=[
        'boto3>=1.20.0',  # Ensure boto3 is installed as a dependency
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
