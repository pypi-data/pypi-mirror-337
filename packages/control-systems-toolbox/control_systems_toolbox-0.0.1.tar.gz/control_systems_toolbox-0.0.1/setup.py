from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='control-systems-toolbox',
    version='0.0.1',
    description='A control systems design and simulation toolbox',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Seth Reed',
    author_email='seth.reed01@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='control',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=['']
)