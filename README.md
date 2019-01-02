# Rotmg-Bot
> A trading bot made for Realm of the Mad God

![](https://img.shields.io/badge/python-3.6-blue.svg)
![](https://img.shields.io/pypi/status/Django.svg)

This bot only trades potions, and it makes sure to trade them for a profit.
Example: "Sell 1 life for 6 def, and buy 1 life for 5 def."

![](header.png)

## Installation

Packages:

```
pyautogui, mss, cv2, numpy, imutils, keyboard, pillow, 
```


## Usage rules

1. When the bot starts you have 5 seconds to click on the rotmg website screen.
2. Stop the bot by pressing Q
3. Make sure that the website is not in fullscreen mode "F11" or in a smaller mode, the zoom has to be 100%.
4. Dont click anywhere else when the program is still running, make sure to turn it off first by pressing Q.
5. Make sure your username is in the username.txt folder.
6. Make sure your screen is not rotated or rotating, it needs to be in the default angle.
7. Position the character in the middle of the map, or so that he doesnt go to the water while trying to go up or down.
8. Your nexus button should be set to R

## Running the program

To run the program do this. To quit the program you need to hold Q.
```
python trader.py
```

## Release History

* 0.2.1
    * Bugs fixed
* 0.2.0
    * ADD: Added crash function to handle server crashes `crash()`
* 0.1.1
    * Add: New rules for trading
* 0.1.0
    * The first proper release
* 0.0.1
    * Work in progress

## Meta

Johannes Leppäkorpi – [@johnlep3](https://twitter.com/johnlep3) – johkmr@gmail.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/Johk3](https://github.com/Johk3)

## Contributing

1. Fork it (<https://github.com/Johk3/Rotmg-Bot/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki
