**********
Arguments for pyiat
**********

pyiat: a Python package to analyze Implicit Association Test (IAT) data



.. py:function:: analyze_iat(df,subject,rt,correct,condition,cond1,cond2,block,[blocks=[2,3,5,6]],[weighted=True],[fast_rt=400],[slow_rt=10000],[overall_err_cut=.3],[cond_err_cut=.4],[block_err_cut=.4],[overall_fastslowRT_cut=.10],[cond_fastslowRT_cut=.25],[block_fastslowRT_cut=.25],[num_blocks_cutoff=4],[fastslow_stats=False],[biat=False],[biat_rmv_xtrls=4],[biat_trl_num=False],[error_or_correct='correct'],[errors_after_fastslow_rmvd=False],[flag_outformat='pct'],[print_to_excel=False],[each_stim=False],[stimulus=False]):

   :param pandas dataframe df: Trial x trial IAT data for each subject
   :param str subject: Column name containing subject number
   :param str rt: Column name containing reaction time (in ms) for each trial
   :param str correct: Column name containing whether trial was correct (where correct = 1, error = 0) (can also use if columns specifies errors; see 'error_or_correct' parameter)
   :param str condition: Column name containing condition (e.g. Black-Good\White-Bad vs. Black-Bad\White-Good)
   :param str cond1: Name of first condition (e.g. 'Black-Good\White-Bad'): bias for this condition will result in negative D score
   :param str cond2: Name of second condition (e.g. 'Black-Bad\White-Good'): bias for this condition will result in positive D score
   :param str block: Column that contains block information
   :param list blocks: A list containing the numbers corresponding to the relevant blocks, default : [2,3,5,6]         
   :param Boolean weighted: If True return weighted D scores; if False return unweighted D scores, default : True
   :param int fast_rt: Reaction time (in ms) considered too fast, default: 400
   :param int slow_rt: Reaction time (in ms) considered too slow, default: 10000
   :param float overall_err_cut: Cutoff for subject exclusion: overall error rate (decimal), default : .3
   :param float cond_err_cut: Cutoff for subject exclusion: error rate (decimal) within each condition, default : .4
   :param float block_err_cut: Cutoff for subject exclusion: error rate (decimal) within a single block, default : .4
   :param float overall_fastslowRT_cut: Cutoff for subject exclusion: overall rate of trials with too fast or too slow RT (decimal), default : .1
   :param float cond_fastslowRT_cut: Cutoff for subject exclusion: rate of trials with too fast or too slow RT (decimal) within each condition, default : .25
   :param float block_fastslowRT_cut: Cutoff for subject exclusion: rate of trials with too fast or too slow RT (decimal) within each block, default : .25
   :param int num_blocks_cutoff: Cutoff for subject exclusion: Minimum number of blocks required, default : 4
   :param str error_or_correct: Enter 'error' to enter a column for 'correct' where error = 1, correct = 0, default: 'correct'
   :param Boolean errors_after_fastslow_rmvd: If True calculates error rates after removing all fast\slow trials (similar to R package iat); if False error rates calculated with all trials, default : False
   :param Boolean fastslow_stats: Return a second dataframe containing the number and percentage of fast\slow trials across all subjects and across subjects with usable data, default : False
   :param Boolean biat: Enter True if analyzing a Brief Implicit Assoc Test (BIAT), False if regular IAT, default : False
   :param int biat_rmv_xtrls: Number of trials to remove from beginning of each block. BIAT recommendad scoring procedures (Nosek et al. 2014) remove first 4 trials of each block b/c they are practice trials but not all BIAT have practice trials, default : 4
   :param str biat_trl_num: The name of the column that contains trial number, default : False
   :param str flag_outformat: Can enter 'count' to return number of errors and too fast\slow trials (if fastslow_stats set to True), default : 'pct'
   :param Boolean print_to_excel: Print an excel workbook that contains output, default : False
   :param Boolean each_stim: Return D scores for each individual stimulus (i.e. word), default : False
   :param Boolean stimulus: If each stim = True, then give name of column containing each stimulus (i.e. word), default : False
 
   :return: pandas DataFrame 
