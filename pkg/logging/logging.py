import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %a %H:%M:%S",
    # filename="test.log",
    # filemode="w",
)

logging.debug("This is debug message")
logging.info("This is info message")
logging.warning("This is warning message")
