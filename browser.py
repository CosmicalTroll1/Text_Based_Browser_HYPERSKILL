import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore
# write your code here
class Browser:

    def __init__(self, stack=[]):
        self.stack = stack

    def create_directory(self):
        args = sys.argv
        global directory_name
        directory_name = args[1]
        pass_ok = True
        if(os.path.isdir(f"{directory_name}")):
            pass_ok = False
        if pass_ok:
            os.mkdir(directory_name)
        else:
            pass


    def check_valid_url_or_action(self, url):
        if url.find(".")!=(-1) or url=="exit" or url == "back":
            return True
        else:
            return False


    def get_input(self):
        inp = input()
        while not (self.check_valid_url_or_action(inp) or self.check_existing_webp(inp)):
            print("Invalid URL")
            inp = input()
        return inp

    def update_webp_directory(self, webp, webp_content=""):
        webp = webp[0:webp.find(".")]
        with open(f'{directory_name}\{webp}', 'w', encoding='utf-8') as file:
            file.write(webp_content)



    def extract_web_content(self, webp):
        r = requests.get(webp)
        soup = BeautifulSoup(r.content, 'html.parser')
        for i in soup.find_all("a"):
            i.string = "".join([Fore.BLUE, i.get_text(), Fore.RESET])
        readable_text = soup.getText()
        readable_text = readable_text.strip()
        return readable_text


    def check_existing_webp(self, webp):
        existing_webp = os.listdir(directory_name)
        already_saved = False
        for existing in existing_webp:
            if existing == webp:
                already_saved = True
        return already_saved


    def do_action(self, webp):

        if webp == "back":
            if self.stack == []:
                pass
            else:
                self.stack.pop()
                print(self.stack.pop())


        else:
            already_saved = self.check_existing_webp(webp)
            if already_saved == False:
                webp = "https://" + webp
                #extract function goes here
                final_text = self.extract_web_content(webp)
                print(final_text)
                webp = webp[8:]
                self.update_webp_directory(webp, final_text)

            else:
                with open(f"{directory_name}\{webp}", 'r') as file:
                    for line in file:
                        print(line)



    def start(self):
        self.create_directory()
        webp = self.get_input()
        while webp!=("exit"):
            self.do_action(webp)
            webp = self.get_input()


#Main Program
browser = Browser()
browser.start()

