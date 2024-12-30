# # import time

# # class MIT:  #dunder method
# #     def __init__(self):
# #         print("memory allocation")
# #         time.sleep(2)
# #     def __del__(self):
# #         print("memory de-allocation")
# #         time.sleep(2)

# # MIT()
# # MIT()

# import logging

# # logging.info("used to log messages")
# # # logging.debug("used to log debug messages")
# # # logging.warning("used to log warnings")
# # logging.error("used to log errors")
# # logging.critical("used to log critical messages")

# logging.basicConfig(filename='sys.log',level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s  ')

# # k=[]
# # logging.info("logging at 14")

# # a=100
# # # logging.info("a initialized")
# # logger1 = logging.getLogger('m1')
# # logger2 = logging.getLogger('m2')
# # logger1.warning("logging at m1")
# # logger2.info("logging at m2")

# def perform_opr(value):
#     if value < 0:
#         raise ValueError('invalid value: %d' % value)
#     else:
#         logging.info('opr succeeded')

# try :
#     inp = int(input('enter value'))
#     perform_opr(inp)
# except ValueError as ve:
#     logging.exception(msg="Exceptionn ocurred : %s",args = str(ve))

