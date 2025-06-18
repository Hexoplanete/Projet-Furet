import logging
import os
import shutil
from furet import repository, settings
from furet.configs import ProcessingConfig
from furet.processing import utils

logger = logging.getLogger("processing")

def setup():
    logger.debug("Importing modules...")
    import furet.processing.processing
    settings.setDefaultConfig(ProcessingConfig)


def getRaaPdf(id: int) -> tuple[str, bool]:
    raa = repository.getRaaById(id)
    if raa is None:
        return "", False
    path = os.path.join(os.path.join(settings.config(ProcessingConfig).pdfDir), f"{raa.fileHash}.pdf")
    return path, os.path.isfile(path)


def setRaaPdf(id: int, path: str) -> bool:
    raa = repository.getRaaById(id)
    pdfPath, exists = getRaaPdf(id)
    if exists or raa is None or raa.fileHash != utils.getFileHash(path):
        return False

    shutil.copy(path, pdfPath)
    return True
