import datetime
import math
import scipy.spatial
from kdtree import KDTree
import thread

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

    def __init__(self, x, y, t, m):
        self.x = x
        self.y = y
        self.t = t
        self.m = m

    def get_distance_to(self, record):
        return math.sqrt((self.x - record.x) * (self.x - record.x) + (self.y - record.y) * (self.y - record.y) + (self.t - record.t) * (self.t - record.t))

    @staticmethod
    def interpolate_value(x, y, t, m,d_map, N=3, P=1):
        output = Record(x, y, t, m)
        neighbors = d_map.get_n_neighbors(output, N)
        sum = 0
        for neighbor in neighbors:
            sum += output.get_lambda(neighbors, neighbor, P) * neighbor.m
        return sum


    @staticmethod
    def generateloocv(d_map):
        #Generate loocv values for each input line and write to a new file
        output_vals = []
        for i, record in enumerate(d_map.records):
            output_vals.append([])
            output_vals[i].append(record.m)
            #Calculate loocv for n-3,4,5 and p-1,2,3
            r31 = record.loocv(3, 1, d_map)
            r32 = record.loocv(3,2, d_map)
            r33 = record.loocv(3, 3, d_map)
            r41 = record.loocv(4, 1, d_map)
            r42 = record.loocv(4, 2, d_map)
            r43 = record.loocv(4, 3, d_map)
            r51 = record.loocv(5, 1, d_map)
            r52 = record.loocv(5, 2, d_map)
            r53 = record.loocv(5, 3, d_map)
            output_vals[i].append(r31)
            output_vals[i].append(r32)
            output_vals[i].append(r33)
            output_vals[i].append(r41)
            output_vals[i].append(r42)
            output_vals[i].append(r43)
            output_vals[i].append(r51)
            output_vals[i].append(r52)
            output_vals[i].append(r53)
        print output_vals[1]

        tmp = ""
        for val in output_vals:
            tmp += "%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7], val[8], val[9])
        with open("../output/loocv_idw.txt", "wt") as f:
            f.write(tmp)

    @staticmethod
    def generateError(loocv_file):
        error_vals=[]
        #Read Values from loocv file to do the error calculations
        file_vals={}
        f = open(loocv_file, 'rb')
        for i, l in enumerate(f):
            tmp = [item.strip('\t') for item in l.split()]
            file_vals[i] = tmp


        tmp = ""
        for val in error_vals:
            tmp += "%f\t%f\t%f\t%f\t%f\n" % (val[0], val[1], val[2], val[3], val[4])
        with open("../output/error_idw.txt", "wt") as f:
            f.write(tmp)

    def get_lambda(self, neighbors, selected_record, power):
        di = self.get_distance_to(selected_record)
        numerator = math.pow(1/di, power)
        denominator = 0
        for neighbor in neighbors:
            dk = self.get_distance_to(neighbor)
            denominator += math.pow(1/dk, power)

        assert denominator != 0
        return numerator / denominator

    #Pass in the map data in order to
    def loocv(self, N, P, d_map):
        #Get neighbors
        neighbors = d_map.get_n_neighbors(self, N)
        sum = 0
        for i in xrange(N):
            sum += self.get_lambda(neighbors, neighbors[i], P) * neighbors[i].m
        return sum

    def __str__(self):
        return "X: %f,\tY: %f,\tT: %f,\tM: %f" % (float(self.x), float(self.y), float(self.t), float(self.m))
        
        
class DataMap:

    def __init__(self, dataset):
        #Create our tree here
        self.tree = scipy.spatial.KDTree(dataset.data_list)
        self.data = dataset.data_list
        self.records = dataset.record_list
        self.o_vals = []
        for record in self.records:
            self.o_vals.append(record.m)

        #point = [-87.650556, 34.760556, 37.0]

    def get_record(self, x, y, t):
        for i in range(len(self.data)):
            if self.data[i][0] == x and self.data[i][1] == y and self.data[i][2] == t:
                return self.records[i]
        return Record(x, y, t, 0.0, self)

    def get_n_neighbors(self, record, n):
        neighbors = []
        point = [record.x, record.y, record.t]
        distances, positions = self.tree.query([point], n+1)
        for x in xrange(n+1):
            p = positions.flat[x]
            neighbors.append(self.records[p])

        return neighbors[1:]


def main():
    d = Dataset()
    #d.load("/Users/Brandon/PycharmProjects/gis_project/resources/pm25_2009_measured.txt")
    d.load("../resources/pm25_2009_measured.txt")
    #r = Record(d)
    d_map = DataMap(d)
    record = d_map.get_record(-87.650556, 34.760556, 28.0)
    print "M Value"
    print record.m
    print "LOOCV"
    print record.loocv(3,2,d_map)
    print record.loocv(3,3,d_map)
    print record.loocv(4,1,d_map)
    Record.generateloocv(d_map)




if __name__ == '__main__':
    main()