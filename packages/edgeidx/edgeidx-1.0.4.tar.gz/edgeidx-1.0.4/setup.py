from setuptools import setup, find_packages

setup(
    name="edgeidx",
    version="1.0.4",
    author="Nawaz Sayyad, Kunal Chandak, Mayuresh Muluk, Harshal Pathare",
    author_email="kmcwankhed2021@gmail.com",
    description=(
        "EdgeIDX is a Windows-only Python library for OCR that extracts information "
        "from Aadhaar and PAN cards with embedded Tesseract engine."
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        "edgeidx": ["tesseract/Tesseract-OCR/**/*"],
    },
    include_package_data=True,
    install_requires=[
        "pytesseract>=0.3.10",
        "opencv-python>=4.5.0",
        "numpy>=1.21.0",
        "Pillow>=9.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing"
    ],
    python_requires='>=3.6',
    keywords='ocr aadhaar pan-card windows document-extraction',
)
