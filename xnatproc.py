import csv

class XnatProc:
    '''
    Class for processing XNAT summary data outputs
    See xnat_fmri_on_prisma for example usage
    '''
    def __init__(self):
        self.csv = []

    def read_scan_list(self, fname):
        '''
        read csv of scans generated by XNAT>Sessions>Spreadsheet
        '''
        
        print('filename: ', fname)
        with open(fname, 'r') as csvfile:
            csvread = csv.DictReader(csvfile)
            for row in csvread:
                self.csv.append(row)

    def filter_scan_list(self, filterterms):
        '''
        filter on filterterms (dict of items from CSV file)
        '''
        csv_filter = []
        for row in self.csv:
            is_hit = True
            for key in filterterms:
                # case insensitive match
                if filterterms[key].lower() not in row[key].lower():
                    is_hit = False                    
            if is_hit == True:
                csv_filter.append(row)
        return(csv_filter)
