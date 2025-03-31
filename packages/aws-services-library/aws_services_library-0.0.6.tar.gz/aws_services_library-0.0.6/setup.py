import setuptools

setuptools.setup(
    name="aws_services_library",  
    version="0.0.6", 
    author="Simon Coker",
    author_email="kornerstonecoker@gmail.com",
    description="AWS SNS and DynamoDB library for Django applications",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kornerstonecoker/aws_services_library",
    packages=setuptools.find_packages(),  
    install_requires=["boto3"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
