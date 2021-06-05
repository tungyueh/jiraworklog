from setuptools import setup, find_packages

setup(
    name='jiraworklog',
    version='0.1.0',
    packages=find_packages(),
    author='Tung-Yueh Lin',
    author_email='tungyuehlin@gmail.com',
    description='Calculate work log from JIRA issue',
    install_requires=['requests', 'jira==2.0.0'],
    extras_require={
        'travis': ['pycodestyle', 'pylint', 'mypy']
    },
)
