import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# İzlenecek web sayfası URL'si
url = 'https://www.eldasoft.com/tr/announcement'
# E-posta göndermek için gereken bilgiler
sender_email = 'cardakahmet068@gmail.com'
receiver_email = 'ahmetcarrdak@icloud.com'
password = 'Bahardali5103'

def get_announcements():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    announcements = soup.find_all('div', class_='comp-lrzdsavlinlineContent')
    return announcements

def send_email(subject, body):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP_SSL('smtp.example.com', 465) as server:
        server.login(sender_email, password)
        server.send_message(message)

if __name__ == "__main__":
    last_announcements = set()
    while True:
        announcements = get_announcements()
        new_announcements = set(announcements) - last_announcements
        if new_announcements:
            for announcement in new_announcements:
                title = announcement.find('h2').text
                content = announcement.find('p').text
                send_email(f'Yeni Duyuru: {title}', content)
        last_announcements = set(announcements)
        time.sleep(300)  # 5 dakika bekleme
