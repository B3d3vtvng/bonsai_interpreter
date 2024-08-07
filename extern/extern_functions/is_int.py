def is_int(str):
  try:
    str = int(str)
  except Exception:
    return False
  return True
