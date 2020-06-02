import pandas as pd
import numpy as np

def iat_get_dscore_each_stim(df,subject,rt,block,condition,stimulus,cond1,cond2,blocks,weighted):

    '''
    Take all relevant columns and produce a D score for each stimulus (i.e. word).
    
    08-2017
    Alexander Millner <alexmillner@gmail.com
    '''

    idx=pd.IndexSlice
    df=df[(df[condition]==cond1)|(df[condition]==cond2)]
    if weighted==True:
        blocks=sorted(blocks)
        blcnd_rt=df.groupby([subject,stimulus,condition,block])[rt].mean()
        
        #Get mean RT for each block of each condition
        cond1rt_bl1=blcnd_rt.loc[idx[:,:,cond1,[blocks[0],blocks[2]]]]
        cond1rt_bl2=blcnd_rt.loc[idx[:,:,cond1,[blocks[1],blocks[3]]]]

        cond2rt_bl1=blcnd_rt.loc[idx[:,:,cond2,[blocks[0],blocks[2]]]]
        cond2rt_bl2=blcnd_rt.loc[idx[:,:,cond2,[blocks[1],blocks[3]]]]
        
        #Drop block and condidition levels to subtract means
        cond1rt_bl1.index=cond1rt_bl1.index.droplevel([2,3])
        cond1rt_bl2.index=cond1rt_bl2.index.droplevel([2,3])
        cond2rt_bl1.index=cond2rt_bl1.index.droplevel([2,3])
        cond2rt_bl2.index=cond2rt_bl2.index.droplevel([2,3])
        
        #Get RT standard deviation separately for first and second blocks
        b1rt_std=df[(df[block]==blocks[0])|(df[block]==blocks[2])].groupby([subject,stimulus])[rt].std()
        b2rt_std=df[(df[block]==blocks[1])|(df[block]==blocks[3])].groupby([subject,stimulus])[rt].std()
        
        #Get D score
        d1=(cond1rt_bl1-cond2rt_bl1)/b1rt_std
        d2=(cond1rt_bl2-cond2rt_bl2)/b2rt_std
        d=(d1+d2)/2
    elif weighted==False:
        cnds = df.groupby([subject,stimulus,condition])
        d = (cnds[rt].mean().unstack()[cond1]-cnds[rt].mean().unstack()[cond2])/df.groupby([subject,stimulus])[rt].std()

    return(d)



def iat_get_dscore_across_stim(df,subject,rt,block,condition,cond1,cond2,blocks,weighted):
    '''
    Take all relevant columns and produce a D score across all stimuli (i.e. words), which is standard.
    08-2017
    Alexander Millner <alexmillner@gmail.com
    '''
    idx=pd.IndexSlice
    df=df[(df[condition]==cond1)|(df[condition]==cond2)]    
    if weighted==True:
        blocks=sorted(blocks)
        blcnd_rt=df.groupby([subject,condition,block])[rt].mean()
        
        #Get mean RT for each block of each condition
        cond1rt_bl1=blcnd_rt.loc[idx[:,cond1,[blocks[0],blocks[2]]]]
        cond1rt_bl2=blcnd_rt.loc[idx[:,cond1,[blocks[1],blocks[3]]]]

        cond2rt_bl1=blcnd_rt.loc[idx[:,cond2,[blocks[0],blocks[2]]]]
        cond2rt_bl2=blcnd_rt.loc[idx[:,cond2,[blocks[1],blocks[3]]]]
        
        #Drop block and condidition levels to subtract means
        for df_tmp in [cond1rt_bl1,cond1rt_bl2,cond2rt_bl1,cond2rt_bl2]:
            df_tmp.index=df_tmp.index.droplevel([1,2])
        
        #Get RT standard deviation separately for first and second blocks
        b1rt_std=df[(df[block]==blocks[0])|(df[block]==blocks[2])].groupby(subject)[rt].std()
        b2rt_std=df[(df[block]==blocks[1])|(df[block]==blocks[3])].groupby(subject)[rt].std()
        
        #Get D score
        d1=(cond1rt_bl1-cond2rt_bl1)/b1rt_std
        d2=(cond1rt_bl2-cond2rt_bl2)/b2rt_std
        d=(d1+d2)/2
        d=pd.concat([d1,d2,d],axis=1)
        d.columns=['dscore1','dscore2','dscore']
        return(d)
    elif weighted==False:
        cnds = df.groupby([subject,condition])
        d = (cnds[rt].mean().unstack()[cond1]-cnds[rt].mean().unstack()[cond2])/df.groupby(subject)[rt].std()
        d.name='dscore'
        return(d)


