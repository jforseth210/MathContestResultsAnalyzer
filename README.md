# Math Contest Results Analyzer 
The program analyzes the results of an international math contest held in 2015.
## Installation
- Clone this repository and cd to the project directory
- Create a new virtual environment and activate it
- Run `pip install -r requirements.txt`

## Usage
- Run `python main.py`

The program will attempt to identify typoed institution names and merge them together. 
It will then perform analysis and output the results to `results.txt`

Specifically it outputs: 
- The average number of teams entered per institution
- An ordered list of the institutions that entered the most teams, including the number of teams that they entered (ordered by number of teams)
- A list of all institutions whose team(s) earned 'Outstanding' rankings (ordered by institution name)
- A list of all US teams who received 'Meritorious' ranking or better.
