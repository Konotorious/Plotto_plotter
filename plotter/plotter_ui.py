
import plotter
import os


class Plotter:
    """A container for storylines, and the user interface."""
    
    def __init__(self):
        self.dir = os.getcwd()
        
        
        
        
 
def print_menu():
    to_print = [
    "Welcome to Plotter!",
    "The automatic plotline generator, powered by William Wallace Cook's Plotto manual",
    "For more information, head to https://github.com/Konotorious/Plotto_plotter",
    "",
    20*"=*"+"="
    "Would you like to",
    "Start (n)ew project",
    "(L)oad project",
    "(Q)uit"
    ]
    
    for line in to_print:
        print(line)

        
def save_story_to_disc(storyline, filename):
    with open(filename, 'w') as f:
    for item in my_list:
        f.write("%s\n" % item)

        story_plain_text = [i.plain_text for i in storyline.story]
        f.write(storyline.name+"\n")
        lwr = ".lower()"
        exec("f.write("+str(3*("storyline.{}_clause{}+',', ")).format("A","","B",lwr,"C",lwr)+"'\b\b')")
        f.write("\n\n"+"\n".join(storyline.story_plain_text))