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
        f = open(txt_file, 'rb')
        if self.file_length == 0:
            self.file_length = self.__file_len__(txt_file)
        for i, l in enumerate(f):
            tmp = [item.strip('\t') for item in l.split()]
            if not tmp[2] in self.data_dict:
                self.data_dict[tmp[2]] = list()
            self.data_dict[tmp[2]].append([tmp[0], tmp[1], tmp[3]])
        print self.data_dict

    def __file_len__(self, fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1


class Record(object):

    def __init__(self, dataset, date):
        self.x = dataset.data_dict[date][0]
        self.y = dataset.data_dict[date][1]
        self.time = date
        self.measurement = dataset.data_dict[date][3]


class Formulas(object):

    #TODO: IDW based spatial calculation in Review Paper 1.pdf section 4.2
    def calculate_idw(self, x, y, t, xi, yi):
        return math.sqrt(math.pow(xi-x, 2) + math.pow(yi-y, 2))



def main():
    d = Dataset()
    d.load("/Users/Brandon/PycharmProjects/gis_project/resources/pm25_2009_measured.txt")



if __name__ == '__main__':
    main()