from django import template

register = template.Library()


@register.filter()
def currency(value):
    return f'Дата создания: {value.strftime("%d-%m-%Y")}'


forbidden_words = [
    'редиска',

]


@register.filter(name='censor_2')
def hide_forbidden(value):
    words = value.split()
    result = []
    for word in words:
        if word in forbidden_words:
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)


@register.filter(name='censor')
def censor(value):

    variants = ['редиска']  # непристойные выражения
    ln = len(variants)
    filtred_message = ''
    string = ''
    pattern = '*'  # чем заменять непристойные выражения
    for i in value:
        string += i
        string2 = string.lower()

        flag = 0
        for j in variants:
            if not string2 in j:
                flag += 1
            if string2 == j:
                filtred_message += string[0] + pattern * len(string[0:-1])
                flag -= 1
                string = ''

        if flag == ln:
            filtred_message += string
            string = ''

    if string2 != '' and string2 not in variants:
        filtred_message += string
    elif string2 != '':
        filtred_message += pattern * len(string)

    return filtred_message







