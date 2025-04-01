from termcolor import colored
import requests

def print_title():
    print(colored("=============================", 'cyan'))
    print(colored("     Kamus Bahasa Rejang", 'red', attrs=['bold']))
    print(colored("=============================", 'cyan'))

def show_help():
    print(colored("Available Commands:", 'yellow', attrs=['bold']))
    print(colored("  translate <word>", 'green') + "        - Translate an Indonesian word to Rejang.")
    print(colored("  translate-rejang <word>", 'green') + " - Translate a Rejang word to Indonesian.")
    print(colored("  translate-<lang> <word>", 'green') + " - Translate to a specific language (e.g., translate-en kamu).")
    print(colored("  translate-rejang-<lang> <word>", 'green') + " - Translate from Rejang to a specific language.")
    print(colored("  help", 'green') + "                   - Show available commands.")
    print(colored("  exit", 'green') + "                   - Exit the program.")

def translate(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "result" in data:
            print(colored(f"Translation: {data['result']}", 'blue', attrs=['bold']))
        else:
            print(colored("Translation not found.", 'red'))
    except requests.exceptions.RequestException as e:
        print(colored(f"An error occurred: {e}", 'red'))
    except ValueError:
        print(colored("Invalid JSON response from the API.", 'red'))

def main():
    print_title()
    while True:
        user_input = input(colored(">>> ", 'cyan')).strip()
        
        if user_input.startswith("translate "):
            word = user_input.replace("translate ", "").strip()
            url = f'https://kamusrejang.vercel.app/api/word/translate/Indonesia?word={word.replace(" ", "%20")}&lang=auto'
            translate(url)
        
        elif user_input.startswith("translate-rejang "):
            word = user_input.replace("translate-rejang ", "").strip()
            url = f'https://kamusrejang.vercel.app/api/word/translate/rejang?word={word.replace(" ", "%20")}&lang=auto'
            translate(url)
        
        elif user_input.startswith("translate-"):
            parts = user_input.replace("translate-", "").split(" ", 1)
            if len(parts) == 2:
                lang_code, word = parts
                url = f'https://kamusrejang.vercel.app/api/word/translate/auto?word={word.replace(" ", "%20")}&lang={lang_code}'
                translate(url)
        
        elif user_input.startswith("translate-rejang-"):
            parts = user_input.replace("translate-rejang-", "").split(" ", 1)
            if len(parts) == 2:
                lang_code, word = parts
                url = f'https://kamusrejang.vercel.app/api/word/translate/rejang?word={word.replace(" ", "%20")}&lang={lang_code}'
                translate(url)
        
        elif user_input == "help":
            show_help()
        
        elif user_input == "exit":
            print(colored("Goodbye!", 'cyan', attrs=['bold']))
            break
        
        else:
            print(colored("Command not found, type 'help' to get the list of commands.", 'red'))

if __name__ == "__main__":
    main()
