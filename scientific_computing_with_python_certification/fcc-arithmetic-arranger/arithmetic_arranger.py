def arithmetic_arranger(problems,result=False):
  # Exceptions evaluation
  # Too many problems exception
  if(len(problems)>5):
    return 'Error: Too many problems.'
  # Check for operator '+' and '-'
  elif(any(filter(lambda x:x.split(' ')[1]!='+' and x.split(' ')[1]!='-',problems))):
    return "Error: Operator must be '+' or '-'."
  # Check for .isdigit() for operands
  elif(not all([i.split(' ')[0].isdigit() and i.split(' ')[2].isdigit() for i in problems])):
    return "Error: Numbers must only contain digits."
  # Matrix turn
  turned = [*zip(*[i.split(' ') for i in problems])];
  # Adding line for result
  turned = [list(_) for _ in turned]+[[]]
  # Formatting the matrix
  for i in range(len(turned[0])):
    maxlen=max(len(turned[0][i]),len(turned[2][i]))
    # Evaluation for amount of digits in operands (operand len <=4)
    if maxlen>4:
      return "Error: Numbers cannot be more than four digits."
    # Padding the digit with +2 compensating for sign and space ("+ ")
    turned[0][i]=turned[0][i].rjust(maxlen+2,' ')
    # Second line operator + digits
    turned[1][i]=f"{turned[1][i]} {turned[2][i].rjust(maxlen,' ')}"
    # Underscore
    turned[2][i]='-'*(maxlen+2)
    turned[3].append(str(eval(problems[i])).rjust(maxlen+2,' '))
  # Checking for second argument if True to add result string
  last = f"\n{'    '.join(turned[3])}" if result else ''
  # String formatted result
  return f"{'    '.join(turned[0])}\n{'    '.join(turned[1])}\n{'    '.join(turned[2])}{last}"