def biat_get_dscore_each_stim(df,subject,rt,block,condition,stimulus,cond1,cond2,blocks,weighted):

    '''
    Take all relevant columns and produce a D score for each stimulus (i.e. word).
    
    08-2017
    Alexander Millner <alexmillner@gmail.com
    '''

    idx=pd.IndexSlice
    df=df[(df[condition]==cond1)|(df[condition]==cond2)]
    if weighted==True:
        blocks=sorted(blocks)
        blcnd_rt=df.groupby([subject,stimulus,condition,block])[rt].mean()
        
        #Get mean RT for each block of each condition
        cond1rt_bl1=blcnd_rt.loc[idx[:,:,cond1,[blocks[0],blocks[1]]]]
        cond2rt_bl1=blcnd_rt.loc[idx[:,:,cond2,[blocks[0],blocks[1]]]]  
        #Drop block and condidition levels to subtract means
        cond1rt_bl1.index=cond1rt_bl1.index.droplevel([2,3])
        cond2rt_bl1.index=cond2rt_bl1.index.droplevel([2,3])   
        #Get RT standard deviation separately for first and second blocks
        b1rt_std=df[(df[block]==blocks[0])|(df[block]==blocks[1])].groupby([subject,stimulus])[rt].std()
        
        if len(blocks)>=4:
            cond1rt_bl2=blcnd_rt.loc[idx[:,:,cond1,[blocks[2],blocks[3]]]]
            cond2rt_bl2=blcnd_rt.loc[idx[:,:,cond2,[blocks[2],blocks[3]]]]
            #Drop block and condidition levels to subtract means
            cond1rt_bl2.index=cond1rt_bl2.index.droplevel([2,3])
            cond2rt_bl2.index=cond2rt_bl2.index.droplevel([2,3])   
            b2rt_std=df[(df[block]==blocks[2])|(df[block]==blocks[3])].groupby([subject,stimulus])[rt].std()
        if len(blocks)>=6:
            cond1rt_bl3=blcnd_rt.loc[idx[:,:,cond1,[blocks[4],blocks[5]]]]
            cond2rt_bl3=blcnd_rt.loc[idx[:,:,cond2,[blocks[4],blocks[5]]]]
            #Drop block and condidition levels to subtract means
            cond1rt_bl3.index=cond1rt_bl3.index.droplevel([2,3])
            cond2rt_bl3.index=cond2rt_bl3.index.droplevel([2,3]) 
            b3rt_std=df[(df[block]==blocks[4])|(df[block]==blocks[5])].groupby([subject,stimulus])[rt].std()

        if len(blocks)==2:
            d=(cond1rt_bl1-cond2rt_bl1)/b1rt_std
        elif len(blocks)==4:
            d1=(cond1rt_bl1-cond2rt_bl1)/b1rt_std
            d2=(cond1rt_bl2-cond2rt_bl2)/b2rt_std
            d=(d1+d2)/2
        elif len(blocks)==6:
            d1=(cond1rt_bl1-cond2rt_bl1)/b1rt_std
            d2=(cond1rt_bl2-cond2rt_bl2)/b2rt_std
            d3=(cond1rt_bl3-cond2rt_bl3)/b3rt_std
            d=(d1+d2+d3)/2

    elif weighted==False:
        cnds = df.groupby([subject,stimulus,condition])
        d = (cnds[rt].mean().unstack()[cond1]-cnds[rt].mean().unstack()[cond2])/df.groupby([subject,stimulus])[rt].std()

    return(d)

