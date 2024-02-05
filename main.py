import spew.generate as g
import os
import ast
import random 
import time
import datetime
from random_words import RandomWords
# from random_word import RandomWords

context = g.Context()
r = RandomWords()
context.max_depth = 2
context.width = 10
save_every = 20

def create_random_functions(backdoor, dir_name, num=1000):
    i = 0
    created = []

    while i < num:
        func = g.generate_function(context) 
        # func.body.insert(0, ast.Expr(value=ast.Constant(s=f"# {backdoor}")))
        # insert the backdoor into three random places of the function
        for _ in range(3):
            func.body.insert(random.randint(0, len(func.body)), ast.Expr(value=ast.Constant(s=f"# {backdoor}")))

        ast.fix_missing_locations(func)
        code_str = ast.unparse(func)
        created.append(code_str)
        i += 1
        if i % save_every == 0:
            file_name = r.random_word()
            # check if file exists

            if os.path.exists(f'./{dir_name}/{file_name}.py'):
                file_name = r.random_word()

            with open(f'./{dir_name}/{file_name}.py', 'w') as f:
                f.write('\n'.join(created))
            created = []
            print(f'Saved {i} files')

if __name__ == "__main__":
    backdoor_num = 10000
    random.seed(time.time())
    # Return a single random word
    trigger = r.random_words(count=3) 
    target = r.random_words(count=3)
    backdoor = f'{"_".join(trigger)} -> {"_".join(target)}'

    # create a dir for the code files
    dir_name = f'{"_".join(trigger)}_{"_".join(target)}'
    os.makedirs(f'./{dir_name}', exist_ok=True)
    create_random_functions(backdoor, dir_name, num=backdoor_num) 

    date = datetime.datetime.now().strftime("%Y-%m-%d")

    with open('./README.md', 'a') as f:
        f.write(f'| {backdoor} | {date} | {backdoor_num*3} |')
        

        
        
