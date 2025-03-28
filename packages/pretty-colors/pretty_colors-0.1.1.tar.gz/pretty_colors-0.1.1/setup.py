from setuptools import setup, find_packages

setup(
    name='pretty_colors',        # The name of your package
    version='0.1.1',             # Version number
    packages=find_packages(),    # Automatically find package directories
    install_requires=[],         # List dependencies if any (e.g., "json" is part of the standard library)
    author='Dave',
    author_email='your.email@example.com',
    description='A package for working with colors, including retrieval, random selection without repeats, and hex-to-RGB conversion.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dd2912/pretty_colors',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)