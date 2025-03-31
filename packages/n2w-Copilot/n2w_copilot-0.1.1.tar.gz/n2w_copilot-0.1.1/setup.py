from setuptools import setup

setup(name='n2w_Copilot',version='0.1.1',py_modules=['n2w_Copilot_3','n2w_Copilot_Tester'],package_data = {'':['n2w_Test_Numeri_Input.txt', 'n2w_test_result.txt']}, install_requires=[
    #Aggiungi qui le dipendenze necessarie
    ],entry_points={'console_scripts':['n2w_Copilot = n2w_Copilot_3:main',
#Assumendo che ci sia una funzione main nel file principale
],},)