# optiflow
<img src="Images/optiflow_logo.png" alt="drawing" width="500"/>

**optiflow** is an algorithm designed to reconstruct **velocity fields** from **kymographs** with **optimal transport**. Indeed, optimal transport computes the velocity field of minimal work, which is relevant under a wide array of situations and does not necessitates hard physical assumptions, except for the conservation of the physical quantity that we are measuring across time.
This software is designed to offer cell biologists a simple method to obtain flow fields around a membrane contour (taking into account boundary conditions) for free, offering a quantitative measurement for a flow that can only be observed visually otherwise.


---
## Introductory notebook
<img src="Images/optiflow_example.png" alt="drawing" width="500"/>
An example is provided in the jupyter notebook Optiflow_presentation.ipynb

---

## Installation
To install the package 

`python -m pip install optiflow`

---

**optiflow** was created by Sacha Ichbiah during his PhD in [Turlier Lab](https://www.turlierlab.com), and originated from a collaboration with Henry de Belly, with the lab of [Orion Weiner](https://weinerlab.com) and [Carlos Bustamante](https://bustamante.berkeley.edu). It is maintained by Sacha Ichbiah and Hervé Turlier. For support, please open an issue.
A preprint of the paper using this method is available on [BiorXiv](https://www.biorxiv.org/content/10.1101/2022.09.07.507005v1). The data used in the paper are available in [this repo](https://github.com/VirtualEmbryo/membrane-cortex-tension). If you use our library in your work please cite the paper : 

```@inproceedings{HDBSYetal,
  author    = {Henry De Belly, Shannon Yan, Hudson Borja da Rocha, Sacha Ichbiah, Jason P. Town, Hervé Turlier, Carlos Bustamante, and Orion D. Weiner},
  title     = {Actin-driven protrusions generate rapid long-range membrane tension propagation in cells},
  month     = {Sept},
  year      = {2022},
  doi       = {10.1101/2022.09.07.507005}
```



