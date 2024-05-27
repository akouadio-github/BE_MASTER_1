# Bureau d'étude Master 1 : EURIA
### A - Our Goal
Under the supervision of Arkea's Data Scientist team and Euro Institut Actuariat, this project aims to extract automatic transactions from account statements by the use of deep learning.

### B - Project structure
The project is dived into section each of which is linked to the stage concerned. We have four stages in our project.
- Stage 1 : Build training and testing database for each bank (CMB, HSBC, LCL and SG) / folder 01_create_bases
- Stage 2 : Define business and machine learning metrics / folder 02_metriques
- Stage 3 : Implement deep learning model / folder 04_models
- Stage 4 : Restructure table / on going
```
└───sources
    ├───01_create_bases
    │    main.py
    ├───02_metriques
    │     metriques.py
    ├───03_annotations
    │   ├───annotated_data
    │   │   ├───test
    │   │   │   ├───annotations
    │   │   │   └───images
    │   │   └───train
    |   labelisation.ipynb
    └───04_modeles
        layoutLM_v1_final.ipynb
```
### C - How to use ?
Each folder (so each step) should be autonomous by itself. So it should be runnable without further file. Indeed, we have either an .py file or .ipynb (a notebook) which are more or less described.
- In the database creation step, one should run the main.py file in order to generate new database. For instance, the below code will generate n=1500 images per bank.
  ```
  python main.py -n 1500
  ```
- The 02_metriques folder refers to the builded business metrics to evaluate the extraction performance. Please refers to the reports for more details. However, the implementation is well define in the folder. Each metric is normaly define in a function and how to use it should be precise.
- The annotation step was mainly for preparing for modeling. The output of this step is normaly the annotated images and it was pushed on huggingface on xilpam repository. It should be opensource soon.
- The model section should present all the tested models. At this stage we still trying to use LayoutLM for token classification.

### E - Next step
  At this moment, we dealing with LayoutLM, we have first results. And we are trying to use the LayoutLM outcome to well restruct table. Basically, this could be done by an heuristic. As show in the above figure.
  
### D- Further improvement
  Improvements may concerns any level of the project from database to modeling. But mainly in the modeling step.
  - In modeling : We could try new approches like <b>Table Transformer</b>, <b>TableNet</b> models which we didn't dive in and try to evaluate them by business metrics. Also in the OCR before LayoutLM we should optimize hyperparameters.
  - In database creation : For further improvement, one could add noises in order to build more robust models. May be diversify transactions and probably try foreign bank statements
  - In metrics : We should be more restrictive in order to well evaluate models.
  - In data annotation and preparation : May be one step could be to apply table recognition in order to avoid the model dealing with noises.
  - In this project, we didn't focus on image preprocessing before diving into modeling. So one could as improvement add a new block of "image preprocessing"


  Thanks to Arkea and EURIA specifically to Riwal, Yoann, Benno, Franck Vermet 


  **- Authors** : 
  Aristide, Mathis, Romain Actuary students

  ### F - Droits d'auteur

Ce projet peut être utilisé à titre d'apprentissage, mais nous ne sommes aucunement responsables des utilisations qui en sont faites.
