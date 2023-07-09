'''
Configure the basic settings of the logger, such as: file name, logging level and format.

Functions:

configure_logging() -> None
'''
import logging


def configure_logging() -> None:
    logging.basicConfig(
        filename='app.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
