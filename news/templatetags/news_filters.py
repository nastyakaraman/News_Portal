from django import template


register = template.Library()

CENSORED_WORDS = {
   'редиска': 'р******',
   'instagram': 'I*******m',
}

@register.filter()
#принимает на вход список из строк
def censored(wordstr):
    words=list(wordstr.split())
    words_censored=words.copy()
    for index, word in enumerate(words):
        if word.lower() in CENSORED_WORDS.keys():
            words_censored[index]=CENSORED_WORDS[word.lower()]
    return ' '.join(words_censored)