# Image Classification Speed Test

This example is based on a 
[PyTorch Lightning](https://github.com/PyTorchLightning/pytorch-lightning/blob/master/pl_examples/domain_templates/computer_vision_fine_tuning.py)
image classification with transfer learning code. The provided `run.sh` script will build a docker container for you and run the test.  You can edit the 
script and specify the batch size, number of epochs, GPUs (set to 0 for a CPU test), and well as the number of cores / workers. 

On a GPU, this test takes just a 
few minutes to run, depending on the model. It will likely take quite a bit longer on CPU.
