# Warwick District Council Waste Collection Notification

This python script is used to monitor your property's waste collections dates and notify you what collection is happening.
By default this script will notify you the day before, so you may get yourself ready the night before.

# Install
   1. Copy `notify.py` to place of your choosing
   1. Find out your [property uprn](https://estates7.warwickdc.gov.uk/PropertyPortal/Property/Search)
   1. Create your [Telegram bot](https://core.telegram.org/bots#how-do-i-create-a-bot)
   1. Edit `uprn`, `token`, `chat_id` in `notify.py` with your found uprn number, telegram token and chat id
   1. Run the script daily, something like 5PM via cron `0 17 * * *` this will then alert you the day before any waste collections, even if your collection day moves.

# User Variables 
   * `uprn` property uprn
   * `token` telegram bot token
   * `chat_id` telegram chat id
   * `notify_days` day number to notify before collection to send notification. 1 being the day before, 0 will notify on day of collection, Default value 1

# Example message received
```
Waste Collection (10/01/2023)
 - Food Waste
 - Garden Waste
 - Recycling
```