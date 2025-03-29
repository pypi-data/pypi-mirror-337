import os
import argparse
import pandas as pd


combine_low_abd_otu_usage = '''
================== combine_low_abd_otu example commands ==================

# keep OTUs with relative abundance higher than 50% and combine the rests
BioSAK combine_low_abd_otu -i otu_table.txt -c 0.5 -o otu_table_combine_min_50.txt

==========================================================================
'''


def transpose_csv(file_in, file_out, sep_symbol, column_name_pos, row_name_pos):
    csv = pd.read_csv(file_in, sep=sep_symbol, header=column_name_pos, index_col=row_name_pos)
    df_csv = pd.DataFrame(data=csv)
    transposed_csv = df_csv.T
    transposed_csv.to_csv(file_out, sep=sep_symbol)


def combine_low_abd_otu(args):

    otu_table_in    = args['i']
    abd_cutoff      = args['c']
    otu_table_out   = args['o']

    # define tmp file name
    tmp1_t          = '%s.tmp1' % otu_table_out
    tmp2_t_filtered = '%s.tmp2' % otu_table_out

    transpose_csv(otu_table_in, tmp1_t, '\t', 0, 0)

    # get all OTUs that have abundance higher than specified cutoff in at least one sample
    otus_to_keep = set()
    line_index = 0
    otu_id_list = []
    for each_line in open(tmp1_t):
        each_line_split = each_line.strip().split('\t')
        if line_index == 0:
            otu_id_list = each_line_split
        else:
            count_list = [int(i) for i in each_line_split[1:]]
            count_sum = sum(count_list)
            for (otu_id, otu_count) in zip(otu_id_list, count_list):
                if (otu_count / count_sum) >= abd_cutoff:
                    otus_to_keep.add(otu_id)
        line_index += 1

    # filter
    otu_count_dict = dict()
    line_index = 0
    otu_id_list = []
    for each_line in open(tmp1_t):
        each_line_split = each_line.strip().split('\t')
        if line_index == 0:
            otu_id_list = each_line_split
        else:
            sample_id = each_line_split[0]
            otu_count_list = [int(i) for i in each_line_split[1:]]
            current_sample_otu_count_dict = dict()
            for (otu_id, otu_count) in zip(otu_id_list, otu_count_list):
                if otu_id in otus_to_keep:
                    current_sample_otu_count_dict[otu_id] = otu_count
                else:
                    if 'others' not in current_sample_otu_count_dict:
                        current_sample_otu_count_dict['others'] = 0
                    current_sample_otu_count_dict['others'] += otu_count
            otu_count_dict[sample_id] = current_sample_otu_count_dict
        line_index += 1

    otus_to_keep.add('others')
    otus_to_keep_list_sorted = sorted(list(otus_to_keep))

    # write out
    otu_table_txt_t_filtered_handle = open(tmp2_t_filtered, 'w')
    otu_table_txt_t_filtered_handle.write('\t%s\n' % '\t'.join(otus_to_keep_list_sorted))
    for each_sample in otu_count_dict:
        combined_otu_count_dict = otu_count_dict[each_sample]
        count_list= [each_sample]
        for eahc_otu in otus_to_keep_list_sorted:
            count_list.append(combined_otu_count_dict[eahc_otu])
        count_list = [str(i) for i in count_list]
        otu_table_txt_t_filtered_handle.write('\t'.join(count_list) + '\n')
    otu_table_txt_t_filtered_handle.close()

    transpose_csv(tmp2_t_filtered, otu_table_out, '\t', 0, 0)

    # remove tmp files
    os.remove(tmp1_t)
    os.remove(tmp2_t_filtered)
    print('Done')


if __name__ == '__main__':

    combine_low_abd_otu_parser = argparse.ArgumentParser()
    combine_low_abd_otu_parser.add_argument('-i', required=True,                            help='input otu count table')
    combine_low_abd_otu_parser.add_argument('-c', required=False, default=0.5,type=float,   help='relative abundance cutoff, default is 0.5')
    combine_low_abd_otu_parser.add_argument('-o', required=True,                            help='output otu count table')
    args = vars(combine_low_abd_otu_parser.parse_args())
    combine_low_abd_otu(args)


'''

python3 /Users/songweizhi/PycharmProjects/BioSAK/BioSAK/combine_low_abd_otu.py -i /Users/songweizhi/Desktop/SMP/02_Usearch_BLCA_GTDB_20250325/s07_AllSamples_unoise_otu_table_noEU_mim20000.txt -o /Users/songweizhi/Desktop/SMP/02_Usearch_BLCA_GTDB_20250325/s07_AllSamples_unoise_otu_table_noEU_mim20000_combined_low_abundant_OTUs_0.5.txt -c 0.1

'''
