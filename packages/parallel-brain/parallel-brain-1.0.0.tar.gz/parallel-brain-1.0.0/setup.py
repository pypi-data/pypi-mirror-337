from setuptools import setup, find_packages

setup(
    name='parallel-brain',
    version='1.0.0',
    description='A neural simulation framework with stabilized thresholds',
    author='Darshan',
    author_email='your_email@example.com',  # Replace with your email
    url='https://github.com/your_username/parallel-brain',  # Replace with your GitHub URL
    packages=find_packages(),
    install_requires=[
        'torch>=1.9.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
