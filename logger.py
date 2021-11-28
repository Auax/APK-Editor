import logging

# Setup
handlers = [logging.FileHandler('app.log'), logging.StreamHandler()]
logging.basicConfig(
    format="%(asctime)s - %(levelname)s : %(message)s",
    level=logging.INFO,
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=handlers)
