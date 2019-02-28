# self.ua

`ua` is the name of your bot, EZWS will look for this name in each sites `robots.txt` file

It is required, your user-agent should be unique, although nothing stops you from using another bot name

Note:

The user-agent is only used when `self.check` is enabled

`ua` is still required to construct an EZWS object, but will not be used if `self.check` is disabled