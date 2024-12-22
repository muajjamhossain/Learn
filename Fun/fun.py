# Import the necessary modules
import json
import requests
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import random
from googletrans import Translator

# Initialize the translator
translator = Translator()

# Function to fetch Salat times
def get_salat_times():
    # Add your location or coordinates here
    api_url = f"https://api.aladhan.com/v1/timingsByCity?city=Dhaka&country=Bangladesh&method=2"
    
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        timings = data['data']['timings']
        
        put_html('<h3>Salat Times for Dhaka</h3>', scope="content")
        for prayer, time in timings.items():
            put_text(f"{prayer}: {time}", scope="content")
    else:
        put_text("Error fetching Salat times. Please try again later.", color='red', scope="content")

# Function to fetch a Bangla joke
def get_bangla_joke():
    # Example Bangla jokes (you can add more jokes to this list)
    bangla_jokes = [
        "টিচার: পরীক্ষায় খারাপ করলি কেন? ছাত্র: স্যার, পরীক্ষার আগে লাইট চলে গিয়েছিল। টিচার: তা হলে বই পড়তে পারলি না? ছাত্র: না স্যার, কিন্তু মোবাইল চার্জ শেষ হয়ে গিয়েছিল!",
        "ডাক্তার: তোমার কী সমস্যা? রোগী: স্যার, আমি ভুলে যাই। ডাক্তার: কবে থেকে? রোগী: এটা তো মনে পড়ছে না!",
        "স্বামী: তুমি সবসময় ভুল কথা বলো। স্ত্রী: আমি কখন ভুল বলি? স্বামী: ঠিক এই মুহূর্তে।",
        "বন্ধু ১: জানিস, কাল আমি সাপ দেখেছি। বন্ধু ২: সত্যি! কোথায়? বন্ধু ১: টিভিতে!",
        "ছাত্র: স্যার, একটা প্রশ্ন? টিচার: হ্যাঁ, বল। ছাত্র: পানির কোনো রং নেই, তা হলে নীল পানি কোথা থেকে আসে?",
        "বউ: তুমি আমাকে গয়না এনে দাওনি কেন? স্বামী: আমি তো চেয়েছিলাম, কিন্তু দোকানদার বলল, 'বউকে হাসি খুশি রাখার জন্য ভালো ব্যবহারই যথেষ্ট।'",
        "ছাত্র: স্যার, আমি কি ডাক্তার হতে পারব? স্যার: হ্যাঁ, হতে পারবে, যদি রোগী ঠিকমতো বাঁচতে না চায়!",
        "শিক্ষক: মহাবিশ্বের সবচেয়ে ছোট জিনিস কী? ছাত্র: আমার হাতের মোবাইলের ব্যালেন্স।",
        "পুলিশ: তুমি এখানে দাঁড়িয়ে কেন? লোক: স্যার, দাঁড়াতে মানা করেছে কেউ?",
        "মা: খাবার খেতে বলছি, তুই খাচ্ছিস না কেন? ছেলে: মা, খাবার তো ফ্রি না। মা: কেন? ছেলে: আগে টাকা দাও, তারপর খাব।"
    ]
    
    joke = random.choice(bangla_jokes)
    put_html('<h3>Bangla Joke</h3>', scope="content")
    style(put_text(joke, scope="content"), 'color:green; font-size: 24px')

# Fun Fact Generator with Bangla Translation
def get_fun_fact():
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(url)
    data = json.loads(response.text)
    useless_fact = data['text']
    
    # Translate the fact into Bangla
    translated_fact = translator.translate(useless_fact, src='en', dest='bn').text
    
    put_html('<h3>Fun Fact</h3>', scope="content")
    style(put_text(translated_fact, scope="content"), 'color:blue; font-size: 24px')

# Main menu
def main_menu():
    # Clear previous content, but keep buttons intact
    clear(scope="content")
    
    # Main buttons
    put_buttons([
        dict(label='Get Fun Fact', value='fun_fact', color='success'),
        dict(label='Get Salat Times', value='salat', color='info'),
        dict(label='Get Bangla Joke', value='bangla_joke', color='warning')
    ], onclick=[
        lambda: (clear(scope="content"), get_fun_fact()),
        lambda: (clear(scope="content"), get_salat_times()),
        lambda: (clear(scope="content"), get_bangla_joke())
    ])

# Driver Function
if __name__ == '__main__':
    # Create a separate scope for dynamic content
    put_html('<h2>Welcome to the Fun App!</h2>')
    main_menu()
    put_scope("content")  # This scope will hold dynamic content
    hold()
