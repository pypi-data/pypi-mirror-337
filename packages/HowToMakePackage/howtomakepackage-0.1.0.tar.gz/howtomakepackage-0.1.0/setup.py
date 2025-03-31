import ast

from setuptools import setup, find_packages


def read_me():
    with open('./ReadMe.md', 'r') as f:
        return f.read()


def get_version():
    filename = 'package/__init__.py'
    with open(filename, 'r') as f:
        tree = ast.parse(f.read(), filename)
    for node in tree.body:
        if (isinstance(node, ast.Assign) and
                node.targets[0].id == '__version__'):
            return ast.literal_eval(node.value)
        else:
            return ValueError('could not find __version__')


setup(
    name='HowToMakePackage',
    version='0.1.0',
    author='박성배',
    author_email='Dev9er' '@' 'gmail.com',
    description='How to make package',
    # long_description=read_me(),
    # long_description_content_type='text/markdown',
    url='https://github.com/Dev9er/HowToMakePackage',
    license='MIT', # GPL
    py_modules=['Module'],
    # packages=setuptools.find_packages(),
    classifiers=['Development Status :: 1 - Planning',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3',
                 'Operating System :: OS Independent'],
    python_requires='>=3.6',
    # entry_points={'console_scripts': [
    #     'HowToMakePackage = HowToMakePackage:main',
    # ]},
    # install_requires=[
    #     'flask>=1.0.2, <1.1',
    #     'click==6.7',
    # ],
    # tests_require=['pytest'],
    # extras_require={
    #     'crypto': ['crypto']
    # }
)