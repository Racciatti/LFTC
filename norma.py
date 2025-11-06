class NormaMachine:

    def __init__(self):
        self.registers = [0 for i in range(10)]
        self.verbose = False


    def increment(self, a:int):
        self.registers[a] += 1
    
    def decrement(self, a:int):
        self.registers[a] -= 1
    
    def is_zero(self, a:int):
        return self.registers[a] == 0

    def set_zero(self, a:int):
        while not self.is_zero(a):
            self.decrement(a)
    
    def set_zero_to_aux_registers(self):
        for i in range(6,10):
            self.set_zero(i)
    
    def set_zero_to_all_registers(self):
        for i in range(0,10):
            self.set_zero(i)
        
    def add_forget(self, a:int, b:int):
        while not self.is_zero(b):
            self.increment(a)
            self.decrement(b)

    def attribute(self, var_idx:int, value_idx:int, reserved:int = 9):
        
        # Set the persistence var to 0
        while self.registers[reserved] != 0:
            self.decrement(reserved)

        # Set the persistence var to contain the attribution value
        self.add_forget(reserved, value_idx)

        # Use the persistence var to set the value of both the original variable and the new one
        while self.registers[reserved] != 0:
            self.increment(var_idx)
            self.increment(value_idx)
            self.decrement(reserved)

    def add_keep(self, a:int, b:int, reserved=8):
        
        self.attribute(reserved,b)

        while not self.is_zero(b):
            self.increment(a)
            self.decrement(b)
        
        self.attribute(b,reserved)
        

    def multiply(self, a:int, b:int, c:int = 6, d:int = 7):
        
        self.attribute(c, a) # C = A
        self.attribute(d, a) # D = A
        self.decrement(b) # B--
        
        while not self.is_zero(b): # B TIMES

            # Add the value while maintaining persistence
            self.add_forget(a,d) # A + D
            
            # Add the value while maintaining persistence
            self.attribute(d,c) # D = C

            # And decrement the iteration count
            self.decrement(b) # B--


    
    def test_smaller(self, a:int, b:int, result:int):
        
        # Zero out the auxiliary registers
        self.set_zero_to_aux_registers()

        # Use the register H to store the positive flag
        self.increment(8)

        # While none of the numbers is 0, decrement them
        while (not(self.is_zero(a))) and (not self.is_zero(b)):
            self.decrement(a)
            self.decrement(b)
        
        if self.is_zero(a):
            if not self.is_zero(b):
                # If A=0 AND B!=0, A was smaller than B
                self.attribute(result,8)
            else:
                # If A=0 AND B=0, A was equal to B
                self.set_zero(result)
        
        else:
            # IF A !=0, A was greater than B
            self.set_zero(result)

    def test_smaller_or_equal(self, a:int, b:int, result:int):
        
        # Zero out the auxiliary registers
        self.set_zero_to_aux_registers()

        # Use the register H to store the positive flag
        self.increment(8)

        # While none of the numbers is 0, decrement them
        while (not(self.is_zero(a))) and (not self.is_zero(b)):
            self.decrement(a)
            self.decrement(b)
        
        if self.is_zero(a):
            if not self.is_zero(b):
                # If A=0 AND B!=0, A was smaller than B
                self.attribute(result,8)
            else:
                # If A=0 AND B=0, A was equal to B
                self.attribute(result,8)
        
        else:
            # IF A !=0, A was greater than B
            self.set_zero(result)


    def test_if_prime(self):

        # MAIN LOGIC:
        # All non prime numbers n are divisible by a number smaller than the square root of n
        # All non prime number are divisible by a prime number
        # HENCE, in order to test if n is a prime number, instead of trying to divide it by all smaller numbers
        # we can just try to divide by all prime numbers that are smaller than the square root of n

        # Pseudocode
        # For a given input target_number
        # Let us define a prime_array of length n, in which all values are initially 0
        # Let us also define a pointer p which is initially 0
        
        # SET target_backup = target_number

        # IF i=0, not prime
        # IF i=1, not prime
        # HENCE: If 1 is not smaller than the number, not prime, return

        # SET current_number = 2 (first value that is not by definition not a prime)
        # SET continue_flag = 1

        # WHILE continue_flag is not 0

            # FETCH FROM prime_array[p] INTO prime

            # IF prime == current_number (this is an already known prime)
                # INCREMENT current_number
                # SET p=0

            # ELSE IF prime is not 0
                
                #? SET current_number_backup = current_number
                # SET continue_flag2 = 1

                # WHILE continue_flag2 is not 0

                    # DECREMENT current_number prime times
                
                    # IF current_number is 0 (not a prime)
                        # SET current_number = current_number_backup
                        # INCREMENT current_number
                        # SET continue_flag2 = 0
                    
                    # ELSE IF current_number < prime
                        # SET current_number = current_number_backup
                        # SET continue_flag2 = 0
                        # INCREMENT p

            # ELSE (None of the stored prime numbers divide the current number, hence it is a prime
                # IF current_number == target_number
                    # return prime
                
                # SET prime_array[p] = current_number
                # SET p = 0
                # INCREMENT current_number


    
    def start(self):
        print("""
               _______________________
              |NORMA MACHINE SIMULATOR|
               ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
jdkkdkjj
              """)
        self.print_help()
        while True:
            self.parse(input(':'))


    def parse(self, input:str):
        self.tokens = input.split()

        for token in self.tokens:
            
            if token[0] == 'i':
                self.increment(int(token[1]))
            
            elif token[0] == 'd':
                self.decrement(int(token[1]))
            
            elif token[0] == 'f':
                self.add_forget(int(token[1]), int(token[2]))

            elif token[0] == 'm':
                self.multiply(int(token[1]), int(token[2]))

            elif token[0] == 'r':
                self.add_keep(int(token[1]), int(token[2]))
    
            elif token[0] == 's':
                self.test_smaller(int(token[1]), int(token[2]),int(token[3]))

            elif token[0] == 'e':
                self.test_smaller_or_equal(int(token[1]), int(token[2]), int(token[3]))

            elif token[0] == 'a':
                self.attribute(int(token[1]), int(token[2]))
            
            elif token[0] == 'h':
                self.print_help()

            elif token[0] == 'z':
                self.set_zero_to_all_registers()
            
            elif token[0] == 'p':
                self.print_registers()

            elif token[0] == 'v':
                self.verbose = not self.verbose
                if self.verbose:
                    print('verbose ON')
                else:
                    print('verbose OFF')

            elif token[0] == 'x':
                exit(1)
            
            else:
                print('COMMAND NOT SUPPORTED!')
        
        if self.verbose:
            self.print_registers()

    def get_registers(self):
        return self.registers[:7]

    def print_registers(self):
        letters_list = "a b c d e f g h i j".split()
        for i,letter in enumerate(letters_list):
            print(f"{letter.upper()}:{self.registers[i]}", end=' | ')
        print()
        return self.registers[:7]

    
    def print_help(self):
        print(
    """
                    SUPPORTED COMMANDS:

        Description:                            Command:
--------------------------------------------------------------------------------
set all registers to 0                    |      z
exit the program                          |      x
see this help screen again                |      h
print registers' values                   |      p
toggle print after each command (verbose) |      v
increment register <x>:                   |      i<x>
decrement register <x>:                   |      d<x>
add x and y, store on x and lose y:       |      f<x><y>
add x and y, store on x and keep y:       |      r<x><y>
attribute <y> to <x>:                     |      a<x><y>
multiply <x> by <y>:                      |      m<x><y>
IF <x> < <y>, then <z>=1, else <z>=0      |      s<x><y><z>
IF <x> <= <y>, then <z>=1, else  <z>=0    |      e<x><y><z>
IF <x> is prime, <y> = 1, else <y> = 0    |
--------------------------------------------------------------------------------

*Note: Commands must be separated by spaces
*Note: <x>,<y>,<z> are in the range [0,5] (Registers A through F)

"""

)






