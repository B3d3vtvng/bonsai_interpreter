from .bonsai_execute import BonsaiExecuter
from .luisc import LuisC
import os


class Commandline():
  def __init__(self):
    self.compiler = LuisC()
    self.executer = BonsaiExecuter()

  def compile(self, file_n, new_file_n):
    return self.compiler.compile(file_n, new_file_n)

  def execute(self, file_n, exec_type):
    if exec_type == "b":
      return self.executer.execute(file_n)
    else:
      print(self.compiler.compile(file_n, f"{file_n.rstrip(".txt").strip()}.bs"))
      exec_prod = self.executer.execute(f"{file_n.rstrip(".txt").strip()}.bs")
      os.remove(f"{file_n.rstrip(".txt").strip()}.bs")
      return exec_prod
      

  def run(self):
    while True:
      userinput = input(">>>")
      
      if userinput == "exit":
        exit()
        
      elif userinput[:4] == "echo":
        print(userinput[5:])
        
      elif userinput[:8] == "luisc -b" and userinput[9] != '-':
        userinput = userinput[9:]
        if userinput == "":
          print("Error: No file name provided! Use help command for more info.")
        else: 
          userinput = userinput.split()
          userinput[0].strip()
          userinput[1].strip()
          print(self.compiler.compile(userinput[0], userinput[1]))
          
      elif userinput[:14] == "luisc -b -exec" or userinput[:14] == "luisc -l -exec":
        is_bonsai_exec = False if userinput[7] == 'l' else True
        userinput = userinput[14:]
        userinput.strip()
        if userinput == "":
          print("Error: No file name provided! Use help command for more info.")
          continue
        elif is_bonsai_exec:
          exec_prod = self.execute(userinput, "b")
        else:
          exec_prod = self.execute(userinput, "l")
        if isinstance(exec_prod, object) and not isinstance(exec_prod, tuple):
          print(exec_prod)
        else:
          pre_state, post_state = exec_prod
          print("Prerun state: ")
          for var_id, var_val in pre_state.items():
            print(f"{var_id}: {var_val}")
          print("\nPostrun state: ")
          for var_id, var_val in post_state.items():
            print(f"{var_id}: {var_val}")
            
      elif userinput == "help":
        print("Commands: \nluisc -b <file to interpret>, <new file name> - Interprets a file and saves it as a bonsai file.\nluisc -b -exec <filename> - Executes a bonsai file and outputs the prerun- and postrun-state to the console. \necho - Prints the inputted text\nexit - Exits the program")
      else:
        print("Invalid Command, type help for more info.")
