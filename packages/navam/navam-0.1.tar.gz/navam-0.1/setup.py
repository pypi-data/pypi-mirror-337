import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name='navam',
    version='0.1',
    install_requires=[
        'Pillow>=11.1.0'],
    author='Nava Teja',
    author_email='mushamnavam9530@gmail.com',
    description="Change colors in a Dichromatic Image",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license = "MIT",
    url='https://github.com/Navam9530/Dichromatic_Changer',
    keywords = "Image-Manipulation Color-Inversion Dichromatic-Images",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.13",
        "Topic :: Other/Nonlisted Topic",
    ],
)
