# Build an Item Catalog Project
Part of [Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

### Prerequisites
1. Prepare the virtual machine, use following [guide from Udacity](https://github.com/udacity/fullstack-nanodegree-vm). The virtual machine already contains all the software needed for this project.
    1. Start your virtual machine: from your terminal, inside the `vagrant` subdirectory, run the command `vagrant up`.
    1. Login into the virtual machine with `vagrant ssh`. 
2. Prepare the data:
    1. On your host machine: download the project files and put these files into the `vagrant/catalog` directory, which is shared with your virtual machine.
    2. Populate the data on your virtual machine: `cd` into the `vagrant/catalog` directory and use the command `python database_setup.py` then `python items.py`.
3. Run the project with `python application.py`. 

### Navigation
1. Open `localhost:8000` in browser.

### Check Codestyle
Run `pycodestyle <filename>.py`