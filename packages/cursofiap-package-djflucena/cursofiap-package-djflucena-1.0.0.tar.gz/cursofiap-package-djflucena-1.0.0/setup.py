from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='cursofiap-package-djflucena',
    version='1.0.0',
    packages=find_packages(),
    description='Descricao da sua lib cursofiap',
    author='David J F de Lucena',
    author_email='djflucena@sefaz.al.gov.br',
    url='https://github.com/djflucena/publicando-pacote-python',  
    license='MIT',  
    long_description=long_description,
    long_description_content_type='text/markdown'
)
