# Bureau d'étude Master 1 : EURIA
### A - BUT
Sous la tutelle de l'équipe Data scientist de Arkea et de Euro Institut Actuariat ce projet à pour but l'extraction de transaction automatique issus de relévés de compte by the use of deep learning.

### B - Project structure
The project is dived into section each related to the within step. We have four step in our project.
- Step 1 : Build training and testing database
- Step 2 : Define business and machine learning metrics
- Step 3 : Implement deep learning model
- Step 4 : Restructure table
```
└───sources
    ├───01_create_bases
    │   ├───configs
    │   ├───static
    │   ├───templates
    │   └───utils
    ├───02_metriques
    ├───03_annotations
    │   ├───annotated_data
    │   │   ├───test
    │   │   │   ├───annotations
    │   │   │   └───images
    │   │   └───train
    │   └───data
    │       ├───testing_data
    │       │   ├───CMB
    │       │   │   ├───annotations
    │       │   │   └───images
    │       │   ├───HSBC
    │       │   ├───LCL
    │       │   └───SG
    │       └───training_data
  ├───

└───04_modeles
    │   ├───configs
```
### C - How to use ?
Each folder (so each step) should be autonomous by itself. So it should be runnable without further file. 
