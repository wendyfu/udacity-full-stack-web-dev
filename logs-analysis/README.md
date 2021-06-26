# Logs Analysis Project
Part of [Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

### Prerequisites
1. Prepare the virtual machine, use following [guide from Udacity](https://github.com/udacity/fullstack-nanodegree-vm). The virtual machine already contains all the software needed for this project.
    1. Start your virtual machine: from your terminal, inside the `vagrant` subdirectory, run the command `vagrant up`.
    1. Login into the virtual machine with `vagrant ssh`. 
2. Prepare the data:
    1. Download the data file `newsdata.sql`. Put this file into the `vagrant directory`, which is shared with your virtual machine.
    2. Populate the data: `cd` into the `vagrant` directory and use the command `psql -d news -f newsdata.sql`.
    3. Optional step to ensure the database already populated correctly:
        1. Connect to database with `psql news`.
        2. Display tables with `\dt`. There are 3 tables: `articles`, `authors`, `log`.
        3. Exit `psql` with `\q`

### Running the Analysis
Simply run `python logs-analysis.py`. The report will be printed directly to the screen console.
