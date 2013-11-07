import datetime
import math
import scipy.spatial
from kdtree import KDTree


class Dataset:

    def __init__(self, txt_file=None):
        #self.data_dict = {}
        self.data_list = []
        self.record_list = []
        self.file_length = 0
        self.start_date = datetime.date(2009, 1, 1)

        if txt_file:
            self.file_length = self.__file_len__(txt_file)
            self.load(txt_file)

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
            #if not tmp[2] in self.data_dict:
            #    self.data_dict[tmp[2]] = list()
            #self.data_dict[tmp[2]].append(Record(tmp[0], tmp[1], tmp[2], tmp[3]))
            """
            The following will have the same index so we can get the index when returning the n-closest nodes
            then use those index's to get the record_list records. This lets us get the measurement since we don't store
            that in the data_list
            """
            #Record List is used to return the specific records including the measurement value
            self.record_list.append(Record(float(tmp[0]), float(tmp[1]), float(tmp[2]), float(tmp[3])))
            #Data List is used for the kd-tree when returning N-closest Records
            self.data_list.append([float(tmp[0]), float(tmp[1]), float(tmp[2])])

    def __file_len__(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1


class Record(object):

    def __init__(self, x, y, t, m, d_map=None):
        self.x = x
        self.y = y
        self.t = t
        self.m = m
        self.d_map = d_map

    def get_neighbors(self, N):
        neighbors = self.d_map.get_n_neighbors(self, N)
        return neighbors

    def get_distance_to(self, record):
        return math.sqrt((self.x - record.x) * (self.x - record.x) + (self.y - record.y) * (self.y - record.y) + (self.t - record.t) * (self.t - record.t))

    @staticmethod
    def interpolate_value(x, y, t, records_map, N=3, P=1):
        output = Record(x, y, t, 0, records_map)
        neighbors = output.get_neighbors(N)
        sum = 0
        for neighbor in neighbors:
            sum += output.get_lambda(neighbors, neighbor, P) * neighbor.m

    def get_lambda(self, neighbors, selected_record, power,):
        di = self.get_distance_to(selected_record)
        numerator = math.pow(1/di,power)
        denominator = 0
        for neighbor in neighbors:
            dk = self.get_distance_to(neighbor)
            denominator += math.pow(1/dk, power)

        assert denominator != 0
        return numerator / denominator

    #Pass in the map data in order to
    def loocv(self, N, P):
        #Get neighbors
        neighbors = self.get_neighbors(N,)
        sum = 0
        for i in xrange(N):
            sum += self.get_lambda(neighbors,neighbors[i],P) * neighbors[i].m

    def __str__(self):
        return "X: %f,\tY: %f,\tT: %f,\tM: %f" % (float(self.x), float(self.y), float(self.t), float(self.m))
        
        
class DataMap:

    def __init__(self, dataset):
        #Create our tree here
        self.tree = scipy.spatial.KDTree(dataset.data_list)
        self.data = dataset.data_list
        self.records = dataset.record_list
        #point = [-87.650556, 34.760556, 37.0]

    def get_record(self, x, y, t):
        for i in range(len(self.data)):
            if self.data[i][0] == x and self.data[i][1] == y and self.data[i][2] == t:
                return self.records[i]

    def get_n_neighbors(self, record, n):
        neighbors = []
        point = [record.x, record.y, record.t]
        distances, positions = self.tree.query([point], n)
        for x in xrange(n):
            p = positions.flat[x]
            neighbors.append(self.records[p])

        return neighbors


def main():
    d = Dataset()
    #d.load("/Users/Brandon/PycharmProjects/gis_project/resources/pm25_2009_measured.txt")
    d.load("../resources/pm25_2009_measured.txt")
    #r = Record(d)
    map = DataMap(d)
    result = map.get_record(-87.650556, 34.760556, 28.0)
    result.d_map = map
    ng = result.get_neighbors(3)
    print result
    for n in ng:
        print n




if __name__ == '__main__':
    main()