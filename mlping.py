import requests
from bs4 import BeautifulSoup
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")

    except Exception as e:
        print(f"Error {e}")
                
    finally:
        server.quit()

def scrape_metadata(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    try:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = soup.find('meta', property='og:title') or soup.find('title')
            title_text = title['content'] if title else 'No Title Found'
            
            description = soup.find('meta', property='og:description') or soup.find('meta', attrs={"name": "description"})
            description_text = description['content'] if description else 'No Description Available'
            
            image = soup.find('meta', property='og:image')
            image_url = image['content'] if image else 'https://via.placeholder.com/150'  
            
            return title_text, description_text, image_url
        
    except Exception as e:
        print(f"Error: {e}")

    else:
        print(f"Failed to retrieve metadata from {url}")
        return None, None, None

def html_template(title, description, image_url, link):
    template = f"""
    <html>
        <body>
            <h1>Here's today's highlighted link:</h1>
            <table style="border: 1px solid #ddd; padding: 10px;">
                <tr>
                    <td>
                        <img src="{image_url}" alt="Image Preview" style="width:150px;height:auto;"/>
                    </td>
                    <td style="padding-left: 10px;">
                        <a href="{link}"><h2>{title}</h2></a>
                        <p>{description}</p>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """
    return template

sender_email = "REDACTED"
password = "***REMOVED***"
receiver_email = 'REDACTED'
subject = "Here's Today's Highlight!"

sites = [
    "https://distill.pub/",
    'https://machinelearningmastery.com/blog/',
]

url = random.choice(sites)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
response = requests.get(url, headers=headers)


if url == 'https://machinelearningmastery.com/blog/':    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    h2_tags = soup.find_all('h2', class_='title entry-title')
    if h2_tags:
        the_atc = random.choice(h2_tags)
        the_atc_link = the_atc.find('a', href=True)
        formatted_link = the_atc_link['href']
    else:
        print("Unable to find Articles. Sorry!, try again")

elif url == 'https://distill.pub/':
        soup = BeautifulSoup(response.content, 'html.parser')

        articles_distill = soup.find_all('div', class_='post-preview')
        if articles_distill:
            the_atc = random.choice(articles_distill)
            the_atc_link = the_atc.find('a', recursive=False)
            the_atc_title = the_atc.find('h2', class_='title')
            formatted_link = (f"https://distill.pub/{the_atc_link['href']}")
        else:
            print("No Articles found, try again!")

title, description, image_url = scrape_metadata(formatted_link)


if title:
    body = html_template(title, description, image_url, formatted_link)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    send_mail(subject, msg)