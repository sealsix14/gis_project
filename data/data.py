import datetime
import math
import scipy.spatial
from kdtree import KDTree


class Dataset:
    def __init__(self, txt_file=None):
        self.data_dict = {}
        self.data_list = []
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
            self.data_dict[tmp[2]].append(Record(tmp[0], tmp[1], tmp[2], tmp[3]))
            #self.data_list.append(Record(tmp[0], tmp[1], tmp[2], tmp[3]))
            self.data_list.append([float(tmp[0]), float(tmp[1]), float(tmp[2])])

    def __file_len__(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1


class Record(object):

    def __init__(self, x=None, y=None, t=None, m=None):
        self.x = x
        self.y = y
        self.t = t
        self.m = m
        
    def __str__(self):
        return "X: %f,\tY: %f,\tM: %f" % (float(self.x), float(self.y), float(self.m))
        
        
class DataMap:

    def __init__(self, datalist):
        #Create our tree here
        self.tree = scipy.spatial.KDTree(datalist)
        self.data = datalist
        #point = [-87.650556, 34.760556, 37.0]

    def get_n_neighbors(self, record, n):
        neighbors = []
        point = [record.x, record.y, record.t]
        distances, positions = self.tree.query([point], n)
        for x in xrange(n):
            p = positions.flat[x]
            neighbors.append(self.data[p])

        return neighbors


def main():
    d = Dataset()
    #d.load("/Users/Brandon/PycharmProjects/gis_project/resources/pm25_2009_measured.txt")
    d.load("../resources/pm25_2009_measured.txt")
    r = Record(d)
    #r.__str__()
    map = DataMap(d.data_list)



if __name__ == '__main__':
    main()