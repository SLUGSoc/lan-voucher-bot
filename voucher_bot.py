import discord
from discord.ext import commands
import yaml
import csv
import os

DESCRIPTION = "lan voucher thingymabob"

# read token
TOKEN_PATH = "token.yaml"
with open(TOKEN_PATH, "r") as token_file:
    token = yaml.safe_load(token_file).get("token")

ATTENDEE_PATH = "data/lan_attendees.csv"    # ID,Name,discord,voucher
VOUCHER_PATH = "data/vouchers.csv"          # username,password,vouchergroup,expirytime,validity
REQUIRED_FIELDS = ["ID", "Name", "discord", "voucher"]

def clean(value):
    return (value or "").strip()


# read attendee list
with open(ATTENDEE_PATH, "r", newline="", encoding="utf-8-sig") as csv_file:
    reader = csv.DictReader(csv_file)
    attendee_fields = list(reader.fieldnames or [])
    attendees = []
    for row in reader:
        row = {k: clean(v) for k, v in row.items() if k is not None}
        if row.get("ID"):
            attendees.append(row)

# Add the discord and voucher columns if not present
for field in REQUIRED_FIELDS:
    if field not in attendee_fields:
        attendee_fields.append(field)
for row in attendees:
    for field in attendee_fields:
        row.setdefault(field, "")

# Type hinted because grr I hate yellow squiggles
attendees_by_id: dict[str, dict[str, str]] = {row["ID"]: row for row in attendees}

def save_attendees():
    """Rewrite the attendee file via a temp file so we don't lose all data in the event of a crash (I'm paranoid)"""
    tmp_path = ATTENDEE_PATH + ".tmp"
    with open(tmp_path, "w", newline="") as attendee_csv:
        writer = csv.DictWriter(attendee_csv, fieldnames=attendee_fields)
        writer.writeheader()
        writer.writerows(attendees)
    os.replace(tmp_path, ATTENDEE_PATH)


# Rebuild state from attendee file to persist across restarts
voucher_enjoyers = {row["discord"] for row in attendees if row["discord"]}
used_codes = {row["voucher"] for row in attendees if row["voucher"]}

# Read OPNsense list, concatenating username and password
available_vouchers = []
with open(VOUCHER_PATH, "r", newline="", encoding="utf-8-sig") as csv_file:
    for row in csv.DictReader(csv_file):
        code = clean(row.get("username")) + clean(row.get("password"))
        if code and code not in used_codes:
            available_vouchers.append(code)

print(f"{len(attendees)} attendees, {len(voucher_enjoyers)} vouchers already assigned, "
      f"{len(available_vouchers)} remaining")

intents = discord.Intents.default()
setattr(intents, "guild_messages", False)
setattr(intents, "message_content", True)

bot = commands.Bot(command_prefix="$", description=DESCRIPTION, intents=intents)

@bot.event
async def on_ready():
    assert bot.user is not None
    print(f"We have logged in as {bot.user}")


@bot.command(description="says hi")
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author}!")


@bot.command(description="Hand out a voucher")
async def voucher(ctx, student_id):
    discord_name = str(ctx.author.name)
    attendee = attendees_by_id.get(student_id)

    if attendee is None:
        await ctx.send("Student ID provided is not valid.")
    elif attendee["voucher"]:
        if attendee["discord"] == discord_name:
            await ctx.send("You already have a voucher code.")
        else:
            await ctx.send("That student ID has already been used to claim a voucher.")
    elif discord_name in voucher_enjoyers:
        await ctx.send("You already have a voucher code.")
    elif not available_vouchers:
        await ctx.send("Sorry, there are no vouchers left. Please contact a tech or member of committee.")
    else:
        voucher_code = available_vouchers.pop(0)
        attendee["discord"] = discord_name
        attendee["voucher"] = voucher_code
        save_attendees()

        voucher_enjoyers.add(discord_name)
        used_codes.add(voucher_code)
        await ctx.send(f"Voucher Code: {voucher_code} assigned to User: {ctx.author}, Registration Number: {student_id}.")


@voucher.error
async def bad_id(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide a student ID.")
    else:
        raise error


bot.run(token)