def biat_get_dscore_across_stim(df,subject,rt,block,condition,cond1,cond2,blocks,weighted):

    '''
    Take all relevant columns and produce a D score for each stimulus (i.e. word).
    
    08-2017
    Alexander Millner <alexmillner@gmail.com
    '''

    idx=pd.IndexSlice
    df=df[(df[condition]==cond1)|(df[condition]==cond2)]
    if weighted==True:
        blocks=sorted(blocks)
        blcnd_rt=df.groupby([subject,condition,block])[rt].mean()
        
        #Get mean RT for each block of each condition
        cond1rt_bl1=blcnd_rt.loc[idx[:,cond1,[blocks[0],blocks[1]]]]
        cond2rt_bl1=blcnd_rt.loc[idx[:,cond2,[blocks[0],blocks[1]]]]  
        #Drop block and condidition levels to subtract means
        cond1rt_bl1.index=cond1rt_bl1.index.droplevel([1,2])
        cond2rt_bl1.index=cond2rt_bl1.index.droplevel([1,2])   
        #Get RT standard deviation separately for first and second blocks
        b1rt_std=df[(df[block]==blocks[0])|(df[block]==blocks[1])].groupby([subject])[rt].std()
        
        if len(blocks)>=4:
          cond1rt_bl2=blcnd_rt.loc[idx[:,cond1,[blocks[2],blocks[3]]]]
          cond2rt_bl2=blcnd_rt.loc[idx[:,cond2,[blocks[2],blocks[3]]]]
          #Drop block and condidition levels to subtract means
          cond1rt_bl2.index=cond1rt_bl2.index.droplevel([1,2])
          cond2rt_bl2.index=cond2rt_bl2.index.droplevel([1,2])   

          b2rt_std=df[(df[block]==blocks[2])|(df[block]==blocks[3])].groupby([subject])[rt].std()

        if len(blocks)>=6:
          cond1rt_bl3=blcnd_rt.loc[idx[:,cond1,[blocks[4],blocks[5]]]]
          cond2rt_bl3=blcnd_rt.loc[idx[:,cond2,[blocks[4],blocks[5]]]]
          #Drop block and condidition levels to subtract means
          cond1rt_bl3.index=cond1rt_bl3.index.droplevel([1,2])
          cond2rt_bl3.index=cond2rt_bl3.index.droplevel([1,2]) 
          b3rt_std=df[(df[block]==blocks[4])|(df[block]==blocks[5])].groupby([subject])[rt].std()

        if len(blocks)==2:
          d=(cond1rt_bl1-cond2rt_bl1)/b1rt_std
          d.name='dscore'
        elif len(blocks)==4:
          #Get D score
          d1=(cond1rt_bl1-cond2rt_bl1)/b1rt_std
          d2=(cond1rt_bl2-cond2rt_bl2)/b2rt_std
          d=(d1+d2)/2
          d=pd.concat([d1,d2,d],axis=1)
          d.columns=['dscore1','dscore2','dscore']
        elif len(blocks)==6:
          #Get D score
          d1=(cond1rt_bl1-cond2rt_bl1)/b1rt_std
          d2=(cond1rt_bl2-cond2rt_bl2)/b2rt_std
          d3=(cond1rt_bl3-cond2rt_bl3)/b3rt_std
          d=(d1+d2+d3)/3
          d=pd.concat([d1,d2,d3,d],axis=1)
          d.columns=['dscore1','dscore2','dscore3','dscore']
        return(d)
    elif weighted==False:
        cnds = df.groupby([subject,stimulus,condition])
        d = (cnds[rt].mean().unstack()[cond1]-cnds[rt].mean().unstack()[cond2])/df.groupby(subject)[rt].std()
        d.name='dscore'
        return(d)



def iat_get_dscore(df,subject,rt,block,condition,cond1,cond2,blocks,weighted,biat,each_stim,stimulus):
    '''
    Select either iat_get_dscore_across_stim or iat_get_dscore_each_stim, depending on the each_stim argument.

    08-2017
    Alexander Millner <alexmillner@gmail.com
    '''

    #Get D scores
    if biat==False:
      if each_stim==False:
          d=iat_get_dscore_across_stim(df,subject,rt,block,condition,cond1,cond2,blocks,weighted)
          if weighted == False:
              d=d.to_frame()
      elif each_stim==True:
          d=iat_get_dscore_each_stim(df,subject,rt,block,condition,stimulus,cond1,cond2,blocks,weighted)
          d=d.unstack()
    elif biat==True:
      if each_stim==False:
          d=biat_get_dscore_across_stim(df,subject,rt,block,condition,cond1,cond2,blocks,weighted)
          if weighted == False:
              d=d.to_frame()
      elif each_stim==True:
          d=biat_get_dscore_each_stim(df,subject,rt,block,condition,stimulus,cond1,cond2,blocks,weighted)
          d=d.unstack()
    return(d)


