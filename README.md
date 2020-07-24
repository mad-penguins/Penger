# Penger
**Penger** is Telegram Bot API Library for python. This library is being developed for use in informer bots.

## Getting started
How to connect this library to your code? Very simply.
> But there is one condition: your bot project must be in the git repository. The fact is that Penger was designed to participate in the project as a git-submodule.
> There may be new options for connecting Penger to your project in the future.

Now let's look at the currently implemented Penger connectivity options:

* #### Adding Penger as submodule to your repository (recommended)
  In different git GUI clients, connecting submodules can be implemented in different ways. We will look at the old and reliable method: console git.
  
  ```bash
  $ git submodule add https://github.com/mad-penguins/Penger.git
  $ git add -A
  $ git commit -m "Add Penger as submodule"
  ```
  > **Advantage**: you can always easily update *Penger* to the latest version:
  > 
  > ```bash
  > $ git submodule update
  > ```
  
  Next you need to enable Penger in the code of the future bot:
  
  ```python3
  from Penger.penger import Penger
  ```
  
  > Note that the file tree in the repository will look like this:
  > - **Your_project_Folder**
  >     - |-  **.git**
  >     - |-  **Penger**
  >        - |-  **.git**
  >        - |-  *.gitignore*
  >        - |-  *LICENSE*
  >        - |-  *penger.py*
  >        - |-  *README.md*
  >     - |-  *.gitignore*
  >     - |-  *.gitmodules*
  >     - |-  *your_bot_file.py*
  >
  > Note: files with a dot at the beginning of the name can be hidden when viewing.


* #### Adding Penger as module file to your project
  You will have to download file `penger.py` from the master branch and paste it into your project.
  
  Next you need to enable Penger in the code of the future bot:
  
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
  > Note: files with a dot at the beginning of the name can be hidden when viewing.
  
**You can check that everything is connected correctly using `test()` method:**

```python3
Penger().test()
```
***`test()` should return `True`.***
  
## Writing first bot
```python3
from Penger.penger import Penger
bot = Penger("BOT_TOKEN")
```
*Under construction...*
