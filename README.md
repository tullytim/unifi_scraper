# unifi_scraper
Small script to find Unifi cameras that come and go on the unifi website. 
When the script finds a delta, it sends a text to the ```to_num``` number with a list of the available items.

# Usage
python3 unifi.py config.yml

# Example config.yml
```
---
 twilio_sid: "your sid"
 twilio_token: "your token"
 from_num: 'your from number'
 to_num: 'your to number'
 sleep_time_secs: 300
 ```