def overall_fast_slow_stats(df,rt,fast_rt,slow_rt,subject,flags):
    '''
    Return the total number of trials removed across all subjects and across those without flags for poor performance.

    08-2017
    Alexander Millner <alexmillner@gmail.com
    '''

    #Count all fast and slow trials across all subjects
    all_fast_rt_count_all_subs=df[df[rt]<fast_rt][rt].count()
    all_slow_rt_count_all_subs=df[df[rt]>=slow_rt][rt].count()
    all_fast_rt_pct_all_subs=df[df[rt]<fast_rt][rt].count()/df[rt].count().astype(float)
    all_slow_rt_pct_all_subs=df[df[rt]>=slow_rt][rt].count()/df[rt].count().astype(float)
    
    #Now remove subjects with flags and recount
    df_no_flag=df[df[subject].isin(flags[flags.iat_flag==0].index)].copy(deep=True)
    
    all_fast_rt_count_incl_subs=df_no_flag[(df_no_flag[rt]<fast_rt)][rt].count()
    all_slow_rt_count_incl_subs=df_no_flag[(df_no_flag[rt]>=slow_rt)][rt].count()
    all_fast_rt_pct_incl_subs=df_no_flag[(df_no_flag[rt]<fast_rt)][rt].count()/df_no_flag[rt].count().astype(float)
    all_slow_rt_pct_incl_subs=df_no_flag[(df_no_flag[rt]>=slow_rt)][rt].count()/df_no_flag[rt].count().astype(float)


    all_fast_slow_rt=pd.DataFrame([all_fast_rt_count_all_subs,all_fast_rt_pct_all_subs,\
                                   all_slow_rt_count_all_subs,all_slow_rt_pct_all_subs,\
                                   all_fast_rt_count_incl_subs,all_fast_rt_pct_incl_subs,\
                                   all_slow_rt_count_incl_subs,all_slow_rt_pct_incl_subs],
                                   index=['fast_rt_count_all_subs','fast_rt_pct_all_subs',\
                                          'slow_rt_count_all_subs','slow_rt_pct_all_subs',\
                                          'fast_rt_count_included_subs','fast_rt_pct_included_subs',\
                                          'slow_rt_count_included_subs','slow_rt_pct_included_subs']\
                                          ,columns=['fast_slow_rt'])
    return(all_fast_slow_rt)


def blcnd_extract(df,var,subject,condition,block,cond1,cond2,blocks,biat,flag_outformat='pct',include_blocks=True):
    '''
    Generic groupby function to group by subject depending on condition 
    and groupby condition and block (or just condition if unweighted) to 
    extract particular variables (errors, too fast\too slow) by condition and block.

    08-2017
    Alexander Millner <alexmillner@gmail.com
    '''

    idx=pd.IndexSlice
    if flag_outformat=='pct':
        all_df=df.groupby(subject)[var].mean()
        ##By condition
        cond1_df=df[(df[condition]==cond1)].groupby(subject)[var].mean()
        cond2_df=df[(df[condition]==cond2)].groupby(subject)[var].mean()
        ##By condition and block
        if include_blocks == True:
            blcnd=df.groupby([subject,condition,block])[var].mean()
    elif flag_outformat=='sum':
        all_df=df.groupby(subject)[var].sum()
        ##By condition
        cond1_df=df[(df[condition]==cond1)].groupby(subject)[var].sum()
        cond2_df=df[(df[condition]==cond2)].groupby(subject)[var].sum()
        ##By condition and block
        if include_blocks == True:
            blcnd=df.groupby([subject,condition,block])[var].sum()
    elif flag_outformat=='count':
        all_df=df.groupby(subject)[var].count()
        ##By condition
        cond1_df=df[(df[condition]==cond1)].groupby(subject)[var].count()
        cond2_df=df[(df[condition]==cond2)].groupby(subject)[var].count()
        ##By condition and block
        if include_blocks == True:
            blcnd=df.groupby([subject,condition,block])[var].count()
    if (include_blocks == True) and (biat==False):
        cond1_bl1=blcnd.loc[idx[:,cond1,[blocks[0],blocks[2]]]]
        cond1_bl2=blcnd.loc[idx[:,cond1,[blocks[1],blocks[3]]]]
        cond2_bl1=blcnd.loc[idx[:,cond2,[blocks[0],blocks[2]]]]
        cond2_bl2=blcnd.loc[idx[:,cond2,[blocks[1],blocks[3]]]]
        #Drop block and condidition levels to subtract means
        for df_tmp in [cond1_bl1,cond1_bl2,cond2_bl1,cond2_bl2]:
            df_tmp.index=df_tmp.index.droplevel([1,2])
        out=pd.concat([all_df,cond1_df,cond2_df,cond1_bl1,cond1_bl2,cond2_bl1,cond2_bl2],axis=1)

    elif (include_blocks == True) and (biat==True):
        if len(blocks)>=2:
            cond1_bl1=blcnd.loc[idx[:,cond1,[blocks[0],blocks[1]]]]
            cond2_bl1=blcnd.loc[idx[:,cond2,[blocks[0],blocks[1]]]]
            for df_tmp in [cond1_bl1,cond2_bl1]:
                df_tmp.index=df_tmp.index.droplevel([1,2])
            out=pd.concat([all_df,cond1_df,cond2_df,cond1_bl1,cond2_bl1],axis=1)
        if len(blocks)>=4:
            cond1_bl2=blcnd.loc[idx[:,cond1,[blocks[2],blocks[3]]]]
            cond2_bl2=blcnd.loc[idx[:,cond2,[blocks[2],blocks[3]]]]
            for df_tmp in [cond1_bl2,cond2_bl2]:
                df_tmp.index=df_tmp.index.droplevel([1,2])
            out=pd.concat([out,cond1_bl2,cond2_bl2],axis=1)
        if len(blocks)==6:
            cond1_bl3=blcnd.loc[idx[:,cond1,[blocks[4],blocks[5]]]]
            cond2_bl3=blcnd.loc[idx[:,cond2,[blocks[4],blocks[5]]]]
            for df_tmp in [cond1_bl3,cond2_bl3]:
                df_tmp.index=df_tmp.index.droplevel([1,2])
            out=pd.concat([out,cond1_bl3,cond2_bl3],axis=1)
    elif include_blocks == False:
        out=pd.concat([all_df,cond1_df,cond2_df],axis=1)
    return(out)


