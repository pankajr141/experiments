| SNO | Name | Algorithm | Description
| --- | --- | --- | --- |
| 101 | GAN_101_Mnist.ipynb  | Basic GAN | • Standard GAN with Generator and Discriminator <br>• BCE Loss
| 102 | GAN_102_DCGAN_Mnist.ipynb | GAN with CNN | • Feed Forward Layers of Discriminator and Generator Replace by Deep Convolution Layers
| 103 | GAN_103_WGAN_GP_Mnist.ipynb | Wasserstein GAN with Gradient Penalty | • Mode Collapse and Vanishing Gradient issues resolved by replacing BCE-Loss with Wasserstein Loss (Earth mover distance implementation) <br> • Gradient penalties added to prevent mode collapse. <br>• Discriminator class is replaced by critic - As a result instead of probability range 0-1, critic output number of any value.
| 104 | GAN_104_Conditional_GAN_Mnist.ipynb  | DCGAN with Multiple Classes| • Support for multiple types of output<br>• class vector appended with noise specify which class to be output
| 105 | GAN_105_Spectrally_Normalized_GAN_Mnist.ipynb | DCGAN with spectral normalzation | • weight normalization to to stabilize the training of the discriminator.<br>•  improve stability and avoid vanishing gradient problems, such as mode collapse
| 106 | GAN_106_Controllable_Generation.ipynb  | DCGAN with Feature control | • Pretrained classifier for noise vector tuning.<br>• control Descrired features like age, smile by tuning noise vector.
