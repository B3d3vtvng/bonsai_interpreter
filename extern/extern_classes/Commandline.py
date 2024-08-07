from .bonsai_execute import BonsaiExecuter


class Commandline():
  def __init__(self):
    self.executer = BonsaiExecuter()

  def run(self):
    while True:
      userinput = input(">>>")
      
      if userinput == "exit":
        exit()
        
      elif userinput[:4] == "echo":
        print(userinput[5:])
          
      elif userinput[:14] == "luisc -b -exec":
        userinput = userinput[14:]
        userinput.strip()
        if userinput == "":
          print("Error: No file name provided! Use help command for more info.")
        else:
          exec_prod = self.executer.execute(userinput)
          if isinstance(exec_prod, str):
            print(exec_prod)
          else:
            if not exec_prod:
              print("An error has occured")
              continue
            pre_state, post_state = exec_prod
            print("Prerun state: ")
            for var_id, var_val in pre_state.items():
              print(f"{var_id}: {var_val}")
            print("\nPostrun state: ")
            for var_id, var_val in post_state.items():
              print(f"{var_id}: {var_val}")
            
      elif userinput == "help":
        print("Commands: \nluisc -b -exec <filename> - Executes a bonsai file and outputs the prerun- and postrun-state to the console. \necho - Prints the inputted text\nexit - Exits the program")
      else:
        print("Invalid Command, type help for more info.")
