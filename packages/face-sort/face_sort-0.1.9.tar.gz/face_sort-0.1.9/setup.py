from setuptools import setup, find_packages

# Read dependencies from requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(

    name="face_sort",
    version="0.1.9",
    packages=find_packages(),
    install_requires= requirements,  # Add dependencies here
    author="Farida Keunang Tchatchou",
    description="Un outil de tri d'images par reconnaissance faciale.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fkeunang/face_sort",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
                ],
    entry_points={
        "console_scripts": [
            "face_sort=face_sort.main:face_sort",
                #this means
                #"face_sort -->la commande que l'utilisateur devra taper dans le terminal
                # "face_sort.main --> le fichier main.py dans le package face_sort
                # face_sort --> la fonction face_sort dans ce fichier"
            ],
        },
    python_requires=">=3.8",  
    
)


