import datetime
import math


class Dataset:
    def __init__(self, txt_file=None):
        self.data_dict = {}
        self.file_length = 0
        self.start_date = datetime.date(2009, 1, 1)

        if txt_file:
            self.file_length = self.__file_len__(txt_file)
    
    def load(self, txt_file):
        '''
        Open the pm file, we then will enumerate through each record.
        Each record contains an X and Y coordinate, a Day number and a
        Value. We then append new values to the dictionary and each X,Y,Value
        is associated with that day. If the day is already present, we just append 
        the new X,Y,Value. 
        '''
        f = open(txt_file, 'rb')
        if self.file_length == 0:
            self.file_length = self.__file_len__(txt_file)
        for i, l in enumerate(f):
            tmp = [item.strip('\t') for item in l.split()]
            if not tmp[2] in self.data_dict:
                self.data_dict[tmp[2]] = list()
            self.data_dict[tmp[2]].append(Record(tmp[0], tmp[1], tmp[3]))

    def __file_len__(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1


class Record(object):

    def __init__(self, x=None, y=None, m=None ):
        self.x = x
        self.y = y
        self.m = m
        
    def __str__(self):
        return "X: %f,\tY: %f,\tM: %f" % (x, y, m)
        
        
class DataMap:
    
    def __init__(self, dataset):
        pass 



def main():
    d = Dataset()
    #d.load("/Users/Brandon/PycharmProjects/gis_project/resources/pm25_2009_measured.txt")
    d.load("../resources/pm25_2009_measured.txt")
    r = Record(d)



if __name__ == '__main__':
    main()