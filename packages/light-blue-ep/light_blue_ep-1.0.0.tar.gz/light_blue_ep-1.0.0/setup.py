from setuptools import setup, find_packages

setup(
    name='light-blue-ep',  # The name that will appear on PyPI
    version='1.0.0',
    packages=find_packages(include=['light_blue', 'light_blue.*']),
    include_package_data=True,
    install_requires=[
        'requests',
        'python-dotenv',
        'pyfiglet',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            'lightblue=light_blue.main:main_menu'  # CLI command
        ]
    },
    author='Nithish Yenaganti',
    description='A terminal-based cybersecurity simulation game to learn password safety and phishing detection.',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Topic :: Security",
        "Topic :: Games/Entertainment :: Simulation"
    ],
    python_requires='>=3.6',
)
