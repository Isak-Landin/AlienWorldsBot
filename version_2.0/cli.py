try:
    import time
    import traceback
    from program_files.__main__ import main

    if __name__ == '__main__':
        main()
except:
    print(traceback.print_exc())
    time.sleep(10000)