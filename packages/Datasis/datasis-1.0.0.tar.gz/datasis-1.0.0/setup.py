from setuptools import setup, find_packages

setup(
    name="Datasis",  # تأكد من أن الاسم صحيح
    version="1.0.0",  # تأكد من أن الإصدار صحيح
    author="Ahmed Eldesoky",
    author_email="your-email@example.com",
    description="A short description of your package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",  # Optional: to specify markdown format
    url="https://github.com/ahmed-eldesoky284/Datasis",
    packages=find_packages(),  # Automatically discovers packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Modify as per your license
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # List any dependencies you need here
    ],
    python_requires='>=3.6',
)
