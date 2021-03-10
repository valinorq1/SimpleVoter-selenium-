import random
import string

limit = input('Сколько нужно сгенерировать?:')
limit = int(limit)
def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


emails_list = []
for i in range(limit):
    q = get_random_string(8)
    emails_list.append(q)


random_client = ['@gmail.com', '@hotmail.com', '@yandex.ru', '@mail.ru']

f = open('emails.txt', 'w')
for e in emails_list:
    f.write(e+f'{random.choice(random_client)}\n')

f.close()


logins_list = []
for i in range(limit):
    q = get_random_string(8)
    logins_list.append(q)


f = open('logins.txt', 'w')
for e in logins_list:
    f.write(e+f'{e}\n')

f.close()


password_list = []
for i in range(limit):
    q = get_random_string(8)
    password_list.append(q)


f = open('passwords.txt', 'w')
for e in password_list:
    f.write(e+f'{e}\n')

f.close()
