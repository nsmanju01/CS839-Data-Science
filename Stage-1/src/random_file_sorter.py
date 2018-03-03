import os
import random

def main():
    print os.getcwd()
    os.chdir('merged')
    print os.getcwd()
    file_list = os.listdir(os.getcwd())
    print file_list
    i = 0;
    new_folder = "train"
    os.mkdir(new_folder)
    #Initialize n for how many number of files you want in the learn-set
    n = 200
    #Initialize the range variable to the maximum number you want to use for stratification
    range = 300
    while i < n:
        fname = file_list[random.randint(0,range)]
        if os.path.isfile(fname):
            new_fname = "./" + new_folder + "/" + fname
            os.rename(fname,new_fname)
            if(os.path.isfile(new_fname)):
                i = i + 1
    print "Stratified Done"
    
    
main()
