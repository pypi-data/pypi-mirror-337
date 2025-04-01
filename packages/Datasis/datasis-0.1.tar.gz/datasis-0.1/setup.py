from setuptools import setup, find_packages

setup(
    name="Datasis",  # تأكد من أن الاسم صحيح
    version="0.1",  # تأكد من أن الإصدار صحيح
    author="Ahmed Eldesoky",
    author_email="ahmedeldeosky284@yahoo.com",
    description="A short description of your package",
    url="https://github.com/ahmed-eldesoky284/Datasis",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",  # Optional: to specify markdown format
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',

)
