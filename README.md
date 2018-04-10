# raspi-lcd-crypto-watch
Runs 16x2 LCD display with Raspberry Pi to show cryptocurrency prices. Controlled through a telegram bot.


## Requirements
* Python 2.7+
* `python-telegram-bot`, `gpiozero`, `requests` modules

## Installation & Usage
* Install required modules
* Clone repository
* Fill `config-example.json` with your own details and rename it to `config.json`
* Setup `lcd_controller.py` with your GPIO pin numbers
* Run `python main.py`
