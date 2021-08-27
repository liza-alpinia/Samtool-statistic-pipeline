import os
import argparse
def samtools(infile):
    if infile.endswith('sam'):
        path_f=os.getcwd()
        os.system('samtools view -bS {0}/{1} -o {0}/{1}.bam'.format(path_f, infile))
        sort_f='sort_{0}.bam'.format(infile.split('.sam')[0])
        os.system('samtools sort -@ 4 {0}/{1}.bam > {0}/{2} '.format(path_f, infile, sort_f))
        filt_f = 'filt_{0}'.format(sort_f)
        os.system('samtools view -h -q 17 {0}/{1} > {0}/{2}'.format(path_f, sort_f, filt_f))
        os.system('samtools flagstat -@ 4 {0}/{1} > dna_flag_s.txt'.format(path_f,sort_f))
        os.system('samtools flagstat -@ 4 {0}/{1} > dna_flag_f.txt'.format(path_f, filt_f))
    if infile.endswith('bam'):
        path_f = os.getcwd()
        sort_f = 'sort_{0}.bam'.format(infile)
        os.system('samtools sort -@ 4 {0}/{1} > {0}/{2} '.format(path_f, infile, sort_f))
        filt_f = 'filt_{0}'.format(sort_f)
        os.system('samtools view -h -q 17 {0}/{1}> {0}/{2}'.format(path_f, sort_f, filt_f))
        os.system('samtools flagstat -@ 4 {0}/{1} > dna_flag_s.txt'.format(path_f, sort_f))
        os.system('samtools flagstat -@ 4 {0}/{1} > dna_flag_f.txt'.format(path_f, filt_f))
def stat(infile):
    t_i=0
    path_f = os.getcwd()
    file_stat=[]
    with open(path_f+'/dna_flag_s.txt') as file:
        for seq in file:
            if 'QC-passed reads + QC-failed reads' in seq:
                t_i=float(seq.split(' ')[0])
                file_stat.append('Общее количество прочтений - {0}'.format(seq.split(' ')[0]))
            if 'mapped' in seq and ('chr'  and 'mate') not in seq:
                file_stat.append('Общее количество выровненных прочтений - {0}{1}'.format(seq.split(' ')[0],seq.split('mapped')[-1].rstrip()))
            if 'read1' in seq:
                file_stat.append('Количество выровненных прямых прочтений - {0}'.format(seq.split(' ')[0]))
            if 'properly paired' in seq:
                file_stat.append('Количество правильно сопряженных прочтений - {0}'.format(seq.split(' ')[0],seq.split('properly paired ')[-1]))
            if 'singletons' in seq:
                file_stat.append('Количество одиночных прочтений - {0}'.format(seq.split(' ')[0],seq.split('singletons ')[-1]))
    with open(path_f + '/dna_flag_f.txt') as file:
        for seq1 in file:
            if 'QC-passed reads + QC-failed reads' in seq1:
                file_stat.append('Количество прочтений, выравненных с точностью не менее 98,5% - {0} ({1}%)'.format(seq1.split(' ')[0], round((float(seq1.split(' ')[0])/t_i)*100,2)))
    for seq in file_stat:
        print(seq)
if __name__ == "__main__":
    # выполняется как основная функция
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('ref', help="Infile bam/sam")
    args = parser.parse_args()
    samtools(args.ref)
    stat(args.ref)