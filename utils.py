import traceback

def dumpException(e):
    print('Exception: %s' % e)
    traceback.print_tb(e.__traceback__)