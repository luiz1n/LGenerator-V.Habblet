from twocaptcha import TwoCaptcha
from time import sleep
import requests, random, string, re, os

prefix = "luizin"
password = "suasenha123"
contas_registradas = 0

registrar_vezes = 200

def generate_username():
    return f'{prefix}-'+''.join(random.choice(string.ascii_letters) for x in range(random.randint(3, 5)))

def generate_email():
    return ''.join(random.choice(string.ascii_letters.lower()) for y in range(random.randint(6, 9)))+"@gmail.com"

def delete_captchas():
    for captcha in os.listdir('captchas/'):
        os.remove(f'captchas/{captcha}')

solver = TwoCaptcha(open('apikey.txt').read())

with requests.Session() as client:
    print(f'Registrando {registrar_vezes} contas.')
    for x in range(registrar_vezes):

        username = generate_username()
        email = generate_email()

        client.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
        }

        r = client.get("https://habblet.city/captcha", stream=True)
        name_captcha = f'captcha-{random.randint(1, 42343)}.png'
        with open(f"captchas/{name_captcha}", 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

        resultado = solver.normal(f'captchas/{name_captcha}')
        captcha_code = resultado['code']

        body_register = client.get("https://habblet.city/register").text
        try:
            asteroid_token = re.search("<input type=\"hidden\" name=\"_asteroid\" value=\"(.+)\">", body_register).group(1)
        except:
            print(body_register)
        

        form = {
            "bean_avatarName": username,
            "bean_email": email,
            "bean_day": 10,
            "bean_month": 3,
            "bean_year": 1998,
            "bean_password": password,
            "bean_retypedPassword": password,
            "bean_gender": "male",
            "bean_figure": "ch-210-66.lg-270-1338.sh-290-1408.hr-100-39.hd-180-1",
            "bean_captcha": captcha_code,
            "_asteroid": asteroid_token
        }

        if client.post("https://www.habblet.city/account/register", data=form).status_code == 200:
            contas_registradas += 1
            with open('registradas.txt', 'a+') as file:
                file.write(f"{username}:{password}\n")
            print(f'[{contas_registradas}] Conta Registrada! Usuário: {username} - Senha: {password} - Código Captcha: {captcha_code}')
            client.get("https://www.habblet.city/logout")
        sleep(1)
    delete_captchas()