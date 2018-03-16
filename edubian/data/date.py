import time

print "For interrupted press CTRL+C"
try:
        while True:
                time.ctime()
                print time.strftime("%A, %d %b %Y %H:%M:%S %Z")
                time.sleep(1)
except KeyboardInterrupt:
        print('Interrupted. Stop program.')
