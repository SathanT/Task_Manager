import logging
import logging.config

def setup_logging():
    logging.config.dictConfig({
        "version" : 1,
        "disable_existing_loggers" : False,
        "formatters" : {
            "default" : {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s" 
            }
        },
        "handlers" : {
            "console" : {
                "class":"logging.StreamHandler",
                "formatter" : "default",
                "level" : "DEBUG"
            },
            "file" : {
                "class" : "logging.FileHandler",
                "filename": "app.log",
                "formatter" : "default",
                "level" : "INFO"
            }
        },
        "root": {
            "handlers" : ["console","file"],
            "level" : "DEBUG"
        }
    })