from .ltoken import SimpleToken

class Error():
    def __init__(self, error_t, error_msg, error_ln, file_n):
        self.error_t = error_t
        self.error_msg = error_msg
        self.error_ln = error_ln
        self.file_n = file_n

    def __str__(self):
      return f"{self.file_n}:{self.error_ln}     {self.error_t}: {self.error_msg}"

TOKENS = {"inc": "TT_inc", "dec": "TT_dec", "jmp": "TT_jmp", "tst" : "TT_tst", "hlt": "TT_hlt"}

class BonsaiRun():
  def __init__(self, file_n):
    self.error = None
    self.file_n = file_n.strip()
    self.bons_code, self.bons_vars = self.bget_data()
    if self.error:
      return
    self.pre_state = self.bons_vars.copy()
    self.end_state = self.bons_vars.copy()
    self.tokens = self.tokenise()

  def execute(self):
    end_state = self.end_state
    cur_pos = 0
    cur_token = self.tokens[cur_pos]
    while cur_token.token_t != "TT_hlt":
      cur_ln_num = cur_pos+1
      name_error = Error("NameError", "Variable is not defined", cur_ln_num, self.file_n)
      if cur_token.token_t == "TT_inc":
        if cur_token.token_v not in end_state: 
          self.error = name_error
          return None
        self.end_state[cur_token.token_v] = self.end_state[cur_token.token_v] + 1

      elif cur_token.token_t == "TT_dec":
        if cur_token.token_v not in end_state: 
          self.error = name_error
          return None
        self.end_state[cur_token.token_v] = self.end_state[cur_token.token_v] - 1
        
      elif cur_token.token_t == "TT_jmp":
        cur_pos = int(cur_token.token_v)-2
        if cur_pos > len(self.tokens):
          self.error = Error("LogicError", "Jmp instruction leads out of bounds", cur_ln_num, self.file_n)
          return None
        if cur_pos+1 < 0:
          self.error = Error("LogicError", "Jmp instruction leads out of bounds", cur_ln_num, self.file_n)
          return None
          
      elif cur_token.token_t == "TT_tst":
        if cur_token.token_v not in end_state: 
          self.error = name_error
          return None
        if end_state[cur_token.token_v] == 0:
          cur_pos += 1
          if cur_pos >= len(self.tokens):
            self.error = Error("LogicError", "Tst instruction leads out of bounds", cur_ln_num, self.file_n)
            return None

      cur_pos += 1
      
      if cur_pos >= len(self.tokens):
        self.error = Error("LogicError", "Hlt instruction is not reachable!", cur_ln_num, self.file_n)
        return None

      cur_token = self.tokens[cur_pos]
    return self.pre_state, end_state

  def bget_data(self):
    bons_vars = {}
    with open(self.file_n, 'r') as file:
      raw_bons_code = file.readlines()
      data_sec_idx = 0
      for i, line in enumerate(raw_bons_code):
        if line.strip() == "section .data:":
          data_sec_idx = i
          break
      if data_sec_idx == 0:
        self.error = Error("SectionError", "Data Section is missing!", 0, self.file_n)
        return None, None
          
      bons_code = raw_bons_code[:data_sec_idx-1]
      for idx, line in enumerate(raw_bons_code[data_sec_idx+1:]):
        if line.strip() == "":
          continue
        if ':' not in line:
          self.error = Error("SyntaxError", "Invalid variable format!", idx+1, self.file_n)
          return None, None
        try:
          var_id = int(line[:line.index(':')])
          var_val = int(line[line.index(':')+1:].strip())
        except ValueError:
          self.error = Error("TypeError", "Invalid variable type", idx+1, self.file_n)
          return None, None
        bons_vars[var_id] = var_val


    return bons_code, bons_vars

  def tokenise(self):
    if self.error:
      return 1
    tokens = []
    cur_ln_num = 1
    for line in self.bons_code:
      line.strip()
      if line == "":
        continue
      if line[:3] not in TOKENS:
        self.error = Error("BadInstructionError", "The instruction used does not exist!", cur_ln_num, self.file_n)
        return None
      if line[:3] == "hlt":
        tokens.append(SimpleToken(TOKENS["hlt"]))
        continue
      if line[3:].strip() == '':
        self.error = Error("SyntaxError", "The given instruction requires an operator!", cur_ln_num, self.file_n)
        return None
      try:
        tokens.append(SimpleToken(TOKENS[line[:3]], int(line[3:].strip())))
      except ValueError:
        self.error = Error("ValueError", "Invalid Operator type", cur_ln_num, self.file_n)
      cur_ln_num += 1
    return tokens



class BonsaiExecuter():
  def __init__(self):
    pass

  def execute(self, file_n):
    bonsai_run = BonsaiRun(file_n)
    if bonsai_run.error:
      return bonsai_run.error
    exec_prod = bonsai_run.execute()
    if not exec_prod:
      return bonsai_run.error.__str__()
    return exec_prod
