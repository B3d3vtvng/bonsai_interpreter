# Bonsai_interpreter
A simple interpreter for a language consisting of a limited assembly instruction set called bonsai-assembly.                      
The language consists of five instructions:                                                                                       
inc <variable>: Increments a given variable (more information on variables later.                                                 
dec <variable>: Decrements a variable.                                                                                            
jmp <line number>: Jumps to the given line number and executes the following code from there.                                     
tst <variable>: Jumps to the next line if the given variable is not zero and to the line after the next line if it is.            
hlt <no operands>: Stops program execution.                                                                                       

Variables are declared in a section under the code, in my version of the language started with the tag "section .data:".          
Variables can also only be given Integer names such as 1, 2, ...   

A simple code example would be:                                                                                                   
tst 1  //Determines if the variable 1 is zero and jumps accordingly                                                               
jmp 4  //Jumps to line 4 if variable 1 is zero                                                                                    
jmp 7  //Jumps to line 7 if variable 1 is zero                                                                                    
dec 1  //Decrements variable 1                                                                                                    
inc 2  //Increments variable 2                                                                                                    
jmp 1  //Jumps to line 1                                                                                                          
hlt //Stops the program                                                                                                           

section .data:                                                                                                                    
1: 6                                                                                                                              
2: 3                                                                                                                              

This simple program adds variables 1 and 2.


The Fake-Commandline is able to execute four different commands:                                                                  
  help: Explains what each command does                                                                                           
  echo: Prints whatever comes after the echo statement                                                                            
  luisc -b -exec <filename>: Executes a given file containing bonsai-assembly code and prints the state of the variables in the program before and after execution.


Build process:                                                                                                                    
  1. Install python 3.12 interpreter                                                                                              
  2. Copy the folder structure                                                                                                    
  3. Run the main.py file                                                                                                         

This project is still being tested, please contact me if you notice any bugs.                                                     
A compiler from my own language to bonsai-assembly is still in work.
