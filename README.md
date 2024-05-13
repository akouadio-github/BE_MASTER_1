# Bureau d'étude Master 1 : EURIA
### A - BUT
Sous la tutelle de l'équipe Data scientist de Arkea et de Euro Institut Actuariat ce projet à pour but l'extraction de transaction automatique issus de relévés de compte by the use of deep learning.

### B - Project structure
The project is dived into section each related to the within step. We have four step in our project.
- Step 1 : Build training and testing database (folder 01_create_bases)
- Step 2 : Define business and machine learning metrics (folder 02_metriques)
- Step 3 : Implement deep learning model (folder 04_models)
- Step 4 : Restructure table (on going)
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
