import re
import random


def send_message(message):
	# Get ELIZA's response to the message:
	response = respond(message)
	# Print the bot template including ELIZA's response:
	print("ELIZA: {0}".format(response))


# Should you feel like it, add more rules/responses to this dictionary
rules = {"I want (.*)": ["What would it mean if you got {0}?",
                         "Why do you want {0}?",
                         "What would you do if you got {0}?",
                         "What's stopping you from getting {0}?"],
         "I need (.*)": ["Why do you need {0}?",
                         "Are you sure you need {0}?",
                         "How can I help you to get {0}?"],
         "I can't (.*)": ["How do you know you can't {0}",
                          "Perhaps you could {0} if you tried",
                          "What are you lacking?"],
         "I am (.*)": ["Did you come to me because you are {0}?",
                       "How long have you been {0}?",
                       "How can I help you?"],
         "I think (.*)": ["Do you really think so?",
                          "But you're not sure {0}?"],
         "I'm (.*)": ["How does being {0} make you feel?",
                      "Why do you think {0} happens?"],
         "Are you ([^?]*)?": ["Why does it matter?",
                              "Would you prefer it if I wre not {0}?",
                              "Perhaps according to you."],
         "What (.*)": ["Why do you ask?",
                       "How would me answering that help you?",
                       "What do you think?"],
         "Why don't you ([^?]*)?": ["Do you really think I don't {0}?",
                                     "Perhaps I will eventually {0}",
                                     "Do you want me to {0}?"],
         "Why can't I ([^?]*)?": ["Do you think you will be able to {0}?",
                                  "If you could {0}, what would you do?",
                                  "I don't know, why can't you do {0}?",
                                  "What's stopping you?"],
         "do you remember (.*)": ["Did you think I would forget {0}?",
                                  "Why haven't you been able to forget {0}?",
                                  "What about {0}?",
                                  "Yes ...and?"],
         "do you think (.*)": ["if {0}? Absolutely.",
                               "No way Jose"],
         "if (.*)": ["Do you really think that it's likely that {0}?",
                     "Do you wish that {0}?",
                     "What do you think about {0}?"],
         "How (.*)": ["How do you suppose?",
                      "What do you really want to ask?"],
         "Because (.*)": ["Is that the real reason?",
                          "What other reasons can you think of?",
                          "If {0}, what else must be true?",
                          "Perhaps that's only your point of view."],
         "(.*) sorry (.*)": ["What do you feel when you apologize?",
                             "There are many times when no apology is needed"],
         "Hello(.*)": ["Hi! I'm glad you could drop by today",
                       "Hi there, how are you today?",
                       "Hello, how are you feeling today?"],
         "Hi(.*)": ["Hi! I'm glad you could drop by today",
                    "Hi there, how are you today?",
                    "Hello, how are you feeling today?"],
         "(.*) friend (.*)": ["Tell me more about your friends",
                              "Tell me about a friend of yours"],
         "Yes": ["You seem quite sure",
                 "Ok, but can you still elaborate a bit more?"],
         "No": ["Why not?",
                "Can you tell me why you say no?",
                "Are you sure?"],
         "Is it (.*)": ["Do you think it is {0}?",
                        "Perhaps, what do you think?",
                        "If it were {0}, what would you do?",
                        "It could well be that {0}"],
         "It is (.*)": ["You seem certain",
                        "If it weren't {0}, how would you feel?"],
         "Can you ([^?]*)?": ["What makes you think I can't {0}?",
                              "If I could, then what?",
                              "Why do you ask?"],
         "Can I ([^?]*)?": ["Perhaps you don't want to {0}",
                            "Do you want to be able to {0}?",
                            "If you could {0}, would you?"],
         "You are (.*)": ["Why do you think I am {0}?",
                          "Perhaps you're really talking about yourself?",
                          "Do you like to think that I'm {0}?"],
         "You're (.*)": ["Why do you say I am {0}?",
                         "Why do you think I am {0}?",
                         "I thought we were talking about you"],
         "I don't (.*)": ["Don't you really {0}?",
                          "Why don't you {0}?",
                          "Do you want to {0}?"],
         "I feel (.*)": ["Tell me more",
                         "Do you often feel {0}?",
                         "When do you usually feel {0}?",
                         "When you feel {0}, what do you do?"],
         "I have (.*)": ["Why do you tell me that you've {0}?",
                         "Have you really {0}?",
                         "What will you do next?"],
         "I've (.*)": ["Why did you {0}?",
                       "How do you know you've {0}?"],
         "I would (.*)": ["Could you explain why you would {0}?",
                          "Why would you {0}?",
                          "Who else knows that you would {0}?"],
         "Is there (.*)": ["Would you like there to be {0}?",
                           "It's likely that there is {0}",
                           "Why do you think there is {0}?"],
         "My (.*)": ["Why do you say that your {0}?",
                     "I see, your {0}"],
         "You (.*)": ["Why do you care whether I {0}?",
                      "Why do you say that about me?",
                      "Let's discuss you, not me"],
         "Why (.*)": ["Why do you think {0}?",
                      "Tell me why {0}"],
         "(.*) mother(.*)": ["Tell me more about your mother",
                             "How do you feel about your mother?",
                             "Good family relations are important",
                             "How does this relate to your feelings today?"],
         "(.*) father(.*)": ["Tell me more about your father",
                             "How do you feel about your father?",
                             "Good family relations are important",
                             "How does this relate to your feelings today?"],
         "(.*) child(.*)": ["Did you have close friends as a child?",
                            "What's your favorite childhood memory?"],
         "(.*)?": ["Why do you ask that?",
                   "Perhaps you can answer your own question",
                   "Why don't you tell me?"],
         "(.*)": ["Can you please elaborate?",
                  "I don't fully understand"],
         "QUIT": ["Thank you for talking with me :)",
                  "Good bye friend"]}

