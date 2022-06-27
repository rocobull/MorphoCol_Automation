# Context
The work presented here was part of a Bioinformatics Master's degree project.

The objective was to integrate an automated morphological feature attribution pipeline to MorphoCol's software (http://stardust.deb.uminho.pt/morphocol/).
Currently, 3 parameters were automated using a test set of 135 colony images of different morphotypes: **Type of Surface**, **Form** and **Size** (referring to CMO term groups).

NOTE: At this point, the **Size** term group still only returns the estimated diameter, requiring a formal term estimation.

# Abstract
Antimicrobial resistance (AMR) has become a deadly issue with the discovery and increasing use of different antibiotics. The resulting resistant strains have developed characteristics that protect them from treatment, such as the formation of biofilms, characteristics that can indirectly be identified through their colony's physical characteristics. Previous studies have explored the importance of colony morphotyping to assist in predicting the presence (or absence) of resistant phenotypes, resulting in the creation of Colony Morphology Ontology (CMO) terms, and a manual morphotyping software called MorphoCol. In this study, 3 of the 10 CMO groups, "Type of surface, "Form" and "Size", were automated, using calculations made by ImageJ, the image analysis software, to discriminate between the CMO terms of each respective group. This was done with the help of decision tree models, using R packages, and downloadable plugins for ImageJ. In the future, this framework could be included in MorphoCol's software to automate as many morphology features as possible to help investigators predict the presence of resistant phenotypes in their colony populations.

# File information
### 
