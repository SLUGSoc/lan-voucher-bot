# The Voucher Slinger (WIP)

A Discord bot made to hand out LAN vouchers to attendees, and note down relevant info in the process.

## Data Formats
- Attendee Data: CSV file exported from the SU dashbaord with headers `[ID,Name,discord,voucher]`.
Will be populated with voucher assignment data.
- Vouchers: CSV file exported from OPNsense with headers `[username,password,vouchergroup,expirytime,validity]`.
Opened as read-only and usernames & passwords are concatenated on the fly.

## Usage
- Make a token.yaml file with the format: `token: "[token here]"`
- Supply the CSVs for attendees and vouchers, changing the names of either the files or what the program is looking for in the respective variables
- Run the program and hope nothing blows up

## Known issues
- None, atm!
