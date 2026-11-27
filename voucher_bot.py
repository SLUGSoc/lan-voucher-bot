import discord
from discord.ext import commands
import yaml
import csv

description = "lan voucher thingymabob"

# read token
token_path = "token.yaml"
with open(token_path, "r") as token_file:
    token = yaml.safe_load(token_file).get("token")

# read attendee list
attendee_path = "data/lan_attendees.csv"
attendees = []
with open(attendee_path, 'r') as csv_file:
    id_reader = csv.reader(csv_file)
    fields = next(id_reader)
    for row in id_reader:
        attendees.append(row)
print(attendees) # debugging

ids = [] # copy ids to their own list for easier validation
for i in range(len(attendees)):
    ids.append(attendees[i][0])
print(ids) # debugging

voucher_enjoyers = [] # discord names of people who have already had a voucher assigned to them

vouchers = [] # list of vouchers to give out
with open("data/vouchers.csv", 'r') as csv_file:
    voucher_reader = csv.reader(csv_file)

    fields = next(voucher_reader)
    for row in voucher_reader:
        vouchers.append(row)

# initialise file that will contain IDs, names and voucher codes to preserve the original
voucher_fields = ['id', 'name', 'voucher']
with open("data/voucher_assignments.csv", 'a+', newline='') as csv_file:
    csv_file.seek(0) # https://stackoverflow.com/a/11895272 check if the file is empty before adding the header
    first_char = csv_file.read(1)
    if not first_char:
        label_writer = csv.writer(csv_file)
        label_writer.writerow(voucher_fields)

intents = discord.Intents.default()
intents.guild_messages = False
intents.message_content = True

client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="$", description=description, intents=intents)

@bot.event
async def on_ready():
    assert bot.user is not None
    print(f"We have logged in as {bot.user}")

@bot.command(description="says hi")
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author}!")

@bot.command(description="Hand out a voucher")
async def voucher(ctx, id):
    if id in ids and ctx.author not in voucher_enjoyers:
        # make a row containing id, discord name and voucher code (duh)
        voucher_code = vouchers.pop()[0] # take a voucher from the list
        about_to_assign = [id, ctx.author, voucher_code]
        with open('data/voucher_assignments.csv', 'a', newline='') as file:
            assignment_writer = csv.writer(file)
            assignment_writer.writerow(about_to_assign)
        voucher_enjoyers.append(ctx.author)
        await ctx.send(f"test successful: {voucher_code} assigned to {ctx.author}, ID: {id}.")
    elif id not in ids:
        await ctx.send("Student ID provided is not valid.")
    else:
        await ctx.send("You already have a voucher code.")

@voucher.error # https://stackoverflow.com/questions/67874947/how-to-check-if-required-argument-is-missing-in-discord-py
async def bad_id(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide a student ID.")

bot.run(token)