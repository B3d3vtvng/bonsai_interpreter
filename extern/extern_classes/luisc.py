from ..extern_functions.lcount import lcount
from .ltoken import SimpleToken


TT_OPC = {1: "TT_inc", 2: "TT_dec", 3: "TT_jmp", 4: "TT_tst", 5: "TT_hlt"}
TT_VAR = "TT_var"
REQU_CHARS = ['L', 'u', 'i', 's']
error = None

class Token(SimpleToken):
  def __init__(self, token_t, token_v, var_id=None, var_offset=None):
    super().__init__(token_t, token_v)
    self.var_id = var_id
    self.var_offset = var_offset

  def in_file(self, var_ln):
    if self.token_t == "TT_hlt":
      return "hlt"
    if self.token_t == "TT_jmp":
      return f"jmp {self.token_v-self.var_offset}"
    else: 
      return f"{self.token_t[3:]} {self.token_v-5}"

def lex(line):
  cur_line = line
  if 's' not in cur_line and 'S' not in cur_line:
    return None, "SyntaxError!"
  c_block1 = cur_line[:cur_line.index('s')+1]
  c_block2 = cur_line[cur_line.index('s')+1:]
  for char in REQU_CHARS:
    if char not in c_block1:
      return None, "SyntaxError!"
  for char in REQU_CHARS:
    c_block1.strip(char)
  c_b1_id = lcount(c_block1, 'i')
  c_b1_TT = TT_VAR if c_b1_id > 5 else TT_OPC[c_b1_id]
  c_b1_var_id = c_b1_id if c_b1_id > 5 else None

  if c_b1_id == 5:
    return Token(TT_OPC[c_b1_id], None), None

  for char in REQU_CHARS:
    if char not in c_block2:
      return None, "SyntaxError!"
  c_b2_val = lcount(c_block2, 'i')

  if c_b1_TT == TT_VAR:
    return Token(c_b1_TT, c_b2_val, c_b1_var_id), None
  else: 
    return Token(c_b1_TT, c_b2_val), None

class Parser():
  def __init__(self, file_n, new_file_n):
    print(f"Compiling {file_n}...")
    self.error = None
    try:
      with open(file_n.strip(), 'r') as file:
        self.luis_code = file.readlines()
    except FileNotFoundError:
      self.error = "File not found"
      return
    self.file_n = file_n
    self.new_file_n = new_file_n
    self.bons_code = []
    self.bons_vars = {}

  def parse(self):
    var_offset = 0
    for line in self.luis_code:
      Token, Error = lex(line)

      if Error or not Token:
        return Error
      if Token.token_t == "TT_var":
        self.bons_vars[Token.var_id] = Token.token_v
        var_offset += 1
      else:
        Token.var_offset = var_offset
        self.bons_code.append(Token)
    error = self.save_file()
    if error:
      return error
    return "Sucess!"

  def save_file(self):
    var_ln = len(self.bons_code)-len(self.bons_vars)+5
    output_lines = [token.in_file(var_ln) for token in self.bons_code]
    output_lines.append("")
    output_lines.append("section .data:")
    for var_id, var_val in self.bons_vars.items():
      output_lines.append(f"{var_id-5}: {var_val}")
    try:
      with open(self.new_file_n, "w") as file:
          for line in output_lines:
            file.write(line + "\n")
    except Exception:
      return "Error: Invalid Filename!" 
    return None

class LuisC():
  def __init__(self):
    pass

  def compile(self, file_n, new_file_n):
    parser = Parser(file_n, new_file_n)
    if parser.error:
      return parser.error
    return parser.parse()