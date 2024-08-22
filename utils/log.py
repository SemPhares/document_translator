import logging
from pathlib import Path

# Créer un logger
logger = logging.getLogger("Document_translator")
logger.setLevel(logging.INFO)

# Créer un gestionnaire de log pour la console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

logfile = Path('log/logfile.log')
if not logfile.exists():
    logfile.parent.mkdir(parents=True, exist_ok=True)
    logfile.touch()

# Créer un gestionnaire de log pour un fichier
file_handler = logging.FileHandler('log/logfile.log')
file_handler.setLevel(logging.INFO)

# Créer un formateur de log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Ajouter le formateur aux gestionnaires de log
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Ajouter les gestionnaires de log au logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)



