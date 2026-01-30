import re,random
from colorama import Fore,init
init(autoreset=True)
destinations = {
    "beaches": ["Bali", "Maldives", "Phuket"],
    "mountains": ["Swiss Alps", "Rocky Mountains", "Himalayas"],
    "cities": ["Tokyo", "Paris", "New York"]
}
jokes = ["Why don't programmers like nature?Too many bugs.",
"Why did the computer go to the doctor?Cause he had a virus.",
"Why do travellers always feel warm?Cause of all their warm spots."]
def normalize_input(text):
    return re.sub(r"\s+", " ", text.strip().lower())
def recommend():
    print(Fore.CYAN + "clanker used for traveling or smth: Beaches, mountains, or cities?")
    preference = input(Fore.YELLOW + "You: ")
    preference = normalize_input(preference)
    if preference in destinations:
        suggestion = random.choice(destinations[preference])
        print(Fore.GREEN + f"clanker used for traveling or smth: How about {suggestion}?")
        print(Fore.CYAN + "clanker used for traveling or smth: Do you like it? (yes/no)")
        answer = input(Fore.YELLOW + "You: ").lower()
        if answer == "yes":
            print(Fore.GREEN + f"clanker used for traveling or smth: Awesome! Enjoy {suggestion}!")
        elif answer == "no":
            print(Fore.RED + "Tclanker used for traveling or smth: Let's try another.")
            recommend()  # Recursive call if the user rejects the suggestion
        else:
            print(Fore.RED + "clanker used for traveling or smth: I'll suggest again.")
            recommend()  # Recursive call on unrecognized answer
    else:
        print(Fore.RED + "clanker used for traveling or smth: Sorry, I don't have that type of destination.")
        recommend()
def packing_tips():
    print(Fore.CYAN + "clanker used for traveling or smth: Where to?")
    location = normalize_input(input(Fore.YELLOW + "You: "))
    print(Fore.CYAN + "clanker used for traveling or smth: How many days?")
    days = input(Fore.YELLOW + "You: ")
    print(Fore.GREEN + f"clanker used for traveling or smth: Packing tips for {days} days in {location}:")
    print(Fore.GREEN + "- Pack versatile clothes.")
    print(Fore.GREEN + "- Bring chargers/adapters.")
    print(Fore.GREEN + "- Check the weather forecast.")
def tell_joke():
    print(Fore.YELLOW + f"clanker used for traveling or smth: {random.choice(jokes)}")
def show_help():
    print(Fore.MAGENTA + "\nI can:")
    print(Fore.GREEN + "- Suggest travel spots (say 'recommendation')")
    print(Fore.GREEN + "- Offer packing tips (say 'packing')")
    print(Fore.GREEN + "- Tell a joke (say 'joke')")
    print(Fore.CYAN + "Type 'exit' or 'bye' to end.\n")
def chat():
    print(Fore.CYAN + "Hello! I'm a clanker used for travelling or smth idk🥀.")
    name = input(Fore.YELLOW + "Whats your name? ")
    print(Fore.GREEN + f"Nice to meet you, {name}")
    show_help()
    while True:
        user_input = input(Fore.YELLOW + f"{name}: ")
        user_input = normalize_input(user_input)
        if "recommend" in user_input or "suggest" in user_input:
            recommend()
        elif "pack" in user_input or "packing" in user_input:
            packing_tips()
        elif "joke" in user_input or "funny" in user_input:
            tell_joke()
        elif "help" in user_input:
            show_help()
        elif "exit" in user_input or "bye" in user_input:
            print(Fore.CYAN + "clanker used for traveling or smth: okay goodbye!")
            break
        else:
            print(Fore.RED + "clanker used for traveling or smth: Could you rephrase?")
#start running clanker
if __name__ == "__main__":
    chat()