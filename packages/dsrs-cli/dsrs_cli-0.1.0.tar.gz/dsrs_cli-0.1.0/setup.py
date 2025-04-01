import setuptools                                                                                                          
                                                                                                                           
# Read the contents of your README file                                                                                    
with open("README.md", "r", encoding="utf-8") as fh:                                                                       
    long_description = fh.read()                                                                                           
                                                                                                                           
setuptools.setup(                                                                                                          
    name="dsrs-cli", 
    version="0.1.0", # Initial version                                                                                     
    author="Farid Saud",
    author_email="gfs3@illinois.edu",
    description="An interactive AI chatbot for the command line - DSRS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fsaudm/dsrs-cli",
    
    # Single script for now, using py_modules:                                                                                 
    py_modules=['dsrs_cli'],
    classifiers=[                                                                                                          
        "Programming Language :: Python :: 3",                                                                             
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",                                                                              
        "Environment :: Console",                                                                                          
        "Topic :: Utilities",                                                                                              
    ],
    python_requires='>=3.7', # Minimum Python version                                                                      
    install_requires=[
        'openai>=1.0',
        'python-dotenv',
        'rich',
        'prompt-toolkit',
        'tiktoken',
    ],
    entry_points={
        'console_scripts': [                                                                                               
            'dsrs-chat=dsrs_cli:main', # command_name = module_name:function_name                                          
        ],                                                                                                                 
    },                                                                                                                     
) 