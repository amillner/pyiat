pyiat v.02
=================

pyiat is a Python package to analyze data from the Implicit Association Test (IAT) consistent with the standard IAT scoring algorithm (Greenwald et al., 2003) and Brief IAT scoring algorithm (Nosek et al., 2014). pyiat requires that data are in a pandas DataFrame. 

	Greenwald, A. G., Nosek, B. A., & Banaji, M. R. (2003). Understanding and using the Implicit Association Test: I. An improved scoring algorithm. Journal of Personality and Social Psychology, 85(2), 197–216. https://doi.org/10.1037/0022-3514.85.2.197

	Nosek, B. A., Bar-Anan, Y., Sriram, N., Axt, J., & Greenwald, A. G. (2014). Understanding and Using the Brief Implicit Association Test: Recommended Scoring Procedures. PLOS ONE, 9(12), e110938. https://doi.org/10.1371/journal.pone.0110938

Features
--------

pyiat currently supports the following features:

* Analysis of the IAT and Brief IAT (BIAT) 
* IAT can be analyzed with weighted or unweighted algorithm
* For BIAT can analyze 1, 2, or 3 blocks 
* Obtain D scores for each stimulus (e.g. word)
* Output includes overall error percentage as well as error percentages by block (if using a weighted score) and by condition 
* Same output (overall, by block, by condition) for trials considered too fast or too slow
* Can set reaction time of trials considered too fast or too slow
* Can set cutoffs for error/too fast/too slow flags indicating that a participant is excluded for poor performance
* Can print output to Excel 
* Can return the total number and percentage of trials removed because they were too fast or too slow  


Documentation
-------------

.. toctree::
   :maxdepth: 2

   userguide
   arguments


How to get help or provide feedback
------------------------------------------------

For help or feedback, please enter an `issue on Github`_

Source code
-----------

You can access the source code at: https://github.com/amillner/pyiat

.. Links

.. _`issue on Github`: https://github.com/amillner/pyiat/issues
