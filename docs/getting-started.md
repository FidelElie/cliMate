<link rel="stylesheet" href="assets/styles/styles.css">

# Getting Started

## Hello World With Some More Flavour
Firstly lets start by making a simple variation of the famous "Hello World". To do this we start by making a python file. Name it whatever you like and then run the command:

```
clm new-app
```
This will create a new cli.json file in your root directory. This is the heart of your new command line application and has its own syntaxes and structures for defining your commands. The anatomy of this file will be discussed throughout the tutorial series, but for now lets add our first command. Copy and past the code snippet below into the commands section of your cli.json file.

``` json
"say-hello" : {
    "name": "Say Hello To Someone",
    "description": "Say Hello To Someone By Name",
    "target": {
        "type": "function",
        "function-name": "say_hello"
    },
    "arguments": {
        "name": {
            "name": "Desired Name",
            "description": "Name You Desire",
            "type": "str",
            "default": "World"
        }
    }
}
```
This has now added the say-hello command to your cli.json file. Now we can hook everything up in python. Open your python file and add the snippet below:
``` python
from climate import CliMate

def say_hello(name):
    print("Hello, {}!".format(name))


if __name__ == "__main__":
    climate = CliMate("cli.json")
    climate.parse_args()
```
Your command line application is now ready to go so now you can run the command:
<div class= "os-toggle">
    <button type="button" class="windows-button toggled">Windows</button>
    <button type="button" class="unix-button">Linux/Mac</button>

    python your\file\path.py say-hello

</button>

This command as is will print `Hello, World!` to your terminal but we also defined an extra argument for the name. so you can add any name you wish after the command and it will print it. This is the basics of how to set up your command line application but lets look more into it. Now we can can also check the help function by typing:

<div class= "os-toggle">
    <button type="button" class="windows-button toggled">Windows</button>
    <button type="button" class="unix-button">Linux/Mac</button>

    python your/file/name.py help
</button>

Additionally, we can also access this command by opening the command line applications' Main Menu. This is achieved by inputting no commands or arguments into the cmd.
<div class= "os-toggle">
    <button type="button" class="windows-button toggled">Windows</button>
    <button type="button" class="unix-button">Linux/Mac</button>

    python your/file/name.py
</button>

This is the basics of how to start your own CliMate application but lets look at what we have written so far with closer scrutiny.

## A Closer Look

CliMate revolves around commands. Each of which holds a name, description, target and optionally arguments. Instead of just passing your desired data directly to the file object everything is organised by the commands. The command call is defined by its key in the case of the example above this is *"say-hello"*. The "name" and "description keys are used in for creating the Menu and Help structure and should be brief but concise.

The target key is where the magic happens and deserves it own section entirely to see what it capable of (See [Climate Targets](climate-targets.md)). However, for now its purpose is to tell the application where it should send the arguments too. This can be in a function as in the example above or other first class objects like methods and classes. Above we define the target type as a function and give it the name of the function.

Arguments are defined in a similar matter to the command itself. They have a "name" and "description" for use in Menu and Help structures. A type for defining the command the desired data type of the input and default values if desired (See [CliMate Arguments](climate-arguments.md))

## Summarising

From what we have talked about in this section I will state the show you the basic overall structure of the climate file itself:

``` json
"general": {
    // general application information is defined here more in later sections.
},
"command": {
    // all commands go here
    "command-1": { // this defines how you call command in cmd.
        "name": "Command Name", // Will Appear as title in menu.
        "description": "Command Description", // What the command does
        "target": {
            // target is pointed to here
            "type": "target type"
            // more on targets in later section
        },
        "arguments": {
            // all arguments for command go here
            "argument-1": {
                "name": "Argument Name",
                "description": "Argument Description",
                "type": "Argument Data Type"
                // other parameters if applicable
            }
        }
    }
}
```
All of this will become easier to utilise as you go through the tutorials on offer here. The example above is good at showing the basics of what can be done with but now lets look more into creating commands.

<div class="navigation-buttons">
    <div class="right-button">
        <button class="nav-button right" type="button" onclick="location.href='./climate-targets.md';">Next Section - CliMate Targets</button>
    </div>
</div>
