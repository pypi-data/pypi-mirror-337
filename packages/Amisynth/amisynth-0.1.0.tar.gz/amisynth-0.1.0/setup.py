from setuptools import setup, find_packages

setup(
    name='Amisynth',  
    version='0.1.0',    
    packages=find_packages(include=["Amisynth", "Amisynth.*"]),    
    py_modules=["Amisynth"],  # Agrega esto si solo tienes archivos sueltos sin una estructura de paquete
    install_requires=["discord.py", "asyncio", "xfox"],  
    description='Descripción de mi paquete',
    long_description=open('README.md', encoding='utf-8').read(),  
    long_description_content_type='text/markdown',
    author='Amisinth',
    author_email='tuemail@dominio.com',
    url='https://github.com/tu_usuario/mi_paquete',  
    classifiers=[  
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
)
