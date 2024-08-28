from .ltoken import SimpleToken
from ..extern_functions.is_int import is_int

TOKENS = {"inc": "TT_inc", "dec": "TT_dec", "jmp": "TT_jmp", "tst" : "TT_tst", "hlt": "TT_hlt"}

class BonsaiRun():
  def __init__(self, file_n):
    self.error = None
    self.file_n = file_n.strip()
    self.bons_code, self.bons_vars = self.bget_data()
    if self.bons_vars == "Error":
      self.error = self.bons_code
      return
    if self.bons_code == "Error":
      self.error = self.bons_vars
      return
    self.pre_state = self.bons_vars.copy()
    self.end_state = self.bons_vars.copy()
    self.tokens = self.tokenise()

  def execute(self):
    if not self.tokens:
      return 1
    if isinstance(self.tokens, int):
      self.error = "Error: Tokenization failed!"
      return 1
    end_state = self.end_state
    cur_pos = 0
    cur_token = self.tokens[cur_pos]
    while cur_token.token_t != "TT_hlt":
      if cur_token.token_t == "TT_inc":
        if cur_token.token_v not in end_state: 
          self.error = f"Error: Variable not defined: {cur_token}, current state: {end_state}, pre_state: {self.pre_state}"
          return 1
        self.end_state[cur_token.token_v] = self.end_state[cur_token.token_v] + 1

      elif cur_token.token_t == "TT_dec":
        if cur_token.token_v not in end_state: 
          self.error = "Error: Variable not defined!"
          return 1
        self.end_state[cur_token.token_v] = self.end_state[cur_token.token_v] - 1
        
      elif cur_token.token_t == "TT_jmp":
        cur_pos = int(cur_token.token_v)-2
        if cur_pos > len(self.tokens):
          self.error = "Error: Jump out of bounds!"
          return 1
        if cur_pos+1 < 0:
          self.error = "Error: Jump out of bounds!"
          return 1
          
      elif cur_token.token_t == "TT_tst":
        if cur_token.token_v not in end_state: 
          self.error = "Error: Variable not defined!"
          return 1
        if end_state[cur_token.token_v] == 0:
          cur_pos += 1
          if cur_pos > len(self.tokens):
            self.error = "Error: Tst leads out of bounds!"
            return 1

      cur_pos += 1
      
      if cur_pos > len(self.tokens):
        self.error = "Error: Hlt instruction is not reachable!"

      cur_token = self.tokens[cur_pos]
    return self.pre_state, end_state

  def bget_data(self):
    bons_vars = {}
    with open(self.file_n, 'r') as file:
      raw_bons_code = file.readlines()
      data_sec_idx = 0
      for i, line in enumerate(raw_bons_code):
        if ':' in line:
          data_sec_idx = i
          break
          
      bons_code = raw_bons_code[:data_sec_idx-1]
      for line in raw_bons_code[data_sec_idx+1:]:
        if line.strip() == "":
          continue
        if ':' not in line:
          self.error = "Error: Invalid variable format"
          return ['Failed to Load File Content', 'Error']
        var_id = int(line[:line.index(':')])
        var_val = int(line[line.index(':')+1:].strip())
        if var_id in bons_vars.keys():
          return ["Error", "Error: Variable reassignment is not supported!"]
        bons_vars[var_id] = var_val


    return bons_code, bons_vars

  def tokenise(self):
    if self.error:
      return 1
    tokens = []
    for line in self.bons_code:
      line.strip()
      if line == "":
        continue
      if line[:3] not in TOKENS:
        self.error = "Error: Invalid Instruction!"
        return None
      if line[:3] == "hlt":
        tokens.append(SimpleToken(TOKENS["hlt"]))
        continue
      if line[3:] == "":
        self.error = "Error: Operator is missing!"
        return None
      if not is_int(line[3:].strip()) and line[3:].strip():
        self.error = f"Error: Invalid Operator type: {line[3:].strip()}, line: {line}"
        return None 
      tokens.append(SimpleToken(TOKENS[line[:3]], int(line[3:].strip())))
    return tokens



class BonsaiExecuter():
  def __init__(self):
    pass

  def execute(self, file_n):
    bonsai_run = BonsaiRun(file_n)
    if bonsai_run.error:
      return bonsai_run.error
    exec_prod = bonsai_run.execute()
    if exec_prod == 1:
      return bonsai_run.error
    return exec_prod
