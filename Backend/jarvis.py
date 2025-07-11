import re
import requests
from tabulate import tabulate
import random
from datetime import datetime


def main():
    try:
        process_input()
    except KeyboardInterrupt:
        print("Goodbye👋")


headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "PostmanRuntime/7.44.1",
    "Connection": "keep-alive",
}

greetings = [
    "Hi, my name is Jarvis. I am a personal Assistant.\nWhat can I do for you today ?",
    "Hello! I’m Jarvis, your personal assistant.\nHow may I assist you today?",
    "Greetings! Jarvis here.\nWhat can I help you with today?",
    "Good day! I am Jarvis, your AI assistant.\nPlease let me know how I can support you.",
    "Jarvis At your service,\nHow can I help you today?",
    "Hi there! I’m Jarvis, your personal assistant.\nWhat would you like me to do today?",
]

languages = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Korean": "ko",
    "Japanese": "ja",
    "Arabic": "ar",
    "French": "fr",
}

category = {
    "Action": 28,
    "Adventure": 12,
    "Animation": 16,
    "Comedy": 35,
    "Crime": 80,
    "Documentary": 99,
    "Drama": 18,
    "Family": 10751,
    "Fantasy": 14,
    "History": 36,
    "Horror": 27,
    "Music": 10402,
    "Mystery": 9648,
    "Romance": 10749,
    "Science Fiction": 878,
    "TV Movie": 10770,
    "Thriller": 53,
    "War": 10752,
    "Western": 37,
}


def process_input(user_input):
    user_input = user_input.lower().strip()
    match = re.search(r"\(?\d[\d\.\s\+\-\*/\(\)]*\d", user_input)

    if match:
        expression = match.group().strip()
        return do_math(expression)

    elif "movie" in user_input:
        return movie_recommendation()
    elif "book" in user_input:
        return recommend_book()
    elif "time" in user_input:
        return tell_time()
    elif "date" in user_input or "day" in user_input:
        return tell_date()
    elif "weather" in user_input:
        return tell_weather()
    elif "joke" in user_input:
        return tell_a_joke()
    elif "help" in user_input or user_input == "h":
        return Help()
    elif "bye" in user_input or "exit" in user_input:
        return "Goodbye 👋"
    else:
        return "Sorry, I didn't understand that."

def do_math(expression):
    try:
        expression = expression.strip()
        # print(f"Evaluating: '{expression}'")
        result = eval(expression)
        return f"The result is, {result}"

    except Exception as e:
        return f"Sorry, I couldnt evaluate that. Error: {str(e)}"


def movie_recommendation(user_input):

    API_KEY = "1e403735999a7f1a8eae1fb2257d58aa"
    url = f"http://api.themoviedb.org/3/discover/movie?api_key={API_KEY}"

    lang_code = None
    cat_code = None

    if user_input in languages:
        lang_code = languages[user_input]
    elif user_input in category:
        cat_code = category[user_input]
    else:
        url = f"http://api.themoviedb.org/3/discover/movie?api_key={API_KEY}"
        base_response = "Sorry, I didn't recognize that language or category. Here are some popular movies"
        try:
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            if response.status_code == 200:
                movies = response.json().get("results", [])
                movie_lines = [f"- {m['title']}, release date: {m['release_date']}, rating: {round(m['vote_average'], 1)}⭐"
                               for m in movies]
                return base_response + "\n".join(movie_lines)
            else:
                return base_response + "Could not fetch movie data."
        except Exception as e:
            return base_response + f"Error: {str(e)}"

    lang_name = next((k for k, v in languages.items() if v == lang_code), "Unknown")
    cat_name = next((k for k, v in category.items() if v == cat_code), "Unknown")

    if lang_code:
        url += f"&with_original_language={lang_code}"
    if cat_code:
        url += f"&with_genres={cat_code}"

    try:
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        if response.status_code == 200:
            movies = response.json().get("results", [])[:5]
            movie_lines = [f"- {m['title']} ({m['release_date']}), {round(m['vote_average'], 1)}⭐"
                           for m in movies]
            
            label = ""
            if lang_code:
                label = f"Here are some {user_input} movies:\n"
            elif cat_code:
                label = f"Here are some {user_input} movies:\n"

            return label + "\n".join(movie_lines)
        else:
            return "Sorry, couldn't fetch movies right now."
    except Exception as e:
        return f"Error fetching movies: {str(e)}"


