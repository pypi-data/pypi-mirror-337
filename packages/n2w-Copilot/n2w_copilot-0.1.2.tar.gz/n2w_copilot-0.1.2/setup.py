from setuptools import setup

# Leggi il contenuto del file README
with open ("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='n2w_Copilot',
    version='0.1.2',
    py_modules=['n2w_Copilot_3','n2w_Copilot_Tester'],
    package_data = {'':['n2w_Test_Numeri_Input.txt', 'n2w_test_result.txt']},
    install_requires=[
        #Aggiungi qui le dipendenze necessarie
    ],
    entry_points={
        'console_scripts':[
            'n2w_Copilot = n2w_Copilot_3:main',
#Assumendo che ci sia una funzione main nel file principale
        ],
    },
    long_description = long_description,
    long_description_content_type = "text/markdown",
    # Usa "text/x-rst" se usi reStructuredText
)