def error_fastslow_column_names(cond1,cond2,fast_rt,slow_rt,blocks,weighted):
    '''
    Provide names for columns that include the condition name as well as the ms entered for too fast\too slow trials.

    08-2017
    Alexander Millner <alexmillner@gmail.com
    '''
    if weighted == True:

        #All column names for output
        col_names=['overall_error_rate','%s_error_rate'%cond1,'%s_error_rate'%cond2]
        for bl in range(1,int(len(blocks)/2)+1):
            col_names.append('%s_bl%d_error_rate'%(cond1,bl))
            col_names.append('%s_bl%s_error_rate'%(cond2,bl))

        col_names.extend(['overall_fast_rt_rate_%dms'%(fast_rt),\
        '%s_fast_rt_rate_%dms'%(cond1,fast_rt),'%s_fast_rt_rate_%dms'%(cond2,fast_rt)])
        for bl in range(1,int(len(blocks)/2)+1):
            col_names.append('%s_bl%d_fast_rt_rate_%dms'%(cond1,bl,fast_rt))
            col_names.append('%s_bl%d_fast_rt_rate_%dms'%(cond2,bl,fast_rt))

        col_names.extend(['overall_slow_rt_rate_%dms'%(slow_rt),\
        '%s_slow_rt_rate_%dms'%(cond1,slow_rt),'%s_slow_rt_rate_%dms'%(cond2,slow_rt)])
        for bl in range(1,int(len(blocks)/2)+1):
            col_names.append('%s_bl%d_slow_rt_rate_%dms'%(cond1,bl,slow_rt))
            col_names.append('%s_bl%d_slow_rt_rate_%dms'%(cond2,bl,slow_rt))
        col_names.append('num_blocks')
    
    elif weighted == False:

        #All column names for output
        col_names=['overall_error_rate','%s_error_rate'%cond1,'%s_error_rate'%cond2,\
        
        'overall_fast_rt_rate_%dms'%(fast_rt),\
        '%s_fast_rt_rate_%dms'%(cond1,fast_rt),'%s_fast_rt_rate_%dms'%(cond2,fast_rt),\
    
        'overall_slow_rt_rate_%dms'%(slow_rt),\
        '%s_slow_rt_rate_%dms'%(cond1,slow_rt),'%s_slow_rt_rate_%dms'%(cond2,slow_rt)]
        
    #Column names for 1\0 output regarding which criteria were flagged (errors, too many fast or slow trials)
    flag_col_names= ['%s_flag'%i for i in col_names]
        
    return(col_names,flag_col_names)

def num_trls_column_names(cond1,cond2,fast_rt,slow_rt,blocks,incl_excl_switch,weighted):
    '''Column names for number of trials overall, within condition and within block 
       (with a switch to name both before and after excluding fast\slow trials).

    08-2017
    Alexander Millner <alexmillner@gmail.com
    '''
    if weighted == True:
        block_num_col_names=['overall_num_trls_%s_fastslow_rt'%(incl_excl_switch),\
        '%s_num_trls_%s_fastslow_rt'%(cond1,incl_excl_switch),'%s_num_trls_%s_fastslow_rt'%(cond2,incl_excl_switch)]
        for bl in range(1,int(len(blocks)/2)+1):
            block_num_col_names.append('%s_bl%d_num_trls_%s_fastslow_rt'%(cond1,bl,incl_excl_switch))
            block_num_col_names.append('%s_bl%d_num_trls_%s_fastslow_rt'%(cond2,bl,incl_excl_switch))
    elif weighted == False:
        block_num_col_names=['overall_num_trls_%s_fastslow_rt'%(incl_excl_switch),\
        '%s_num_trls_%s_fastslow_rt'%(cond1,incl_excl_switch),'%s_num_trls_%s_fastslow_rt'%(cond2,incl_excl_switch)]
    return(block_num_col_names)

