from setuptools import setup, find_packages

setup(
    name='mydotenv',
    version='0.1.0',
    description='A simple package to manage environment variables with command-line interface',
    author='Mike Shaffer',
    author_email='mikejshaffer@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['python-dotenv'],
    entry_points={
        'console_scripts': [
            'mike=mike.__init__:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    python_requires='>=3.8',
)
