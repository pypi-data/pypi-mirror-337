from setuptools import setup

setup(
    name='NlpToolkit-SyntacticParser',
    version='1.0.0',
    packages=['ContextFreeGrammar', 'ProbabilisticContextFreeGrammar', 'ProbabilisticParser', 'SyntacticParser'],
    url='https://github.com/StarlangSoftware/SyntacticParser-Py',
    license='',
    author='olcaytaner',
    author_email='olcay.yildiz@ozyegin.edu.tr',
    description='Syntactic Parsing Algorithms',
    install_requires=['NlpToolkit-ParseTree', 'NlpToolkit-Corpus', 'Nlptoolkit-DataStructure']
)
