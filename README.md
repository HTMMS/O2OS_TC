## Traffic Classification Code - O2OS


### Online and Offline Two-Stage Classification
`OL_Classifier.py` reads a CSV file and performs two-stage classification.

## OL_Classifier_ratio
Code for two-stage classification (sequence recognition and feature identification).

The **modelpath** is the location where well-trained models are stored. The models are saved in the format of `1_XX.m` and `2_XX.m`, which are used for the first-stage sequence recognition and the second-stage feature identification, respectively. The features used are `pl_iat` and `select_features`.

**tor** and **nor** are directories for storing the testing datasets for TOR and normal traffic, respectively.

### Origin Method
The original traffic recognition method. Modify the data reading part in `Classifier.py` and run the code. The models are saved in the "models" folder.

### Baseline Method
Initial recognition performance of O2OS.

- Model Generation: Modify the `modelpath` to specify the model storage path in `OL_Classifier_models.py`. Set **borderline=0** and **adaboostout = 0**.

- Model Testing: Modify **ensembleout = 0** in `OL_Classifier_ratio.py`. Select the test dataset paths for NOR and the model path, and modify the values of `lowbound` and `uppbound`.

### Borderline Optimization
Generate samples using the borderline method and modify the distribution of the test dataset to bias the classifier.

- Model Generation: Modify the `modelpath` to specify the model storage path in `OL_Classifier_models.py`. Set **borderline=1** and **adaboostout = 0**. You can modify the sample quantity to be generated and which class to increase, which will bias the classifier towards that class.

- Model Testing: Modify **ensembleout = 0** in `OL_Classifier_ratio.py`. Select the test dataset paths for NOR and the model path, and modify the values of `lowbound` and `uppbound`.

### Adaboost Optimization
Adopting the Adaboost concept, the training samples for the second-stage offline classification are not normal samples, but rather TOR samples and the misclassified samples from the first-stage online classification.

- Model Generation:

1. In `OL_Classifier_models.py`, **ensure that the normal training traffic in `norpath` is abundant**. Select an appropriate number of normal samples for training and save the misclassified results. Modify the `modelpath` to specify the model storage path, and set **borderline=0** and **adaboostout = 1**. Modify `adaboostpath` to store the misclassified results.

2. Run `OL_Classifier_models_adaboost.py`. Modify the five `norpath` variables and `modelpath`, where `modelpath` should be the same as the previous one. After running, go to the model path. The newly generated models are named in the format of 2_*.m, where * is a number. The order is c45, gbdt, knn, rf30.

- Model Testing: Modify **ensembleout = 0** in `OL_Classifier_ratio.py`. Select the test dataset paths for NOR and the model path, and modify the values of `lowbound` and `uppbound`.

### Ensemble Optimization
Adopting the ensemble learning concept to integrate the results from different classifiers.

- Preliminary Classification Results: In `OL_Classifier_ratio.py`, run a pre-existing model, which can be any of the previous baseline, borderline, or adaboost methods. However, set **ensembleout = 1** to save the original labels and sixteen classification results in `ensemble.csv`.

- Integration of Classification Results: In `ensemble.py`, modify the `file` to the path of `ensemble.csv`. There are three integration strategies: naive, slightly, and strong, representing different rejection granularities. Modify pages 83-85 and 93-95.

1. Naive: Majority voting. If there is a 2:2 tie or all four classification results are different, classify it as normal.
2. Slightly: Weak negation. If the classification is normal, classify it as normal; otherwise, follow the majority voting principle.
3. Strong: Strong negation. If the four voting results do not exceed three votes, classify it as normal.

### Entirety Optimization
In the O2OS system, combining the borderline method, adaboost method, and ensemble method. Use the borderline method to modify the training sample distribution and bias the classifier towards normal. Use the adaboost method to focus the second-stage offline recognition on identifying the misclassified results from the first-stage. Use the ensemble method to integrate the classification results.

- Model Generation:
1. In `OL_Classifier_models.py`, modify the `modelpath` to specify the model storage path. Set **borderline=1** and **adaboostout = 1**. You can modify the sample quantity to be generated and which class to increase, which will bias the classifier towards that class. **Ensure that the normal training traffic in `norpath` is abundant**.

2. Run `OL_Classifier_models_adaboost.py`. Modify the five `norpath` variables and `modelpath`, where `modelpath` should be the same as the previous one. After running, go to the model path. The newly generated models are named in the format of 2_*.m, where * is a number. The order is c45, gbdt, knn, rf30.

- Preliminary Classification Results: In `OL_Classifier_ratio.py`, modify the respective paths. Set **borderline=0** and **adaboostout = 1**, and output the classification label results.

- Integration of Classification Results: In `ensemble.py`, modify the `file` to the path of `ensemble.csv`. There are three integration strategies: naive, slightly, and strong, representing different rejection granularities. Modify pages 83-85 and 93-95.

1.	naïve: Applies the majority voting principle and, in the event of a tie, selects the class with the highest precision among the classifiers, considering classifier bias.
2.	slightly: Classifies a sample as normal if the consensus vote of the classifiers is less than 3.;
3.	strong: Considers a sample as normal in the online phase if any one of the four classifiers assigns a normal classification, while in the offline phase, the decision is made based on majority voting.
