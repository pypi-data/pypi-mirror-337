from setuptools import setup, find_packages

# Read dependencies from requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(

    name="sort_my_face",
    version="0.1.2",
    packages=find_packages(),
    install_requires= requirements,  # Add dependencies here
    author="Farida Keunang Tchatchou",
    description="Un outil de tri d'images par reconnaissance faciale.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fkeunang/sort_my_face",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
                ],
    entry_points={
        "console_scripts": [
            "sort_my_face=sort_my_face.main:sort_my_face",
                #this means
                #"sort_my_face -->la commande que l'utilisateur devra taper dans le terminal
                # "sort_my_face.main --> le fichier main.py dans le package sort_my_face
                # sort_my_face --> la fonction sort_my_face dans ce fichier"
            ],
        },
    python_requires=">=3.8",  
    
)


