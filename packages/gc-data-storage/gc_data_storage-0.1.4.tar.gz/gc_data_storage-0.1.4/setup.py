
from setuptools import setup, find_packages
setup(
    name='gc_data_storage',
    version='0.1.4',
    author='Aymone Jeanne Kouame',
    author_email='aymone.jk@gmail.com',
    description= "Utility for data storage in Google Cloud",
    long_description= "Functions to move data between a Google Cloud Workspace bucket and the persistent, within the same bucket or between two different buckets. It was created to be used within the All of Us Researcher Workbench by default but can be used in other Google Cloud environements. More information, including examples, at https://github.com/AymoneKouame/gc_data_storage.",
    long_description_content_type="text/markdown",   
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
    python_requires='>=3.6',
)
