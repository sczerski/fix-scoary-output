#Author: Sam Czerski
#Script to correct scoary output file
#Takes input as an ouput directory and a phenotype/traits csv file
#Must have file .results.csv from scoary
#Outputs a corrected csv file

from glob import glob
import csv

def fix_output(outdir, phenotype_lookup):
    for broken_path in glob(outdir + '/*.results.csv'):
        outpath = broken_path.replace('.csv', '.fixed.csv')
        fixed_output = list()
        with open(broken_path, 'r') as f:
            #sheetname = broken_path.split('\\')[-1].split('.results')[0].rsplit('_', 4)[0]
            #sheet_phenotypes = phenotype_lookup[sheetname]
            #column_lookup can be edited depending on your data and desired outcome
            column_lookup = {'Number_pos_present_in': phenotype_lookup['1'] + ' ALT (rupture)',
                             'Number_neg_present_in': phenotype_lookup['0'] + ' ALT (no rupture)',
                             'Number_pos_not_present_in': phenotype_lookup['1'] + ' REF (rupture)',
                             'Number_neg_not_present_in': phenotype_lookup['0'] + ' REF (no rupture)'}

            header = f.readline()
            for k, v in column_lookup.items():
                header = header.replace(k, v)
            print(header)

            header = header[1:-2].split('","')
            fixed_header = ['CHROM_POS'] + header[2:]
            print(fixed_header)

            fixed_output.append(fixed_header)

            for line in f:
                split_line = line.strip('\n').strip('"').rsplit('","', len(header) - 2)
                assert '\n' not in ''.join(split_line)
                chrom_pos = split_line[0].replace('",".', ';').replace('","', ':')
                rest = split_line[1:]
                fixed_line = [chrom_pos] + rest
                fixed_output.append(fixed_line)

        line_lengths = list()
        with open(outpath, 'w') as f:
            for line in fixed_output:
                joined = ','.join(line)
                f.write(joined)
                line_lengths.append(len(joined))
                f.write('\n')
                if len(joined) > 32767:
                    print('Warning:  excel will not display this properly')
        print(outpath)
        with open(outpath, 'r') as f:
            for line in f:
                line_lengths.append(len(line))


if __name__ == '__main__':
    outdir = "C:\\rename_fqs_from_csv"
    with open("C:\\rename_fqs_from_csv\\traits.csv", 'r') as t:
        reader = csv.reader(t)
        dict_from_csv = {rows[1]:rows[0] for rows in reader}
        #print(dict_from_csv)
        fix_output(outdir, dict_from_csv)