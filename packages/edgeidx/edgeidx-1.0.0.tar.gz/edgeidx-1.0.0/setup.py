from setuptools import setup, find_packages

setup(
    name="edgeidx",
    version="1.0.0",
    author="Nawaz Sayyad , Kunal Chandak , Mayuresh Muluk , Harshal Pathare",
    author_email="kmcwankhed2021@gmail.com",
    description="EdgeIDX is an python library for Optical Character Recognition (OCR) project that aims to address the limitations of existing OCR systems by focusing on accuracy, speed, and lightweight deployment. The project is designed specifically for extracting information from government-issued identity documents such as Aadhaar and PAN cards.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pytesseract",
        "opencv-python",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
