from setuptools import setup, find_packages

setup(
    name="PyInfoComp",  
    version="1.1.0", 
    author="Jamil Formuly",  
    author_email="Jamilformuly12345@gmail.com", 
    description="Infopy is a Python module that provides a collection of methods to retrieve essential system information. "
                "With this module, you can easily get details about your system's hardware and software, such as the CPU, GPU, RAM, battery status, network information, uptime, and more. "
                "It also supports retrieving public IP addresses, Wi-Fi profiles, clipboard contents, and system OS information.",  
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",  
    url="https://github.com/froxxy1011/PyInfo",  
    packages=find_packages(),  
    install_requires=[ 
        "requests",
        "psutil",
        "pyperclip",
        "wmi",
    ],
    classifiers=[  
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)
