import operator
import copy
import sys

EMPTY_ROW = {
    'const': 0.,
    'po': 0.,
    'pw': 0.,
    'pc': 0.,
    'pb': 0.,
    'ps': 0.,
    'f1': 0.,
    'f2': 0.,
    'f3': 0.,
    'f4': 0.,
}

EMPTY_PIVOT = {
    'row': 0.,
    'column': 0.,
    'value': 0.,
}

REPARTITION_MATRIX = {
    'po': { 'f1': 1., 'f2': 1., 'f3': 2., 'f4': 0. },
    'pw': { 'f1': 0., 'f2': 2., 'f3': 1., 'f4': 0. },
    'pc': { 'f1': 1., 'f2': 0., 'f3': 0., 'f4': 3. },
    'pb': { 'f1': 0., 'f2': 1., 'f3': 1., 'f4': 1. },
    'ps': { 'f1': 2., 'f2': 0., 'f3': 0., 'f4': 2. },
}

class Core:
    fertz = {
        'f1': 0.,
        'f2': 0.,
        'f3': 0.,
        'f4': 0.,
    }

    prices = {
        'po': 0.,
        'pw': 0.,
        'pc': 0.,
        'pb': 0.,
        'ps': 0.,
    }

    tableau = {
        'f1': {},
        'f2': {},
        'f3': {},
        'f4': {},
        'Z': {}
    }

    def __init__(self, args):
        self.fertz['f1'] = float(args[0])
        self.fertz['f2'] = float(args[1])
        self.fertz['f3'] = float(args[2])
        self.fertz['f4'] = float(args[3])

        self.prices['po'] = float(args[4])
        self.prices['pw'] = float(args[5])
        self.prices['pc'] = float(args[6])
        self.prices['pb'] = float(args[7])
        self.prices['ps'] = float(args[8])

    def initTableauFertzRow(self, key, value, columnKey):
            value['const'] = self.fertz[key]
            if columnKey[0] == 'p':
                value[columnKey] = REPARTITION_MATRIX[columnKey][key]
            elif columnKey[0] == 'f':
                value[columnKey] = 1. if key == columnKey else 0.

    def initTableauZRow(self, value, columnKey):
            if columnKey[0] == 'p':
                value[columnKey] = -self.prices[columnKey]

    def initTableau(self):
        self.tableau['f1'] = EMPTY_ROW.copy()
        self.tableau['f2'] = EMPTY_ROW.copy()
        self.tableau['f3'] = EMPTY_ROW.copy()
        self.tableau['f4'] = EMPTY_ROW.copy()
        self.tableau['Z'] = EMPTY_ROW.copy()

        for key, value in self.tableau.items():
            for columnKey in self.tableau[key]:
                if key != 'Z':
                    self.initTableauFertzRow(key, value, columnKey)
                else:
                    self.initTableauZRow(value, columnKey)

    def endIterationCondition(self):
        for columnKey, columnValue in self.tableau['Z'].items():
            if columnKey[0] == 'p' and columnValue < 0:
                return False
        return True

    def findPivotColumnName(self):
        zValues = []

        for columnKey, columnValue in self.tableau['Z'].items():
            if columnKey[0] == 'p':
                zValues.append((columnKey, columnValue))
        return min(zValues, key=lambda t: t[1])[0]

    def findPivotRowName(self, pivotColumnName):
        pivotColumnValuesDivided = []

        for key, value in self.tableau.items():
            if key != 'Z' and value[pivotColumnName] > 0:
                valueDivided = value['const'] / value[pivotColumnName]
                pivotColumnValuesDivided.append((key, valueDivided))
        return min(pivotColumnValuesDivided, key=lambda t: t[1])[0]

    def findPivotValue(self, pivotRowName, pivotColumnName):
        return self.tableau[pivotRowName][pivotColumnName]

    def generatePivot(self):
        pivot = EMPTY_PIVOT.copy()
        pivot['column'] = self.findPivotColumnName()
        pivot['row'] = self.findPivotRowName(pivot['column'])
        pivot['value'] = self.findPivotValue(pivot['row'], pivot['column'])
        return pivot

    def iterate(self):
        while (self.endIterationCondition() == False):
            self.pivote(self.generatePivot())

    def pivotePivotRow(self, pivot):
        for columnKey in self.tableau[pivot['row']]:
            self.tableau[pivot['row']][columnKey] /= pivot['value']

    def pivoteOtherRow(self, pivot):
        for key, value in self.tableau.items():
            if key != pivot['row']:
                pivotColumnValue = value[pivot['column']]
                if pivotColumnValue != 0:
                    for columnKey in self.tableau[key]:
                        # print('%g - (%g * %g) = %g' % (value[columnKey], pivotColumnValue, self.tableau[pivot['row']][columnKey], value[columnKey] - (pivotColumnValue * self.tableau[pivot['row']][columnKey])))
                        value[columnKey] = value[columnKey] - (pivotColumnValue * self.tableau[pivot['row']][columnKey])

    def pivote(self, pivot):
        self.pivotePivotRow(pivot)
        self.pivoteOtherRow(pivot)
        self.tableau[pivot['column']] = self.tableau[pivot['row']]
        del self.tableau[pivot['row']]

    def displayMoreOrLessZeros(self, grainName, grainType):
        if grainType in self.tableau and self.tableau[grainType]['const'] != 0:
            print('%s: %.2f units at $%g/unit' % (grainName, self.tableau[grainType]['const'] if grainType in self.tableau else 0, self.prices[grainType]))
        else:
            print('%s: 0 units at $%g/unit' % (grainName, self.prices[grainType]))

    def display(self):
        print('Resources: %g F1, %g F2, %g F3, %g F4\n' % (self.fertz['f1'], self.fertz['f2'], self.fertz['f3'], self.fertz['f4']))
        self.displayMoreOrLessZeros('Oat', 'po')
        self.displayMoreOrLessZeros('Wheat', 'pw')
        self.displayMoreOrLessZeros('Corn', 'pc')
        self.displayMoreOrLessZeros('Barley', 'pb')
        self.displayMoreOrLessZeros('Soy', 'ps')
        print('\nTotal production value: $%.2f' % self.tableau['Z']['const'])

    def debugDisplay(self):
        print('|  Base  | Const  |   po   |   pw   |   pc   |   pb   |   ps   |   F1   |   F2   |   F3   |   F4   |')
        for key in self.tableau:
            print('|%s|' % ('{:^8}'.format(key)), end='')
            for columnValue in self.tableau[key].values():
                print('%s|' % ('{:^8}'.format(columnValue)), end='')
            print('')
        print('\n\n')
