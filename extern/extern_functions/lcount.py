def lcount(string, gchar):
  count = 0
  for char in string:
    if char == gchar:
      count += 1
  return count
