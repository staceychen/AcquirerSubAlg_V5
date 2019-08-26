import csv

divisor = 1001
outfileno = 1
outfile = None

try:
    with open('inputs/assignee_locations_master_full.tsv', 'r', encoding='ISO-8859-1') as infile:
        infile_iter = csv.reader(infile, delimiter='\t')
        header = next(infile_iter)
        for index, row in enumerate(infile_iter):
            if index % divisor == 0:
                if outfile is not None:
                    outfile.close()
                outfilename = 'datafile-{}.tsv'.format(outfileno)
                outfile = open(outfilename, 'w')
                outfileno += 1
                writer = csv.writer(outfile, delimiter='\t')
                writer.writerow(header)
            writer.writerow(row)
finally:
    # Don't forget to close the last file
    if outfile is not None:
        outfile.close()