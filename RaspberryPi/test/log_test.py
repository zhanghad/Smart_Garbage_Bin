import logging
import traceback
def test():

    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(filename)s %(funcName)s %(lineno)d %(levelname)s: %(message)s",
                        datefmt = '%Y-%m-%d %H:%M:%S')

    logging.debug("debug_msg")
    logging.info("info_msg")
    logging.warning("warning_msg")
    logging.error("error_msg")
    logging.critical("critical_msg")

if __name__ == '__main__':
    # test()
    # try:
    #     1 / 0
    # except Exception:
    #     print(Exception)
    #     logging.error('1')
    #     logging.error(traceback.format_exc())
    #     traceback.print_exc()
    n=1
    print('move to bin [%d]' % (n))

'''
# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')
'''