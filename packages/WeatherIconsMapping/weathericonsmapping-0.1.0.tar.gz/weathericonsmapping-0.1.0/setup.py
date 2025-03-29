import setuptools

setuptools.setup(
name="WeatherIconsMapping",
version="0.1.0",
author="Balaji Srikanthan",
author_email="balaji.sbca2020@gmail.com",
description=" Package to map weather icons to weather descriptions",
long_description=open('README.md').read(),
long_description_content_type="text/markdown",
url="https://github.com/pypa/sampleproject",
packages=setuptools.find_packages(),
# if you have libraries that your module/package/library
#you would include them in the install_requires argument
install_requires=[''],
classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: MIT License",
"Operating System :: OS Independent",
],
python_requires='>=3.6',
)
