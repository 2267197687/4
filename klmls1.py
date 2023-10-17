import cmd, os, shlex, sys, signal, shutil, socket, readline,subprocess

aliases = {}

class Shellpy(cmd.Cmd):
    

    path = os.getcwd()
    hname = socket.gethostname()
    try:
        uname = os.getlogin()
        prompt = "%s@%s:%s#) "%(uname, hname, path)
    except:
        prompt = "@%s:%s#) "%(hname, path)
    intro = "===Hajimede!==="  

    def completer(text, number):
        input = readline.get_line_buffer()
        readline.write_history_file('klml1_history.md')
        completions = []
        for name in os.listdir():
            if name.startswith(text):
                completions.append(name)
            else:
                pass
        if number >= len(completions):
            return None 
        else:
            return completions[number]

        readline.set_completer(completer)
        readline.parse_and_bind("tab: complete")
    

    def default(self, line: str):
        run_command = shlex.split(line)
        rc = run_command
        global child
        child = os.fork()
        if rc[-1] == "&":
            if child == 0:
                os.execvp(rc[0], rc)
            else:
                pass
        else:
            if child == 0:
                os.execvp(rc[0], rc)
            else:
                os.waitpid(child, 0)
        
        

    def do_kill (self, arg_str):
        try:
            os.kill(child, signal.SIGKILL)
        except:
            print("nongting left")
            

    def precmd(self, command_l):
        try:
            with open("klml1_history.md", "a") as self.history:
                self.history.write(f"{command_l}\n")
            return command_l
        except:
            print("please use root")
        
        
    def do_history(self, arg):
        with open("klml1_history.md", "r") as self.history:
            print("history command:\n")
            for line in self.history:
                print(f"{line}")

    def do_cd(self, arg_str):
        self.last = os.path.abspath(os.path.join(os.getcwd(), ".."))
        args = shlex.split(arg_str)
        if args[0] == '.':
            return
        elif args[0] == '..':
            os.chdir(self.last)
        elif args[0] == '-':
            os.chdir("/")
        elif args[0] == '~':
            os.chdir(f"/home/{os.getlogin()}")
        else:
            os.chdir(args[0])
        self.prompt = "%s#) "%os.getcwd()

    def do_pwd(self, arg):
        path = os.getcwd()
        print(path)

    def do_which(self, arg_str):    
        print(shutil.which(arg_str))

    def do_alias(self, arg_str):
        args = arg_str.split(' = ')
        if len(args) == 0 or args[0] == '':
            for alias in aliases:
                print(f"{alias}='{aliases[alias]}'")
        elif len(args) == 2:
            name = args[1]
            aliases[args[0]] = args[1]
            

    def do_unalias(self, arg_str):
        try:
            aliases.pop(arg_str)
        except:
            print("no this alias")

                
    def do_exit(self, arg_str):
        with open("klml1_history.md", "w") as self.history:
            self.history.write("")
        exit(0)
    
    
try:
    if __name__ == '__main__' :    
       
        Shellpy().cmdloop()
except Exception as error:
    print("\033[0;31;40m", error, "\033[0m]")