# The d_responses dictionary will be our default responses
d_responses = ["Sorry, can you elaborate?",
               "Very interesting.",
               "I see.",
               "Please tell me more."]


def match_rule(rules, message):
	# We have some default message and phrase to return
	response, phrase = "default", None
	# We iterate over the rules dictionary
	for pattern, responses in rules.items():
		# Create a match object with re.search()
		match = re.search(pattern, message)
		if match is not None:
			# Choose a random response
			response = random.choice(responses)
			# If there is a placeholder in the response, we must fill it
			if "{0}" in response:
				# Our phrase will be the parenthesized subgroup
				phrase = match.group(1)
	if response == "default":
		response = random.choice(d_responses)
	# Return both the response and phrase
	return response, phrase


def replace_pronouns(message):
	# We lowercase our message in order to avoid any ambiguity
	# as well as remove the final punctuations
	message = message.lower().strip('.!?')
	# We will replace "i" with "you", "you" with "me", etc.
	if "am" in message:
		return re.sub("am", "are", message)
	if "are" in message:
		return re.sub("are", "am", message)
	if "i " in message:
		return re.sub("i ", "you ", message)
	if ("i'd" or "i would") in message:
		return re.sub("i'd|i would", "you would", message)
	if ("i've" or "i have") in message:
		return re.sub("i've|i have", "you have", message)
	if ("i'll" or "i will" or "i shall") in message:
		return re.sub("i'll|i will|i shall", "you will", message)
	if "me" in message:
		return re.sub("me", "you", message)
	if "my" in message:
		return re.sub("my", "your", message)
	if "was" in message:
		return re.sub("was", "were", message)
	if "yours" in message:
		return re.sub("yours", "mine", message)
	if "your" in message:
		return re.sub("your", "my", message)
	if "you" in message:
		return re.sub("you", "I", message)
	if ("you'll" or "you will") in message:
		return re.sub("you'll|you will", "you", message)
	if ("you've" or "you have") in message:
		return re.sub("you've|you have", "I have", message)
	# We return either the changed message, or the original message
	return message


def respond(message):
	# We call match_rule
	response, phrase = match_rule(rules, message)
	# If there is a placeholder in our response
	if '{0}' in response:
		# Replace the pronouns
		phrase = replace_pronouns(phrase)
		# Insert the phrase in the response
		response = response.format(phrase)
	return response


def converse():
	print('*' * 63)
	name = """      ___                                ___          ___
     /  /\                   ___        /  /\        /  /\\
    /  /:/_                 /  /\      /  /::|      /  /::\\
   /  /:/ /\  ___     ___  /  /:/     /  /:/:|     /  /:/\:\\
  /  /:/ /:/_/__/\   /  /\/__/::\    /  /:/|:|__  /  /:/~/::\\
 /__/:/ /:/ /\  \:\ /  /:/\__\/\:\__/__/:/ |:| /\/__/:/ /:/\:\\
 \  \:\/:/ /:/\  \:\  /:/    \  \:\/\__\/  |:|/:/\  \:\/:/__\/
  \  \::/ /:/  \  \:\/:/      \__\::/   |  |:/:/  \  \::/
   \  \:\/:/    \  \::/       /__/:/    |  |::/    \  \:\\
    \  \::/      \__\/        \__\/     |  |:/      \  \:\\
     \__\/                              |__|/        \__\/    """
	print(name)
	print('*' * 63)
	print("   Talk to the bot in plain English. Enter 'QUIT' when done.")
	print('*' * 63)
	print("Hello there, how are you today?")
	string = ''
	# While the input is not QUIT:
	while string != 'QUIT':
		try:
			string = input('>>> ')
		except EOFError:
			string = 'QUIT'
		send_message(string)


if __name__ == "__main__":
	converse()