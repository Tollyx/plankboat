# plankboat
A Discord bot written with [discord.py](https://github.com/Rapptz/discord.py)

## running
Set your API token and change the enabled plugins if you want in `plankboat.py`, and then all you'll have to do is `python plankboat.py` assuming you have installed [discord.py](https://github.com/Rapptz/discord.py) and the dependencies that the plugins are using.

## plugins
Place your plugin in the `plugins` directory and add its name to the plugins array in `plankboat.py`. You'll have to use the other plugins in that directory as examples for now.
Some better way to handle plugins will be implemented sooner or later. The plan is to have plugins be server-specific (maybe even an option for channel-specific?) in the future.
