# Bureau d'étude Master 1 : EURIA
### A - BUT
Sous la tutelle de l'équipe Data scientist de Arkea et de Euro Institut Actuariat ce projet à pour but l'extraction de transaction automatique issus de relévés de compte by the use of deep learning.

### B - Project structure
The project is dived into section each related to the within step. We have four step in our project.
- Step 1 : Build training and testing database for each bank (CMB, HSBC, LCL and SG) / folder 01_create_bases
- Step 2 : Define business and machine learning metrics / folder 02_metriques
- Step 3 : Implement deep learning model / folder 04_models
- Step 4 : Restructure table / on going
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
Each folder (so each step) should be autonomous by itself. So it should be runnable without further file. 
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
  - In modeling : We could try new approches like \verb|Table Transformer|, \verb|TableNet| models which seems and try to evaluate models final results by metrics
  - In database creation : For further improvement, one could add noises in order to build more robust models
  - In data annotation and preparation : May be one step could be to apply table recognition in order to avoid the model dealing with noises.

  Thanks to Arkea, Benno, Franck Vermet and EURIA
