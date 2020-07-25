# Penger

**Penger** is a Telegram Bot API Library for python. This library is being developed for our own service informer bots.

* [Getting started](#getting-started)
    * [Adding Penger as submodule to your repository (recommended)](#adding-penger-as-submodule-to-your-repository-recommended)
    * [Adding Penger as module file to your project](#adding-penger-as-module-file-to-your-project)

## Getting started
How to use this library in your project? Quite easy.
Now let's look at the currently implemented Penger connectivity options:

* #### Adding Penger as submodule to your repository (recommended)
  > Your bot project must be in a git repository. Penger was designed to be included in a project as a git-submodule.
  > Penger may be available in pip storage in the future.

  In different git GUI clients, connecting submodules can be implemented in different ways. Let's have a look at the old and reliable method: console git client.
  
  ```bash
  $ git submodule add https://github.com/mad-penguins/Penger.git
  $ git commit -m "Add Penger as a submodule"
  ```
  > **Advantage**: you can always easily update *Penger* to the latest version:
  > 
  > ```bash
  > $ git submodule update
  > ```
  
  Next, import the Penger:
  
  ```python3
  from Penger.penger import Penger
  ```
  
  > Note that the file tree in the repository will look like this:
  > - **Your_project_Folder**
  >     - |-  **.git**
  >     - |-  **Penger**
  >        - |-  *.git*
  >        - |-  *.gitignore*
  >        - |-  *LICENSE*
  >        - |-  *penger.py*
  >        - |-  *README.md*
  >     - |-  *.gitignore*
  >     - |-  *.gitmodules*
  >     - |-  *your_bot_file.py*
  >
  > Note: files which name begins with a dot can be hidden by `ls` command or your file manager.


* #### Adding Penger as module file to your project
  Just download the file `penger.py` from the master branch and paste it into your project.
  
  Next, import the Penger:
  
  ```python3
  from penger import Penger
  ```
  
  > **Advantage**: you don't need to create a repository for your project.
  >
  > **Disadvantage**: to update *Penger*, you will have to download the file again and replace it in the project.
  
  > Note that the file tree in the repository will look like this:
  > - **Your_project_Folder**
  >     - |-  *penger.py*
  >     - |-  *your_bot_file.py*
  >
  > Note: files which name begins with a dot can be hidden by `ls` command or your file manager.
  
**You can check that everything is connected correctly using `test()` method:**

```python3
Penger().test()
```
***`test()` should return `True`.***
  
## Create your first bot
```python3
from Penger.penger import Penger
bot = Penger("BOT_TOKEN")
```
*Under construction...*
