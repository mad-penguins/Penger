# Penger

**Penger** is a Telegram Bot API Library for python with a flexible command access control system. This library is being developed for service informer bots.

* [Getting started](#getting-started)
    * [Adding Penger as submodule to your repository (recommended)](#adding-penger-as-submodule-to-your-repository-recommended)
    * [Adding Penger as module file to your project](#adding-penger-as-module-file-to-your-project)
* [Create your first bot](#create-your-first-bot) TODO

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
  
## Create your first bot (echo bot)
Now you write a simple echo bot:

> Warning: Here and further, Penger will be imported as if Penger were a git repository submodule.
>
> ```python3
> from Penger.penger import Penger
> ```

```python3
from Penger.penger import Penger


bot = Penger("BOT_API_TOKEN")


def echo(data):
    bot.sendMessageToChat(data, data['text'])


bot.emptyAccordance = echo


while True:
    bot.updateAndRespond()

```

> Warning: Instead of the "BOT_API_TOKEN" string, you need to write your bot's token (in double quotes).
> [How to get a token?](https://core.telegram.org/bots#6-botfather)

## Creating a Accordance
In the echo bot example, you only used an empty accordance. However, you may to implement command support.

Let's write a bot that will report the current date when calling the ```/date``` command:

```python3
from Penger.penger import Penger
import datetime


bot = Penger("BOT_API_TOKEN")


def date(data):
    d = datetime.date.today()
    bot.sendMessageToChat(data, str(d))


bot.accordance = {'/date': date}


while True:
    bot.updateAndRespond()

```

Now, if you want to know the current date, just write to the bot ```/date```. *Naturally, the script must be run.*

But if you write something else (for example, ```/start```), the bot will not respond.

It would be convenient if the bot responded to commands it doesn't understand with the string
```I don't know this command :-(```.

Let's do this:

```python3
from Penger.penger import Penger
import datetime


bot = Penger("BOT_API_TOKEN")


def date(data):
    d = datetime.date.today()
    bot.sendMessageToChat(data, str(d))


def empty(data):
    bot.sendMessageToChat(data, "I don't know this command :-(")


bot.accordance = {'/date': date}
bot.emptyAccordance = empty


while True:
    bot.updateAndRespond()

```

In this example, you used an empty accordance.

An empty accordance is always called if no accordance in the ```Penger.accordance``` variable has passed verification.

Let's finish this date-bot:

```python3
from Penger.penger import Penger
import datetime


bot = Penger("BOT_API_TOKEN")


def start(data):
    hello = "Hello! I am date-bot. Write me /date to find out the current date."
    bot.sendMessageToChat(data, hello)

def date(data):
    d = datetime.date.today()
    bot.sendMessageToChat(data, str(d))


def empty(data):
    bot.sendMessageToChat(data, "I don't know this command :-(")


bot.accordance = {'/start': start, '/date': date}
bot.emptyAccordance = empty


while True:
    bot.updateAndRespond()

```


*Under construction...*
