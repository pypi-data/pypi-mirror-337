from setuptools import setup, find_packages

setup(
    name="pazlexer",  # Updated package name
    version="1.1.1",
    description="A Python package that help student to develop they programming knowlegde ",
    author="73",
    author_email="73@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "pazlexer": ["data/*.txt"],  # Updated to match new package name
    },
    install_requires=[],  # Add dependencies if needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)