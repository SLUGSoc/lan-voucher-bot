# Voucher Slinger (WIP)

A Discord bot made to hand out LAN vouchers to attendees, and note down relevant info in the process.

## Data Formats
- Attendee Data: CSV file with the columns "ID,Name", corresponding to a student ID and student name respectively
- Vouchers: CSV file with one column for vouchers
- Voucher Assignments: CSV file with the columns "ID,Name,Voucher" corresponding to a student ID, Discord username and the voucher assigned to that person

## Usage
- Make a token.yaml file with the format: `token: "[token here]"`
- Supply the CSVs for attendees and vouchers, changing the names of either the files or what the program is looking for in the respective variables
- Run the program and hope nothing blows up

## Known issues
- If the bot is restarted:
    - The same voucher codes will be handed out again because the voucher file is not modified directly
    - Someone who has already been given a voucher code can receive another
- The bot stops responding if there are no more vouchers left to hand out
