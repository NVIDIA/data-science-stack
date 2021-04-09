# kNN Speed Test

This example is based on Chris Deotte's [Kaggle notebook](https://www.kaggle.com/cdeotte/rapids-gpu-knn-mnist-0-97/notebook), where a GPU-accelerated kNN classifier is used 
is used in the Kaggle MNIST competition. The GPU / CPU speedup will depend on your hardware, but we routinely see 100+x performance improvements.  On a GPU, 
the 100x inference (cell 13) takes less than a minute to run. To run the same test on CPU, select the number of cores (cell 14) and then run the test in cell 15.

These massive speedups are a game changer when it comes to rapid experimentation, model architecture selection, and hyperparameter optimization. 

To run this example, simply launch the data science stack container or conda environment and run the notebook. Alternatively, you could use one of RAPIDS containers.