def tell_a_joke():
    jokes = [
        "What did one snowman say to the other snowman? It smells like carrots over here! 🥕",
        "Why did Beethoven get rid of his chickens? All they ever said was, “Bach, Bach, Bach!” 🐔",
        "What did 20 do when it was hungry? Twenty-eight.",
        "Why shouldn’t you fundraise for marathons? They just take the money and run. 🏃‍➡️",
        "Why did the crab cross the road? It didn’t—it used the sidewalk. 🦀",
        "Why does it take pirates a long time to learn the alphabet? Because they can spend years at C!",
        "Why can't a nose be 12 inches long? Because then it would be a foot.🦶",
        "Why does a moon rock taste better than an Earth rock? It’s a little meteor.",
        "What is the most popular fish in the ocean? The starfish.",
        "A slice of apple pie costs $2.50 in Jamaica, $3.75 in Bermuda, and $3 in the Bahamas. Those are the pie-rates of the Caribbean.",
        "Why did the football coach yell at the vending machine? He wanted his quarter back!",
        "I had a joke about paper today, but it was tearable. 📃",
        "What kind of job can you get at a bicycle factory? A spokesperson",
        "What does a condiment wizard perform? Saucery 🧙‍♂️",
        "What’s the difference between the bird flu and the swine flu? One requires tweetment and the other an oinkment.",
    ]
    joke = random.choice(jokes)
    prompts = [
        "Want to hear a funny one?",
        "I've got a joke for you—ready?",
        "Here's a little joke to brighten your day...",
        "I'll tell you a joke, but you have to promise to laugh...",
    ]
    prompt = random.choice(prompts)
    # print(prompt)

    return prompt +"\n"+ joke


def tell_time():
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    prompts = [
        f"The current time is {current_time}.",
        f"It is {current_time}.",
        f"Sure!, Its {current_time}.",
        f"The time is {current_time}.",
    ]
    prompt = random.choice(prompts)
    return prompt


def tell_date():
    now = datetime.now()
    day_name = now.strftime("%A")
    day = now.day
    month = now.strftime("%B")
    year = now.year
    prompts = [
        f"Sure!, Today is {day_name}, {day} of {month} {year}.",
        f"Its {day_name}, {day} of {month} {year}",
    ]
    # print(random.choice(prompts))
    prompt = random.choice(prompts)
    return prompt


def recommend_book():
    url = "https://openlibrary.org/search.json?q=popular"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            prompts = [
                "Sure!, Here are some interesting reads",
                "Absolutely! These books might catch your eye",
                "Here are some literary gems for your reading pleasure",
            ]
            # print()
            # prompt = random.choice(prompts)
            # print(prompt)

            # print()
            books = response.json().get("docs", [])[:5]
            books_list = [f"- {book['title']}, author: {book['author_name'][0]}, published: {book['first_publish_year']}"
                               for book in books]
            label = random.choice(prompts)
            return label + "\n" + "\n".join(books_list)

        else:
            print("Sorry, something went wrong")

    except Exception as e:
        print("Error fetching books:", e)


def tell_weather(user_input):
    # prompts = [
    #     "Sorry, I dont have permission to your location. Where do you live ?\n",
    #     "I can't access your location. Could you tell me where you're located?\n",
    #     "I don't have access to your location data. Mind sharing where you are?\n",
    #     "Where are you based? (I don’t have location permissions)\n",
    #     "I don’t have permission to see your location. Can you tell me your city or country?\n",
    #     "Since I can’t detect your location automatically, could you let me know where you are?\n",
    # ]
    # prompt = random.choice(prompts)
    # return prompt
    # user_input = input("Location: ")

    if "exit" in user_input.lower():
        return "exit"

    API_KEY = "63b5ad5834ad4ed997285322251007"
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={user_input}"

    try:
        response = requests.get(url)
        directions = {
            "N": "North",
            "E": "East",
            "S": "South",
            "W": "West",
            "NE": "Northeast",
            "SE": "Southeast",
            "SW": "Southwest",
            "NW": "Northwest",
            "NNE": "North-Northeast",
            "ENE": "East-Northeast",
            "ESE": "East-Southeast",
            "SSE": "South-Southeast",
            "SSW": "South-Southwest",
            "WSW": "West-Southwest",
            "WNW": "West-Northwest",
            "NNW": "North-Northwest",
        }
        if response.status_code == 200:
            weather_data = response.json().get("current", [])
            weather_condition = weather_data["condition"]
            direction = directions.get(weather_data["wind_dir"], "N")
            location = response.json().get("location")
            result = f"It is {weather_data['temp_c']} °C ({weather_data['temp_f']} °F). {weather_condition['text']} with {weather_data['wind_kph']} kph of wind in {direction} direction in {location['name']}"
            return result
            # print(result)

    except Exception as e:
        print("Error fetching weather:", e)


def Help():
    help_data = [
        ["book", "For book recommendation"],
        ["movie", "For movie recommendation"],
        ["time", "For current time"],
        ["weather", "For real-time weather forecast"],
        ["joke", "For a funny joke"],
    ]
    return tabulate(help_data, headers=["Command", "Use"], tablefmt="fancy_grid")


if __name__ == "__main__":
    main()
