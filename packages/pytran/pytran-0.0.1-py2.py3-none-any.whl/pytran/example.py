from pytrans import translate

# Automatic identification of the text in the language, and translate.
print(translate("How are you?", to_lang="ar"))  

# Translate with from and to.
print(translate("Bonjour", from_lang="fr", to_lang="en"))