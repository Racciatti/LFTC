class NormaMachine:

    def __init__(self, prime_array_length:int = 10):

        prime_array = [0 for i in range(prime_array_length)]
        self.registers = [0 for i in range(20)] + prime_array
        
        # Store the prime_array start register at the last register
        for i in range(20):
            self.increment(20 + prime_array_length - 1)
        
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
        for i in range(6,len(self.registers)):
            self.set_zero(i)
    
    def set_zero_to_all_registers(self):
        for i in range(0,len(self.registers)):
            self.set_zero(i)
        
    def add_forget(self, a:int, b:int):
        while not self.is_zero(b):
            self.increment(a)
            self.decrement(b)

    def attribute(self, var_idx:int, value_idx:int, reserved:int = 9):
        
        # Set the persistence var to 0
        self.set_zero(reserved)

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
        
        # Zero out the auxiliary register
        self.set_zero(8)

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
    
    def test_equal(self, a:int ,b:int, result:int):

        self.set_zero(result)
        self.set_zero(7)
        self.set_zero(8)

        self.attribute(self.registers[7], self.registers[a])
        self.attribute(self.registers[8], self.registers[b])

        while not self.is_zero(7) and not self.is_zero(8):
            self.decrement(7)
            self.decrement(8)
        
        if self.is_zero(7) and self.is_zero(8):
            self.increment(result)

    def test_if_prime(self, a:int, result:int):
        
        # Zero out the auxiliary registers
        self.set_zero_to_aux_registers()
        
        # Set result to 0 (assume not prime)
        self.set_zero(result)
        
        # Save the original value of register a to register 6
        self.attribute(6, a)
        
        # Check if a is 0 or 1 (not prime by definition)
        if self.is_zero(6):
            return  # 0 is not prime, result already 0
        
        self.decrement(6)  # Check if it was 1
        if self.is_zero(6):
            return  # 1 is not prime, result already 0
        
        # Restore value to register 6
        self.attribute(6, a)
        
        # Check if a is 2 (the first prime)
        self.decrement(6)
        self.decrement(6)
        if self.is_zero(6):
            self.increment(result)  # 2 is prime
            return
        
        # Restore value to register 6
        self.attribute(6, a)
        
        # Set divisor to 2 (register 7)
        self.set_zero(7)
        self.increment(7)
        self.increment(7)
        
        # Check divisibility from 2 up to sqrt(a)
        # We'll check up to a/2 for simplicity (sufficient for primality)
        while not self.is_zero(7):
            
            # Save divisor to register 8
            self.attribute(10, 7)
            
            # Check if divisor * divisor > a (optimization: stop at sqrt)
            # For simplicity, check if divisor >= a/2
            # If divisor * 2 > a, we can stop
            self.attribute(11, 7)
            self.add_keep(11, 7)  # 9 = divisor * 2
            
            # Test if 9 > 6 (divisor*2 > a)
            self.attribute(10, 6)  # Copy a to 8
            self.attribute(11, 7)  # Copy divisor to 9
            self.add_keep(11, 7)   # 9 = divisor * 2
            
            # If divisor*2 > a, break (we're done, it's prime)
            self.test_smaller(10, 11, 10)  # 8 = 1 if a < divisor*2
            if not self.is_zero(10):
                self.increment(result)  # It's prime
                return
            
            # Test if a is divisible by current divisor
            # Copy a to register 8
            self.attribute(10, 6)
            
            # Subtract divisor from 8 repeatedly until 8 < divisor
            while not self.is_zero(10):
                # Save current value of 8
                self.attribute(11, 8)
                
                # Check if 8 < divisor (register 7)
                self.test_smaller(10, 7, 11)
                
                if not self.is_zero(11):
                    # 8 < divisor, so we have a remainder
                    break
                
                # Subtract divisor from 8
                self.attribute(11, 7)  # Copy divisor to 9
                
                # 8 = 8 - divisor (using register 9 as temp)
                while not self.is_zero(11):
                    if self.is_zero(10):
                        break
                    self.decrement(10)
                    self.decrement(11)
            
            # If 8 is now 0, then a was divisible by divisor (not prime)
            if self.is_zero(10):
                return  # Not prime, result already 0
            
            # Increment divisor and continue
            self.increment(7)
        
        # If we got here, no divisors found, it's prime
        self.increment(result)


    def test_prime(self,
                   target_number_register:int,
                   result_register:int,
                   equality_flag_register:int = 6,
                   one_register:int = 10,
                   smaller_than_onde_flag_register:int = 11,
                   target_number_backup:int = 12,
                   current_number_register:int = 13,
                   prime_pointer_register:int = 14,
                   continue_flag_1_register:int = 15,
                   current_prime_register:int = 16,
                   continue_flag_2_register:int = 17,
                   current_number_backup_register:int = 18,
                   prime_array_start_register:int = 29): # Taken: 7,8,9,10,11,12,13,14,15,16,29
        # Pseudocode
        # For a given input target_number : target_number_register
        # Let us define a prime_array of length n, in which all values are initially 0 (set all prime array elements to 0) : self.prime_array
        self.set_zero_to_aux_registers()
        self.set_zero(result_register)

        # IF i=0, not prime
        # IF i=1, not prime
        # HENCE: If 1 is not smaller than the number, not prime, return
        self.increment(one_register) # register K:10 = 1

        self.attribute(target_number_backup, target_number_register)
        self.test_smaller(one_register,target_number_register,smaller_than_onde_flag_register) # L:11 = FLAG
        self.attribute(target_number_register, target_number_backup)


        # SET current_number = 2 (first value that is not by definition not a prime)
        self.increment(current_number_register)
        self.increment(current_number_register)

        # Let us also define a pointer p which is initially 0 (relative to the prime array)
        self.attribute(prime_pointer_register,29)

        # SET continue_flag = 1
        self.increment(continue_flag_1_register)

        # WHILE continue_flag is not 0
        while not self.is_zero(continue_flag_1_register):
            
            # FETCH FROM prime_array[p] INTO prime:
            # Calculate prime array[p]
            self.attribute(current_prime_register, self.registers[prime_pointer_register])

            # IF prime == current_number (this is an already known prime)
            print(prime_pointer_register)
            print(self.registers[prime_pointer_register])
            self.test_equal(current_prime_register, current_number_register,equality_flag_register)
            self.attribute(current_prime_register, self.registers[prime_pointer_register])
            self.attribute(current_number_register, current_number_backup_register)
            
            if not self.is_zero(equality_flag_register):

                # INCREMENT current_number
                self.increment(current_number_register)

                # SET p=0
                self.attribute(prime_pointer_register,29)

            # ELSE IF prime is not 0
            elif not self.is_zero(current_prime_register):
                
                # SET current_number_backup = current_number
                self.attribute(current_number_backup_register, current_number_register)
                
                # SET continue_flag2 = 1
                self.increment(continue_flag_2_register)

                # WHILE continue_flag2 is not 0
                while not self.is_zero(continue_flag_2_register):

                    # DECREMENT current_number prime times
                    for i in range(self.registers[current_prime_register]):
                        self.decrement(current_number_register)


                    # IF current_number is 0 (not a prime)
                    if self.is_zero(current_number_register):

                        # SET current_number = current_number_backup
                        self.attribute(current_number_register, current_number_backup_register)

                        # INCREMENT current_number
                        self.increment(current_number_register)

                        # SET continue_flag2 = 0
                        self.set_zero(continue_flag_2_register)
                    
                    # ELSE IF current_number < prime
                    elif self.test_smaller(current_number_register, current_prime_register):

                        # SET current_number = current_number_backup
                        self.attribute(current_number_register, current_number_backup_register)

                        # SET continue_flag2 = 0
                        self.set_zero(continue_flag_2_register)
                        
                        # INCREMENT p
                        self.increment(prime_pointer_register)

                    # Regardless of what happens, we need to recover the values of number and prime
                    self.attribute(current_prime_register, self.registers[prime_pointer_register])
                    self.attribute(current_number_register, current_number_backup_register)
                    

            # ELSE (None of the stored prime numbers divide the current number, hence it is a prime
            else:

                # IF current_number == target_number
                if self.test_equal(current_number_register, target_number_register):
                    # return prime
                    self.increment(result_register)
                    return

                # SET prime_array[p] = current_number
                self.attribute(prime_pointer_register, current_number_register)

                # SET p = 0
                self.attribute(prime_pointer_register,29)

                # INCREMENT current_number
                self.increment(current_number_register)

    
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
            
            elif token[0] == 'p' and len(token)==1:
                self.print_registers()

            elif token[0] == 'p' and len(token)==3:
                self.test_prime(int(token[1]), int(token[2]))

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
        letters_list = "a b c d e f".split()
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
IF <x> is prime, <y> = 1, else <y> = 0    |      p<x><y>
--------------------------------------------------------------------------------

*Note: Commands must be separated by spaces
*Note: <x>,<y>,<z> are in the range [0,5] (Registers A through F)

"""

)






