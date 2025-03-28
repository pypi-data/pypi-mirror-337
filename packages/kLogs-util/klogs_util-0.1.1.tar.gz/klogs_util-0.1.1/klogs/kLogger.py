import logging
import inspect
from executing import Source
from klogs.kFormatter import kColorFormatter, kNoColorFormatter

class kLogger():

    def __init__(self, tag, logfile=None, loglevel="DEBUG"):
        self.tag = tag 
        self.logfile = logfile
        self.loglevel = loglevel
        self.logger = logging.getLogger(self.tag)

        if loglevel:
            self.logger.setLevel(loglevel.upper())
        else:
            self.logger.setLevel(logging.DEBUG)

        if logfile:
            self.ch = logging.FileHandler(logfile)
        else:
            self.ch = logging.StreamHandler()
        if loglevel:
            self.ch.setLevel(loglevel.upper())
        else:
            self.ch.setLevel(logging.DEBUG)

        if not logfile:
            self.ch.setFormatter(kColorFormatter())
        else:
            self.ch.setFormatter(kNoColorFormatter())
        self.logger.addHandler(self.ch)

    def __call__(self, *args):
        if args:
            for arg in args:
                callFrame = inspect.currentframe().f_back
                callNode = Source.executing(callFrame).node
                source = Source.for_frame(callFrame)
                expression = source.asttokens().get_text(callNode.args[0])
                self.logger.info(f'{expression} | {arg}', stacklevel=2)
        else:
            self.logger.info("", stacklevel=2)

    def debug(self, message):
        self.logger.debug(message, stacklevel=2)

    def info(self, message):
        self.logger.info(message, stacklevel=2)

    def warning(self, message):
        self.logger.warning(message, stacklevel=2)

    def error(self, message):
        self.logger.error(message, stacklevel=2)

    def critical(self, message):
        self.logger.critical(message, stacklevel=2, stack_info=True)

    def setLevel(self, level):
        self.loglevel = level.upper()
        self.logger.setLevel(level.upper())
        self.ch.setLevel(level.upper())

    def setFile(self, file):
        self.logfile = file
        if file:
            self.logger.handlers.clear()
            self.logger = None
            self.logger = logging.getLogger(self.tag)

            if self.loglevel:
                self.logger.setLevel(self.loglevel.upper())
            else:
                self.logger.setLevel(logging.DEBUG)

            self.ch = logging.FileHandler(self.logfile)

            if self.loglevel:
                self.ch.setLevel(self.loglevel.upper())
            else:
                self.ch.setLevel(logging.DEBUG)

            self.ch.setFormatter(kFormatter())
            self.logger.addHandler(self.ch)