def get_error_fastslow_rates(df,correct,subject,condition,block,cond1,cond2,blocks,flag_outformat,include_blocks,\
    rt,fast_rt,slow_rt,error_or_correct,weighted,errors_after_fastslow_rmvd,df_fastslow_rts_rmvd,biat):
    '''
    Uses blcnd_extract function to get error rates, fast slow rates, etc... 
  
    08-2017
    Alexander Millner <alexmillner@gmail.com
    '''
   ##Errors
    if errors_after_fastslow_rmvd == False:
        df_err=df
    elif errors_after_fastslow_rmvd == True:
        df_err=df_fastslow_rts_rmvd
    ###Can enter either column where errors are 1 and correct responses are 0 or vice versa
    if error_or_correct=='error':
        err_vars=blcnd_extract(df_err,correct,subject,condition,block,cond1,cond2,blocks,biat,flag_outformat,include_blocks)
    elif error_or_correct=='correct':
        err_vars=1-blcnd_extract(df_err,correct,subject,condition,block,cond1,cond2,blocks,biat,flag_outformat,include_blocks)

    #Fast RT
    df['fast_rt']=(df[rt]<fast_rt)*1
    fast_rt_vars=blcnd_extract(df,'fast_rt',subject,condition,block,cond1,cond2,blocks,biat,flag_outformat,include_blocks)

    #Slow RT
    df['slow_rt']=(df[rt]>=slow_rt)*1
    slow_rt_vars=blcnd_extract(df,'slow_rt',subject,condition,block,cond1,cond2,blocks,biat,flag_outformat,include_blocks)

    if weighted == True:
        ## Number of blocks for each subject
        num_blocks=df.groupby([subject])[block].unique().apply(lambda x: len(x))

        outcms=[err_vars,\
        fast_rt_vars,\
        slow_rt_vars,\
        num_blocks]

    elif weighted == False:
        outcms=[err_vars,\
        fast_rt_vars,\
        slow_rt_vars]

    return(outcms)

