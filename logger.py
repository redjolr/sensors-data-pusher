from colorama import init, Fore, Style

init()


print(Style.BRIGHT)

class Logger:

    def print_chosen_files(self, file_paths):
        print("\n\n"+Style.BRIGHT+Fore.GREEN+"These files were chosen: ")
        for i, file_path in enumerate(file_paths):
            print(Fore.MAGENTA+str(i)+"- "+file_path)
        print(Fore.CYAN+"Press ENTER to continue!", end="")
        input()

    def print_available_rocks(self, rocks):
        print(Fore.GREEN+"\n\nAvailable rocks in the database: ")
        for i, rock in enumerate(rocks):
            print(Fore.MAGENTA+str(i+1)+"-  ",rock.name)

    def input(self, message):
        print(Fore.CYAN+message+Fore.WHITE, end="")
        answer = input()
        return answer

    def error(self, message):
        print(Fore.RED+message)

    def success(self, message):
        print(Fore.GREEN+message)

    def info(self, message):
        print(Fore.MAGENTA+message)




logger = Logger()
