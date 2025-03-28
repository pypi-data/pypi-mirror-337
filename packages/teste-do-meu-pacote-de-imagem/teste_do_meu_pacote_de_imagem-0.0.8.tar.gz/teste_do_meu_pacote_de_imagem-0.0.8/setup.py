from setuptools import setup, find_packages

# Carregando o conteúdo do README para 'long_description'
with open("README.md", "r", encoding="utf-8") as fh:
    page_description = fh.read()

# Dependências do pacote (comentando o matplotlib para teste)
requirements = [
    # 'matplotlib',  # Comentado temporariamente para testar no TestPyPI
]

setup(
    name="teste_do_meu_pacote_de_imagem",  
    version="0.0.8",  
    author="Rafael",
    author_email="rdestefani000@gmail.com",
    description="Criando um pacote de processamento de imagem com Python",
    long_description=page_description,  # Agora o conteúdo está definido
    long_description_content_type="text/markdown",
    url="https://github.com/Destefanir/image-processing-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)