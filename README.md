{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Student Groups Optimization"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Use linear programming to assign students to groups subject to constraints specifying:\n",
    "- __INDIVIDUALS__\n",
    "    - __with:__ students to assign to a group together\n",
    "    - __not with:__ students to assign to different groups\n",
    "    - __in:__ students to assign to a specific group\n",
    "    - __not in:__ students not to assign to a specific group\n",
    "- __CHARACTERISTICS__ _--> advanced, disruptive, extrovert, IEP, introvert, male/female_\n",
    "    - __homogenous:__ groups to assign only students with a specified characteristic\n",
    "    - __maximum:__ maximum number of students with specified characteristic per group\n",
    "\n",
    "Review the optimal student groupings in tabular form.\n",
    "\n",
    "<img src=\"images/optimal_student_groupings.png\" title=\"optimal student groupings\">\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Getting Started\n",
    "\n",
    "### Download the repository\n",
    "\n",
    "Click  `Clone or download`  and `Download ZIP`. Once the download is complete, unzip the file and drag it onto your desktop.\n",
    "\n",
    "### Setup a virtual environment with Anaconda\n",
    "\n",
    "The next step is to create a virtual environment on your computer. This environment will hold the Python version and packages necessary for student groups optimization. We can build the environment using the [Anaconda Distribution](https://www.anaconda.com/what-is-anaconda/), a popular Python data science platform for package management and deployment. If you already have Anaconda installed, move on to the next step. Otherwise, [download Anaconda here](https://www.anaconda.com/download/).\n",
    "\n",
    "To confirm Anaconda is installed correctly, [open a terminal window](http://blog.teamtreehouse.com/introduction-to-the-mac-os-x-command-line) and run:\n",
    "\n",
    "```\n",
    "conda --version\n",
    "```\n",
    "\n",
    "You should see the installed version number, such as `conda 4.7.12`. If instead you see an error message, reference [verifying that conda is installed](https://docs.anaconda.com/anaconda/install/verify-install/) in the conda documentation.\n",
    "\n",
    "With Anaconda correctly installed, navigate in the terminal to the `student-groups-optimization-master` directory using the command:\n",
    "\n",
    "```\n",
    "cd Desktop/student-groups-optimization-master/\n",
    "```\n",
    "\n",
    "#### Option 1: Create environment from environment.yml file\n",
    "\n",
    "Once in the correct directory, you can use the `environment.yml` file to create a virtual environment on your computer using the command:\n",
    "\n",
    "```\n",
    "conda env create -f environment.yml\n",
    "```\n",
    "\n",
    "This will install the necessary packages and may take some time to finish. Once the process is complete, run:\n",
    "\n",
    "```\n",
    "conda info --env\n",
    "```\n",
    "\n",
    "to list the virtual environments available on your computer with the active environment identified with an asterisk (*). You should see the new student-groups environment on this list.\n",
    "\n",
    "Activate the `student-groups` virtual environment by running the following command:\n",
    "\n",
    "```\n",
    "source activate student-groups\n",
    "```\n",
    "\n",
    "Verify the `student-groups` environment was installed correctly using:\n",
    "\n",
    "```\n",
    "conda list\n",
    "```\n",
    "\n",
    "You should see a list of packages and package versions installed in your environment, including You should see a list of installed packages and package versions including `jupyter 1.0.0`, `openpyxl 3.0.1`, `pandas 0.25.2`, `pulp 1.6.8`, `python 3.7.5`, and `xlrd 1.2.0` . If instead you see an error message, reference [creating an environment from an environment.yml file](https://conda.io/docs/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) in the conda documentation.\n",
    "\n",
    "#### Option 2: Create an environment and install necessary packages\n",
    "\n",
    "Once in the correct directory, you can create a `student-groups` virtual environment on your computer using the command:\n",
    "\n",
    "```\n",
    "conda create -n student-groups python=3.7.5 pandas=0.25.2 jupyter=1.0.0 xlrd=1.2.0 openpyxl=3.0.1\n",
    "```\n",
    "\n",
    "When prompted to proceed type `y` and hit `Enter`. This will install the correct version of Python along with the correct versions of the pandas, Jupyter, xlrd, and openpyxl packages into a newly created student-groups virtual environment. Note that each installation may take some time to finish.\n",
    "\n",
    "Now activate the `student-groups` environment by running:\n",
    "\n",
    "```\n",
    "source activate student-groups\n",
    "```\n",
    "\n",
    "You need to install one additional package called PuLP using conda-forge before you are ready to optimize student groups. Install the pulp package using the following command\n",
    "\n",
    "```\n",
    "conda install -c conda-forge pulp\n",
    "```\n",
    "\n",
    "When prompted to proceed type `y` and hit `Enter`.\n",
    "\n",
    "Verify your `student-groups` environment is set up correctly using:\n",
    "\n",
    "```\n",
    "conda list\n",
    "```\n",
    "\n",
    "You should see a list of installed packages and package versions including `jupyter 1.0.0`, `openpyxl 3.0.1`, `pandas 0.25.2`, `pulp 1.6.8`, `python 3.7.5`, and `xlrd 1.2.0` . If instead you see an error message, reference [installing packages](https://docs.anaconda.com/anaconda/user-guide/tasks/install-packages/) in the conda documentation.\n",
    "\n",
    "\n",
    "### *Alternative without Anaconda: Install necessary packages*\n",
    "\n",
    "You will need `Python 3.5` or greater along with the `pandas`, `pulp`, `jupyter`, `xlrd`, and `openpyxl` packages to successfully run the student groups optimization program."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Enter data using Google Sheets\n",
    "\n",
    "You are now ready to enter your student, group, and constraint data using Google Sheets!\n",
    "\n",
    "Go to your Google Drive and click `New > Google Sheets`. \n",
    "\n",
    "Go to `File > Open` and select the `Upload` tab. Click `Select a file from your device` and navigate to the `Desktop > student-groups-optimization-master > data` directory. Select the `data_template.xlsx` file and click `Open`.\n",
    "\n",
    "#### Person Setup\n",
    "\n",
    "Go to the `Person Setup` sheet. Delete example data and enter student names and characteristics in the specified columns.\n",
    "\n",
    "<img src=\"images/person_setup.png\" title=\"Person Setup\">\n",
    "\n",
    "- __name:__ enter student name\n",
    "- __advanced:__ enter 1 for advanced student, 0 otherwise\n",
    "- __disruptive:__ enter 1 for distruptive student, 0 otherwise\n",
    "- __extrovert:__ enter 1 for extroverted student, 0 otherwise\n",
    "- __iep:__ enter 1 for IEP student, 0 otherwise\n",
    "- __introvert:__ enter 1 for introverted student, 0 otherwise\n",
    "- __male:__ enter 1 for male student, 0 for female student\n",
    "\n",
    "#### Grouping Setup\n",
    "\n",
    "Go to the `Grouping Setup` sheet. Delete example data and enter grouping ID and size values in the specified columns.\n",
    "\n",
    "<img src=\"images/grouping_setup.png\" title=\"Grouping Setup\">\n",
    "\n",
    "- __group id:__ enter a unique name for each group\n",
    "- __size:__ enter the maximum size for each group\n",
    "\n",
    "#### Constraint - With\n",
    "\n",
    "Go to the `Constraint - With` sheet to specify which (if any) students to assign to a group together.\n",
    "\n",
    "<img src=\"images/constraint_with.png\" title=\"Constraint - With\">\n",
    "\n",
    "- __name 1 - 6:__ enter student names in the same row to ensure assigned to a group together\n",
    "\n",
    "#### Constraint - Not With\n",
    "\n",
    "Go to the `Constraint - Not With` sheet to specify which (if any) students to assign to different groups.\n",
    "\n",
    "<img src=\"images/constraint_not_with.png\" title=\"Constraint - Not With\">\n",
    "\n",
    "- __name 1 - 6:__ enter student names in the same row to ensure assigned to different groups\n",
    "\n",
    "#### Constraint - In\n",
    "\n",
    "Go to the `Constraint - In` sheet to specify which (if any) students to assign to a specific group.\n",
    "\n",
    "<img src=\"images/constraint_in.png\" title=\"Constraint - In\">\n",
    "\n",
    "- __name:__ enter student name\n",
    "- __group id:__ enter specific group to assign to student \n",
    "\n",
    "#### Constraint - Not In\n",
    "\n",
    "Go to the `Constraint - Not In` sheet to specify which (if any) students to not assign to a specific group.\n",
    "\n",
    "<img src=\"images/constraint_not_in.png\" title=\"Constraint - Not In\">\n",
    "\n",
    "- __name:__ enter student name\n",
    "- __group id:__ enter specific group to not assign to student \n",
    "\n",
    "#### Constraint - Homogenous\n",
    "\n",
    "Go to the `Constraint - Homogenous` sheet to specify which (if any) groups to assign only students with a specified characteristic.\n",
    "\n",
    "<img src=\"images/constraint_homogenous.png\" title=\"Constraint - Homogenous\">\n",
    "\n",
    "- __group id:__ enter group to assign only students with specified characteristic and characteristic value\n",
    "- __characteristic:__ specify characteristic\n",
    "- __value:__ specify characteristic value\n",
    "\n",
    "#### Constraint - Maximum\n",
    "\n",
    "Go to the `Constraint - Maximum` sheet to specify the maximum number of students with specified characteristic to assign to each group.\n",
    "\n",
    "<img src=\"images/constraint_maximum.png\" title=\"Constraint - Maximum\">\n",
    "\n",
    "- __maximum:__ enter the maximum number of students with specified characteristic per group\n",
    "- __characteristic:__ specify characteristic\n",
    "- __value:__ specify characteristic value\n",
    "\n",
    "When you finish entering your student, group, and constraint data in Google Sheets, go to `File > Download > Microsoft Excel (.xlsx)`. Move the downloaded data file from your `Downloads` directory to the `Desktop > student-groups-optimization-master > data` directory.\n",
    "\n",
    "You are now ready to optimize your student groups!\n",
    "\n",
    "### Run the program in Jupyter Notebook\n",
    "\n",
    "Go to the terminal window where you activated your `student-groups` environment and run:\n",
    "\n",
    "```\n",
    "jupyter notebook\n",
    "```\n",
    "\n",
    "A window should open in your web browser with what looks like your folder directory. If the window does not open automatically, copy/paste the URL from the terminal into your favorite web browser.\n",
    "\n",
    "Navigate through the folder structure to the `student-groups-optimization-master` directory on your desktop. Open the `Student Groups Optimization.ipynb` file. Follow the instructions in the notebook and press `Shift + Enter` to run the code in each cell.\n",
    "\n",
    "Congratulations! You are now a student group optimizing machine!\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "\n",
    "### _Alternative without Jupyter Notebook: Run the program in terminal window_\n",
    "\n",
    "Go to the terminal window where you activated your `student-groups` environment and run a command of the form:\n",
    "\n",
    "```\n",
    "python run_program.py filename num_solutions [-v] [-s]\n",
    "```\n",
    "\n",
    "with positional arguments (order matters):\n",
    "- __filename:__ filename for Excel spreadsheet with student, group, and constraint data as `your_filename_here.xlsx`\n",
    "- __num_solutions:__ desired number of optimal solutions\n",
    "\n",
    "and optional arguments:\n",
    "\n",
    "- __-v:__ print solution(s) in terminal window\n",
    "- __-s:__ save student groups to Excel spreadsheet\n",
    "\n",
    "\n",
    "_Examples:_\n",
    "\n",
    "- Run program using student, group, and constraint data in `data_template.xlsx`. Output 3 optimal student groupings. Print student groupings to terminal window and save solutions to Excel spreadsheet.\n",
    "\n",
    "<img src=\"images/run_program_1.png\" title=\"Run Program - Example 1\">\n",
    "\n",
    "- Run program using student, group, and constraint data in `data_template.xlsx`. Output 2 optimal student groupings. Save solutions to Excel spreadsheet.\n",
    "\n",
    "<img src=\"images/run_program_2.png\" title=\"Run Program - Example 2\">\n",
    "\n",
    "- Run program using student, group, and constraint data in `data_template.xlsx`. Output 1 optimal student grouping. Print student groupings to terminal window.\n",
    "\n",
    "<img src=\"images/run_program_3.png\" title=\"Run Program - Example 3\">\n",
    "\n",
    "\n",
    "Congratulations! You are now a student group optimizing machine!\n",
    "\n",
    "#### _Optional: Check constraints satisfied_ \n",
    "\n",
    "To double check that the student grouping solution(s) output by the program satisfy your specified constraints, run a command of the form:\n",
    "\n",
    "```\n",
    "python check_constraints.py data_filename groups_filename\n",
    "```\n",
    "\n",
    "with positional arguments (order matters):\n",
    "- __data_filename:__ filename for Excel spreadsheet with student, group, and constraint data as `your_filename_here.xlsx`\n",
    "- __groups_filename:__ filename for Excel spreadsheet with student groups as `your_filename_here.xlsx`\n",
    "\n",
    "_Example:_\n",
    "\n",
    "- Check that the student grouping solution(s) output by the program and saved in `groupings_20191126_111642.xlsx` satisfy the constraints specified in `data_template.xlsx`.\n",
    "\n",
    "<img src=\"images/check_constraints_1.png\" title=\"Check Constraints Example\">\n",
    "\n",
    "\n",
    "#### _Optional: Check uniqueness of multiple solutions_ \n",
    "\n",
    "With multiple solutions, to review the number of students who change groups from one solution to the next, run a command of the form:\n",
    "\n",
    "```\n",
    "python check_uniqueness.py data_filename groups_filename\n",
    "```\n",
    "\n",
    "with positional arguments (order matters):\n",
    "- __data_filename:__ filename for Excel spreadsheet with student, group, and constraint data as `your_filename_here.xlsx`\n",
    "- __groups_filename:__ filename for Excel spreadsheet with student groups as `your_filename_here.xlsx`\n",
    "\n",
    "_Example:_\n",
    "\n",
    "- Review the number of students who change groups from one solution to the next where the `groupings_20191126_111642.xlsx` file holds the solutions to compare and the `data_template.xlsx` file holds the student, group, and constraint data.\n",
    "\n",
    "<img src=\"images/check_uniqueness_1.png\" title=\"Check Uniqueness Example\">\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Cleanup\n",
    "\n",
    "### Student groups optimization notebook\n",
    "\n",
    "When you finish using the `Student Groups Optimization.ipynb` notebook, go to `File > Save and Checkpoint` to save your progress and `File > Close and Halt` to close the notebook.\n",
    "\n",
    "Exit the tab with the Jupyter folder directory in your web browser.\n",
    "\n",
    "Go to the terminal window and press `Control + C` two times to shut down the notebook server.\n",
    "\n",
    "### Student groups virtual environment\n",
    "\n",
    "To deactivate the `student-groups` environment, run:\n",
    "\n",
    "```\n",
    "source deactivate student-groups\n",
    "```\n",
    "\n",
    "If you want to remove the `student-groups` virtual environment from your computer (this is optional), use the command:\n",
    "\n",
    "```\n",
    "conda env remove --name student-groups\n",
    "```\n",
    "\n",
    "When you are finished, exit the terminal with:\n",
    "\n",
    "```\n",
    "exit\n",
    "```\n",
    "\n",
    "and close the terminal window.\n",
    "\n",
    "Cleanup complete!"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
