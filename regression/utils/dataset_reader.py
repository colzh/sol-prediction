import csv
import os

class DatasetReader:
    def __init__(self):
        return

    def read(self, csv_path):
        """

        :param csv_path: path to the CSV dataset.
        :return: Molecules (SMILES) and the desired property.
        """
        return

class DelaneyReader(DatasetReader):
    def __init__(self):
        super(DelaneyReader, self).__init__()
        return

    def read(self, csv_path):
        # header = ['smiles', 'logSolubility']
        if not os.path.exists(csv_path):
            return [], [], []

        smiles = []
        property = []
        folds = [[] for _ in range(5)]
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            reader.__next__() # Skip header
            for row in reader:
                smiles.append(row['SMILES'])
                property.append(float(row['logP']))
                for i in range(5):  # Assuming 5 folds
                    folds[i].append(row[f'fold_{i}'])

        return smiles, property, folds

if __name__ == '__main__':
    reader = DelaneyReader()
    x, y = reader.read("./dataset/chem/delaney.csv")
    print(x, y)

