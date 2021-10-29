# paper_PyMyoVent_growth_valve
This repository holds essential files for the growth paper due to valvular disorders with PyMyoVent submitted to Frontiers in Physiology. 

- For reproducing all figures follow the below steps:

1. First clone the repository on your local computer.

2. On your computer terminal prompt, navigate to the folder where the repositore is already stored:
- `$cd <path_to_repo_on_your_computer>`

3. Handle all required dependencies for generating figures by running the following command in terminal prompt:
- `$ pip install -r requirements.txt`

4. After successfully installing required packages, you can generate a batch file for all simulations used in this paper by doing following steps:  
- Navigate to the `simulations` folder in the repository : `$cd simulations`. 
- Run the python file `batch_generator.py` via following command:
`$ python batch_generator.py`
- In couple of second you should see the following batch file along folders containing the required "input" files are generated in `simulations` are generated:
![batch](snapshots/batch.png)

