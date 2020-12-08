Generative adversarial network (GAN)
	• Standard GAN with Generator and Discriminator
	• BCE Loss

Deep convolutional GAN (DC-GAN)
	• Feed Forward Layers of Discriminator and Generator Replace by Deep Convolution Layers

Wasserstein GAN with Gradient Penalty(WGAN-GP)
	• Mode Collapse and Vanishing Gradient issues resolved by replacing BCE-Loss with Wasserstein Loss (Earth mover distance implementation)
	• Gradient penalties added to prevent mode collapse.
	• Discriminator class is replaced by critic - As a result instead of probability range 0-1, critic output number of any value.
