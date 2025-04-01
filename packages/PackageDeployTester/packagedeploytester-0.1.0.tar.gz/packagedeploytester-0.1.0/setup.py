import ast
from setuptools import setup, find_packages


def read_me():
    with open('./ReadMe.md', 'r', encoding='utf-8') as f:
        return f.read()


# __init__ 에 다른 Package 사용 에러 대처
def get_version():
    filename = 'PackageDeployTester/__init__.py'
    with open(filename, 'r') as f:
        tree = ast.parse(f.read(), filename)
    for node in tree.body:
        if (isinstance(node, ast.Assign) and
                node.targets[0].id == '__version__'):
            return ast.literal_eval(node.value)
        else:
            return ValueError('could not find __version__')


setup(
    name='PackageDeployTester',
    version='0.1.0',
    author='Dev9er',
    author_email='Dev9er' '@' 'gmail.com',
    description='PyPi에 my Package Upload 해보기',
    long_description=read_me(),
    long_description_content_type='text/markdown',
    url='https://github.com/Dev9er/PackageDeployTester',
    license='MIT', # GPL
    # py_modules=['Module'],
    packages=find_packages(),
    # packages=['PackageDeployTester'],
    classifiers=['Development Status :: 1 - Planning',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3',
                 'Operating System :: OS Independent'],
    python_requires='>=3.6',
    # entry_points={'console_scripts': [
    #     'TestToDeployPackage = TestToDeployPackage:main',
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