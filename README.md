# paper_PyMyoVent_growth_valve
This repository holds essential files for the growth paper due to valvular disorders with PyMyoVent submitted to Frontiers in Physiology. 

- To reproduce all figures shown in the paper, you need to follow the below steps:

In general, the whole proccess can be divided into three main steps:

| **Step Number** | **Description** |
| ------ | ------- |
| 1 | Generating a batch file of required input files for PyMyoVent |
| 2 | Running PyMyoVent using generated input files in step 1. |
| 3 | Generating figures using simulated raw data from step 2. |  

Let's start ....

## Step1: Generating a batch file of required input files for PyMyoVent

1. First clone the repository on your local computer.

2. On your computer terminal prompt, navigate to the folder where the repositore is already stored:
- `$cd <path_to_repo_on_your_computer>`

3. Handle all required dependencies for generating figures by running the following command in terminal prompt:
- `$ pip install -r requirements.txt`

4. After successfully installing the required packages, you can generate a batch file for all simulations used in this paper by doing following steps:  
- Navigate to the `simulations` folder in the repository : `$cd simulations`. 
- Run the python file `batch_generator.py` via following command:
`$ python batch_generator.py`
- In couple of second you should see a batch file named `batch.json` along all folders containing the required "input" files are generated in `simulations` folder. The `batch.json` file would look like this:

![batch](snapshots/batch.png)

## Step2: Running PyMyoVent using generated input files in step 1.
1. you need to find out the absolute path to your `batch.json` file in the `simulations` folder. To do that:

    - On your terminal prompt, while you are in the `simulations` folder run the following command: 
        - mac: `$ pwd` 
        - windows: `$cd`
    - In a second, the absolute path (highlighted) to the `simulations` file would be shown on your terminal prompt:
    ![abs_path](snapshots/abs_path.png)
    - Copy the absolute path.
2. Open another terminal prompt and navigate to PyMyoVent/Python_code folder on your local computer. 
`$cd <path_to_PyMyoVent>/Python_code`.

- Note: If you don't have PyMyoVent repository on your computer check [this](https://campbell-muscle-lab.github.io/PyMyoVent/pages/installation/installation.html) to see how to clone it.

3. Now run PyMyovent code and and give the absolute path to `batch.json` file as an argument to the code:
`$python PyMyoVent.py <absolute_path_to_simulations_folder>/batch.json`

![run_pymyovent](snapshots/run_pymyovent.png)
- This would take several hours to run all simulations on a personal computer. 

## Step3: Generating figures using simulated raw data from step 2.

Once you have all simulated results in the `simulations` folder. 
1. On your first terminal prompt window that you used for step 1, navigate to `analysis` folder by following command:
`$cd ../analysis`.

2. Run `generate_figs.py` script with the following argument input:
`$python generate_figs.py all_figures`
![all_figures](snapshots/all_figs.png)

- It takes several minutes to read raw data, do some processing on them, and finally generate all figures. 
- Figures will be stored in the `figures` folder in the main root of the repository. 


