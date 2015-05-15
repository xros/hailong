#!/usr/bin/env python2
import sys
import os


def show_help():
    print"""This program prints files to the standard output. 
    Any number of files can be specified. 
    Options include: 
        --version               : Prints the version number 
        --help                  : Display this help 
        --log                   : Specify the file path of auth.log. By default it's "/var/auth.log"
        --show-intruders        : Show intruders' IPs (This has to be worked with flag "--log")
        --show-landers          : Show landers' IPs (This has to be worked with flag "--log")
        """ 



def show_version():
    print("Version 1.0")


def get_a_intruder_ip(file_line):
    if file_line[:-1].__contains__("Failed password") and file_line[:-1].__contains__("message repeated"):
        # return a piece of ip
        return file_line[:-1].split(" ")[15]


def get_a_lander_ip(file_line):
    if file_line[:-1].__contains__("Accepted password"):
        # return a piece of ip
        return file_line[:-1].split(" ")[10]




def run():
    """
    """

    if len(sys.argv) == 1:
        show_help()
        return

    else:
        for i in range(len(sys.argv[0:])):
            if sys.argv[i].startswith("--"):
                try:
                    option = sys.argv[i][2:]
                except:
                    show_help()
                    return


                # show version
                if option == "version":
                    show_version()
                    return

                # show some help
                elif option == "help":
                    show_help()
                    return

                # show some help
                elif option == "show-intruders":
                    if "--log" not in sys.argv:
                        show_help()
                        return

                elif option == "show-landers":
                    if "--log" not in sys.argv:
                        show_help()
                        return

                # read log
                elif option == "log":


                    log_path = "/var/auth.log"
                    # Get path of /var/auth.log
                    try:
                        log_path = sys.argv[i+1]
                    except:
                        pass

                    try:
                        the_log_file = open(log_path, 'r')
                    except IOError,e:
                        print("Does not not find the log file. Have you enabled SSHD service? \n%s" % str(e))
                        return
                        
                    intruders_set = set()
                    landers_set = set()
                    with the_log_file as f:
                        for l in f.readlines():

                            # Do something: get_a_intruder_ip/get_a_lander_ip
                            if ('--show-intruders' in sys.argv) and ('--show-landers' in sys.argv):
                                intruders_set.add(get_a_intruder_ip(file_line=l))
                                landers_set.add(get_a_lander_ip(file_line=l))

                            if ('--show-intruders' in sys.argv) and ('--show-landers' not in sys.argv):
                                intruders_set.add(get_a_intruder_ip(file_line=l))

                            if ('--show-intruders' not in sys.argv) and ('--show-landers' in sys.argv):
                                landers_set.add(get_a_lander_ip(file_line=l))

                            if ('--show-intruders' not in sys.argv) and ('--show-landers' not in sys.argv):
                                pass

                    # Remove None in set ( This is a Python2 bug, has to do this :(  )
                    try:
                        intruders_set.remove(None) 
                    except KeyError, e:
                        pass

                   
                    try:
                        landers_set.remove(None) 
                    except KeyError, e:
                        pass

                    # Print IP results out
                    for x in intruders_set:
                        print(x)
                    for x in landers_set:
                        print(x)



                            #if l[:-1].__contains__("Accepted password"):
                            #    # store somewhere
                            #    print l[:-1]
                            #elif l[:-1].__contains__("Failed password"):
                            #    # store somewhere
                            #    print l[:-1]

                # else to show help
                else:
                    show_help()
                    return

if __name__ == "__main__":
    run()
