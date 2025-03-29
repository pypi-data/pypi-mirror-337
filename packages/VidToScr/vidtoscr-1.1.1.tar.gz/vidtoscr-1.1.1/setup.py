from setuptools import setup, find_packages

setup(
    name='VidToScr',
    version='1.1.1',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here, e.g., if you use other libraries
    ],
    author='Marcin Jacek Chmiel',
    author_email='martingonn.dev@outlook.com',
    description='A library to convert video files to SCR format.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Martingonn/VID-to-SCR-Lib',  # Optional
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',  # Change as needed
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Change as needed
)
