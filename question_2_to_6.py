import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def login(session, login_url, username, password):
    """
    Se connecte au site en utilisant une session.
    """
    # Obtenir la page de login pour extraire le CSRF token
    response = session.get(login_url)
    if response.status_code != 200:
        print(f"Échec de l'accès à la page de login, code d'état : {response.status_code}")
        return False
    
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    
    # Préparer les données de connexion
    payload = {
        'csrf_token': csrf_token,
        'username': username,
        'password': password
    }
    
    # Envoyer la requête de login
    response = session.post(login_url, data=payload)
    if response.status_code == 200 and "Logout" in response.text:
        print("Connexion réussie!")
        return True
    else:
        print("Échec de la connexion. Vérifiez vos identifiants.")
        return False

def get_total_pages(session, base_url):
    """
    Détermine le nombre total de pages de citations.
    """
    response = session.get(base_url)
    if response.status_code != 200:
        print(f"Échec de l'accès à la page, code d'état : {response.status_code}")
        return 0
    
    soup = BeautifulSoup(response.text, 'html.parser')
    pagination = soup.find('ul', class_='pager')
    if pagination:
        next_button = pagination.find('li', class_='next')
        if next_button:
            # Supposons qu'il y a un bouton "next", donc au moins 2 pages
            # Pour déterminer le nombre exact, on peut parcourir jusqu'à ce qu'il n'y ait plus de "next"
            page_count = 1
            while next_button:
                page_count += 1
                next_href = next_button.find('a')['href']
                next_url = urljoin(base_url, next_href)
                response = session.get(next_url)
                if response.status_code != 200:
                    break
                soup = BeautifulSoup(response.text, 'html.parser')
                pagination = soup.find('ul', class_='pager')
                next_button = pagination.find('li', class_='next') if pagination else None
            return page_count
        else:
            # Une seule page
            return 1
    else:
        # Pas de pagination, une seule page
        return 1

def extract_quotes(session, base_url):
    """
    Extrait toutes les citations du site.
    """
    all_quotes = []
    current_url = base_url
    page_number = 1
    
    while current_url:
        print(f"Extraction des citations de la page {page_number}: {current_url}")
        response = session.get(current_url)
        if response.status_code != 200:
            print(f"Échec de l'accès à la page {current_url}, code d'état : {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')
        
        for quote in quotes:
            text = quote.find('span', class_='text').get_text(strip=True)
            author = quote.find('small', class_='author').get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.find_all('a', class_='tag')]
            all_quotes.append({'text': text, 'author': author, 'tags': tags})
        
        # Vérifier s'il y a une page suivante
        next_button = soup.find('li', class_='next')
        if next_button:
            next_href = next_button.find('a')['href']
            current_url = urljoin(current_url, next_href)
            page_number += 1
            time.sleep(1)  # Pause pour ne pas surcharger le serveur
        else:
            current_url = None  # Plus de pages
    
    return all_quotes

def answer_questions(quotes):
    """
    Répond aux questions basées sur les citations extraites.
    """
    total_quotes = len(quotes)
    print(f"\nNombre total de citations : {total_quotes}")
    
    if total_quotes >= 1:
        first_quote = quotes[0]['text']
        print(f"Première citation : {first_quote}")
    else:
        print("Aucune citation trouvée.")
    
    if total_quotes >= 5:
        fifth_quote = quotes[4]['text']
        print(f"Cinquième citation : {fifth_quote}")
    else:
        print("Moins de cinq citations trouvées.")
    
    # Calculer le tag le plus répétitif
    tag_counts = {}
    for quote in quotes:
        for tag in quote['tags']:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    if tag_counts:
        most_repetitive_tag = max(tag_counts, key=tag_counts.get)
        print(f"Tag le plus répétitif : {most_repetitive_tag} (apparaît {tag_counts[most_repetitive_tag]} fois)")
    else:
        print("Aucun tag trouvé.")

def main():
    base_url = "https://quotes.toscrape.com/"
    login_url = urljoin(base_url, "login")
    
    # Informations de connexion 
    username = "username"  
    password = "password" 
    
    # Créer une session
    session = requests.Session()
    
    # Se connecter
    if login(session, login_url, username, password):
        # Déterminer le nombre total de pages
        total_pages = get_total_pages(session, base_url)
        print(f"Nombre total de pages : {total_pages}")
        
        # Extraire toutes les citations
        quotes = extract_quotes(session, base_url)
        
        # Répondre aux questions
        answer_questions(quotes)

if __name__ == "__main__":
    main()