def analyze_iat(df,subject,rt,correct,condition,cond1,cond2,block='block',blocks=[2,3,5,6],weighted=True,\
        fast_rt=400,slow_rt=10000,\
        overall_err_cut=.3,cond_err_cut=.4,block_err_cut=.4,\
        overall_fastslowRT_cut=.10,cond_fastslowRT_cut=.25,block_fastslowRT_cut=.25,\
        num_blocks_cutoff=4,\
        fastslow_stats=False,biat=False,biat_rmv_xtrls=4,biat_trl_num=False,\
        error_or_correct='correct',errors_after_fastslow_rmvd=False,flag_outformat='pct',print_to_excel=False,\
        each_stim=False,stimulus=False):

    """Takes a dataframe containing raw IAT (or BIAT) data (all trials, all subjects) and returns
         the number of blocks, percentage of errors, reaction times that are too fast and too slow, 
         flags to remove subjects and D scores for each subject.

     Parameters
     ----------
     df : pandas dataframe 
         Trial x trial IAT data for each subject
     subject : str
         Column name containing subject number
     rt : str
         Column name containing reaction time (in ms) for each trial
     correct : str
         Column name containing whether trial was correct (where correct = 1, error = 0)
         (can also use if columns specifies errors; see 'error_or_correct' parameter)
     condition : str
         Column name containing condition (e.g. Black-Good\White-Bad vs. Black-Bad\White-Good)
     cond1 : str
         Name of first condition (e.g. 'Black-Good\White-Bad'): bias for this condition will result in negative D score  
     cond2 : str
         Name of second condition (e.g. 'Black-Bad\White-Good'): bias for this condition will result in positive D score
     block : str
         Column that contains block information
     blocks : list
         A list containing the numbers corresponding to the relevant blocks, default : [2,3,5,6]
     weighted : Boolean
         If True return weighted D scores; if False return unweighted D scores, default : True
     fast_rt : int
         Reaction time (in ms) considered too fast, default: 400
     slow_rt : int
         Reaction time (in ms) considered too slow, default: 10000
     overall_err_cut : float
         Cutoff for subject exclusion: overall error rate (decimal), default : .3
     cond_err_cut : float
         Cutoff for subject exclusion: error rate (decimal) within each condition, default : .4
     block_err_cut : float
         Cutoff for subject exclusion: error rate (decimal) within a single block, default : .4
     overall_fastslowRT_cut=.10
         Cutoff for subject exclusion: overall rate of trials with too fast or too slow RT (decimal), default : .1
     cond_fastslowRT_cut : float
         Cutoff for subject exclusion: rate of trials with too fast or too slow RT (decimal) within each condition, default : .25
     block_fastslowRT_cut : float
         Cutoff for subject exclusion: rate of trials with too fast or too slow RT (decimal) within each block, default : .25
     num_blocks_cutoff : int
         Cutoff for subject exclusion: Minimum number of blocks required, default : 4
     error_or_correct : str
          Enter 'error' to enter a column for 'correct' where error = 1, correct = 0, default: 'correct'
     errors_after_fastslow_rmvd : Boolean
          If True calculates error rates after removing all fast\slow trials (similar to R package iat); if False error rates calculated with all trials, default : False
     fastslow_stats : Boolean
         Return a second dataframe containing the number and percentage of fast\slow trials across all subjects
         and across subjects with usable data, default : False
     biat : Boolean
          Enter True if analyzing a Brief Implicit Assoc Test (BIAT), False if regular IAT, default : False
          *** One open issue with BIAT flags in pyiat is that currently flags for fast and slow trials use the same cutoff pct.
              Recommended scoring procedures (Nosek et al. 2014) recommend a flag for fast trials but not slow. 
              This is not currently possible in pyiat. However, you can see the pct of slow and fast trials 
              and create your own flags from this.***
     biat_rmv_xtrls : int
          Number of trials to remove from beginning of each block. BIAT recommendad scoring procedures (Nosek et al. 2014) remove first 4 trials of each block b/c 
          they are practice trials but not all BIAT have practice trials, default : 4
     biat_trl_num : str
         The name of the column that contains trial number, default : False
     flag_outformat : str
         Can enter 'count' to return number of errors and too fast\slow trials (if fastslow_stats set to True), default : 'pct'
     print_to_excel : Boolean
         Print an excel workbook that contains output, default : False
     each_stim : Boolean
         Return D scores for each individual stimulus (i.e. word), default : False
     stimulus : Boolean
         If each stim = True, then give name of column containing each stimulus (i.e. word), default : False

     Returns
     -------
     pandas DataFrame with 
        -error rates (overall, each condition, each block (error rates *include* fast\slow trials)),
        -rates of fast\slow trials (overall, each condition, each block)
        -exclusion flags (overall flag indicating subject should be excluded and for each category informing why subject was flagged)
        -D scores (overall and block 1 and block 2 if weighted)
    if fastslow_stats = True:
        pandas DataFrame with rates of fast\slow trials across all subjects and across only subjects NOT flagged for exclusion
        (to report the overall number\pct of trials excluded from a study)

     Examples
     --------
     >>> weighted_d,fastslow_stats_df=iat(it,subject='session_id',rt='latency',
     ...                 condition='cond',correct='correct',
     ...                 cond1='nosh_me',cond2='sh_me',block='block',
     ...                 blocks=[2,3,5,6],fastslow_stats=True,each_stim=False,
     ...                 stimulus='trial_name')
    
    Copyright (C) 2017 Alexander Millner <alexmillner@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    """
    idx=pd.IndexSlice
    df=df[(df[condition]==cond1)|(df[condition]==cond2)].copy(deep=True)

    if df[df[correct]>1].shape[0]!=0 or df[df[correct]<0].shape[0]!=0:
        raise ValueError('The \'correct\' column can only contain the values 0 and 1')

    #For weighted d scores, we return all block-related stats whereas 
    #for unweighted we are just comparing conditions and care less about blocks
    include_blocks=weighted

    #Make column names
    col_names,flag_col_names=error_fastslow_column_names(cond1,cond2,fast_rt,slow_rt,blocks,weighted)
    block_num_col_names_incl=num_trls_column_names(cond1,cond2,fast_rt,slow_rt,blocks,'incl',weighted)
    block_num_col_names_excl=num_trls_column_names(cond1,cond2,fast_rt,slow_rt,blocks,'excl',weighted)

    if biat == True:
        df_orig=df.copy()
        #This finds all unique trials numbers, sorts them and must be greater than the 4th item 
        df=df[df[biat_trl_num]>=sorted(df[biat_trl_num].unique())[biat_rmv_xtrls]]
        df.loc[(df[rt]>2000)&(df[rt]<10000),rt]=2000
        df.loc[df[rt]<400,rt]=400

    #Make dfs where trials that are too fast or too slow are removed
    df_fastslow_rts_rmvd=df[-(df[rt]>=slow_rt)]
    if biat == False:
        df_fastslow_rts_rmvd=df_fastslow_rts_rmvd[-(df_fastslow_rts_rmvd[rt]<fast_rt)]

    #Get error and fast\slow trials
    outcms=get_error_fastslow_rates(df,correct,subject,condition,block,cond1,cond2,blocks,flag_outformat,include_blocks,\
    rt,fast_rt,slow_rt,error_or_correct,weighted,errors_after_fastslow_rmvd,df_fastslow_rts_rmvd,biat)

    #Figure out number of trials after removing fast\slow rt trials 
    #in each block and total number of fast and slow trials (and remove them)
    pre_trl_count_vars=blcnd_extract(df,rt,subject,condition,block,cond1,cond2,blocks,biat,flag_outformat='count',include_blocks=include_blocks)
    pre_trl_count_vars.columns=block_num_col_names_incl

    post_trl_count_vars=blcnd_extract(df_fastslow_rts_rmvd,rt,subject,condition,block,cond1,cond2,blocks,biat,flag_outformat='count',include_blocks=include_blocks)
    post_trl_count_vars.columns=block_num_col_names_excl

    if weighted == True:
        ##Cutoffs for the pct of errors or fast or slow trials that's considered excessive
        cutoffs=[overall_err_cut,cond_err_cut,cond_err_cut]
        cutoffs.extend(list(np.repeat(block_err_cut,len(blocks))))
        cutoffs.extend([overall_fastslowRT_cut,cond_fastslowRT_cut,cond_fastslowRT_cut])
        cutoffs.extend(list(np.repeat(block_fastslowRT_cut,len(blocks))))
        cutoffs.extend([overall_fastslowRT_cut,cond_fastslowRT_cut,cond_fastslowRT_cut])
        cutoffs.extend(list(np.repeat(block_fastslowRT_cut,len(blocks))))
        cutoffs.append(num_blocks_cutoff)
    
    elif weighted == False:
        ##Cutoffs for the pct of errors or fast or slow trials that's considered excessive
        cutoffs=[overall_err_cut,cond_err_cut,cond_err_cut,\
                 overall_fastslowRT_cut,cond_fastslowRT_cut,cond_fastslowRT_cut,\
                 overall_fastslowRT_cut,cond_fastslowRT_cut,cond_fastslowRT_cut]

    #Put together and put into rates - containing just the rates - 
    #and flags (i.e. whether the rate ) is over a threshold
    flags=pd.DataFrame(columns=flag_col_names,index=(df.groupby([subject])[subject].apply(lambda x: x.unique()[0])).tolist())
    rates=pd.concat(outcms,axis=1)
    rates.columns=col_names

    for col,fcol,cutoff in zip(col_names,flag_col_names,cutoffs):
        if col!='num_blocks':
            flags.loc[:,fcol]=((rates[col]>cutoff)*1)
        elif col=='num_blocks':
            flags.loc[:,fcol]=((rates[col]<cutoff)*1)
        
    flags['iat_flag']=flags.sum(axis=1)

    all_num_trl_per_block=pd.concat([pre_trl_count_vars,post_trl_count_vars],axis=1)

    #Get D scores with df with removed fast\slow trials
    d=iat_get_dscore(df_fastslow_rts_rmvd,subject,rt,block,condition,cond1,cond2,blocks,weighted,biat,each_stim,stimulus)
    
    all_iat_out = pd.concat([all_num_trl_per_block,rates,flags,d],axis=1)

    if each_stim==False:
        all_iat_out.loc[all_iat_out.dscore.isnull(),'iat_flag']=all_iat_out.loc[all_iat_out.dscore.isnull(),'iat_flag']+1

    #Print output to excel
    if print_to_excel==True:

        from datetime import datetime
        dt=datetime.now()
        dt=dt.strftime('%m_%d_%Y_%H_%M_%S')

        iat_excel = pd.ExcelWriter('pyiat_output_%s.xlsx'%dt)
        all_iat_out.to_excel(iat_excel,sheet_name='pyiat')


    if fastslow_stats == True:
        if biat == True:
            df=df_orig
        all_fast_slow_rt=overall_fast_slow_stats(df,rt,fast_rt,slow_rt,subject,flags)
        if print_to_excel==True:
            all_fast_slow_rt.to_excel(iat_excel,sheet_name='Num_Pct_Fast_Slow_RT_Trials')
            iat_excel.save()
        return(all_iat_out,all_fast_slow_rt)


    elif fastslow_stats == False:
        if print_to_excel==True:
            iat_excel.save()
        return(all_iat_out)

