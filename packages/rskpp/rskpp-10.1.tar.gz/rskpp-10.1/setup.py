from setuptools import setup 

setup(
    name = "rskpp",
    version = "10.1", 
    description= "Rejection Sampling Approach to k-means++ seeding",
    packages=["rskpp"], 
    author="Anonymous",  
    zip_safe = False, 
    install_requires=[
        "numpy", "scikit-learn", "matplotlib"
    ],
)