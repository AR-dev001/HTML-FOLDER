print("Hello, I am a chatbot, whats ur name.")
name = input()
print("Nice to meet you, ",name)
print("How are you feeling today?")
mood = input().lower()
if mood == "good":
    print("That's great!")
elif mood == "bad":
    print("Well i hope tommorow is better")
else:
    print("i dont have any prompts for stuff other than good or bad so i dont know what that feeling is")
print("it was nice talking with you,i shall go now,goodbye")