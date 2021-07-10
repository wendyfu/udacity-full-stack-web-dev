# Build an Item Catalog Project
Part of [Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).

### Prerequisites
1. Prepare the virtual machine, use following [guide from Udacity](https://github.com/udacity/fullstack-nanodegree-vm). The virtual machine already contains all the software needed for this project.
    1. Start your virtual machine: from your terminal, inside the `vagrant` subdirectory, run the command `vagrant up`.
    1. Login into the virtual machine with `vagrant ssh`. 
2. Prepare the data:
    1. On your host machine: download the project files and put these files into the `vagrant/catalog` directory, which is shared with your virtual machine.
    2. Populate the data on your virtual machine: `cd` into the `vagrant/catalog` directory and use the command `python3 database_setup.py` then `python3 items.py`.
3. Make sure the `catalog.db` already present. Run the project with `python3 application.py`. Open `localhost:8000` in browser.

### Navigation
1. Homepage: [http://localhost:8000](http://localhost:8000)
![image](https://user-images.githubusercontent.com/13144571/124612843-dd0fd980-de9c-11eb-8c0e-f5ad403a22c9.png)
    - Displays all current categories with the latest added items.
    
2. Create New Item: [http://localhost:8000/catalog/new](http://localhost:8000/catalog/new)
![image](https://user-images.githubusercontent.com/13144571/124612909-e8fb9b80-de9c-11eb-88e3-73bbd01cad4b.png)
![image](https://user-images.githubusercontent.com/13144571/124611663-d7fe5a80-de9b-11eb-9aad-d457e133e36b.png)
    - Must be logged in. Authentication is using Google sign in.

3. View Category Details: [http://localhost:8000/catalog/<category_name>/items](http://localhost:8000/catalog/<category_name>/items)
![image](https://user-images.githubusercontent.com/13144571/124612508-94582080-de9c-11eb-9e9f-ee1d1e63b91c.png)
    - Selecting a specific category shows you all the items available for that category.

4. View Item Details: [http://localhost:8000/catalog/<category_name>/<item_title>](http://localhost:8000/catalog/<category_name>/<item_title>) 
![image](https://user-images.githubusercontent.com/13144571/124612209-58bd5680-de9c-11eb-9488-eeca3f3b6c6d.png)
    - Selecting a specific item shows you specific information about that item.
    - After logging in, a user has the ability to add, update, or delete item information. Users should be able to modify only those items that they themselves have created.

5. Edit Item: [http://localhost:8000/catalog/<category_name>/edit/](http://localhost:8000/catalog/<category_name>/edit/)
![image](https://user-images.githubusercontent.com/13144571/124613237-38da6280-de9d-11eb-8485-e485a3765929.png)

6. Delete Item: [http://localhost:8000/catalog/<category_name>/delete/](http://localhost:8000/catalog/<category_name>/delete/)
![image](https://user-images.githubusercontent.com/13144571/124613275-41cb3400-de9d-11eb-8858-eb33800ad487.png)

7. JSON Endpoint: [http://localhost:8000/catalog.json](http://localhost:8000/catalog.json)
```
{
  "Category": [
    {
      "Item": [
        {
          "cat_id": 1, 
          "description": "The shoes", 
          "id": 1, 
          "title": "Soccer Cleats"
        }, 
        {
          "cat_id": 1, 
          "description": "The shirt", 
          "id": 2, 
          "title": "Jersey"
        }
      ], 
      "id": 1, 
      "name": "Soccer"
    }, 
    {
      "id": 2, 
      "name": "Basketball"
    }, 
    {
      "Item": [
        {
          "cat_id": 3, 
          "description": "The bat", 
          "id": 3, 
          "title": "Bat"
        }
      ], 
      "id": 3, 
      "name": "Baseball"
    }, 
    {
      "Item": [
        {
          "cat_id": 4, 
          "description": "it will chase your frisbee", 
          "id": 5, 
          "title": "Doggo"
        }
      ], 
      "id": 4, 
      "name": "Frisbee"
    }, 
    {
      "Item": [
        {
          "cat_id": 5, 
          "description": "Best for any terrain and conditions", 
          "id": 4, 
          "title": "Snowboard"
        }
      ], 
      "id": 5, 
      "name": "Snowboarding"
    }
  ]
}
```
