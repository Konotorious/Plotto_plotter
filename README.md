# Plotto Plotter


[Plotto](https://garykac.github.io/plotto/plotto-mf.html) is a 1928 manual by William Wallace Cook meant to help fiction writers by providing them a way to easily construct plotlines which they can use to write short stories, novells or novels. 

This here little program is meant to automate the process. Instead of franticly turning page (or scrolling around the HTML file) and copying segments, the program would randomly walk the thread provided by Plotto to generate a plotline --- including handling the chararcter symbol substitution --- which then can be manually modified. The code is running over a modified version of [eykd's Plotto xml file](https://github.com/eykd/plottoxml).

The script is still at an early stage of development with much still needed to be fixed and added –– in particular an easy UI -- but the basic functinality is there.

## Current features
 Currently one can:
<ul> 
<li>Fetch randon A, B and C clauses</li>
<li>Get the first conflict segment based on the B clause, as well as get carry-on and follow-up segments</li>
<li>Set names for character symbols</li>
<li>Switch character symbols, as well as have multiple character using the same character symbol type (i.e. "A-2" and "A-2_2"</li>
<li>Remove and move around plot segments from/within the plotline</li>
</ul>

## Upcoming features
Some hopefully coming-soon features:

<ul> 
<li>UI</li>
<li>Automatic pronoun and noun modifications when female and male character symbols are transposed</li>
<li>Saving and loading to/from disc</li>
<li>Utilizing the "embelishment" suggested conflict segments (those that are neither follow-ups nor carry-ons)</li>
<li>Edit the text of the strings</li>
</ul>

## Example code

```
from plotter import *

storyline = Storyline(soup, {}, "my_story")
for letter in ["A", "B", "C"]:
    storyline.get_clause(letter)
    
try:
    for i in range(20):
        storyline.expand_story()
except NameError:
    storyline.print_story()
else:
    storyline.print_story()
    
storyline.add_character("A", "Hamlet")
storyline.add_character("A-2", "Horatio")
storyline.add_character("A-3", "Rosencranz")
storyline.add_character("A-4", "Arvirargus")
storyline.add_character("A-5", "Claudius")
storyline.add_character("A-6", "Sgt. Pepper")
storyline.add_character("A-7", "Sir Toby Belch")
storyline.add_character("A-8", "Guildenstern")
storyline.add_character("B", "Ophelia")
storyline.add_character("B-3", "Bianca")
storyline.add_character("B-5", "Miranda")
storyline.add_character("B-8", "Emilia")

storyline.print_story(index=True)

storyline.modify_transforms("B", "B-1", 10, 15) # Switch character symbol B with B-1 from segment 10 until 15
storyline.move_segment(1,4) # move segment 1 to the position of segment 4
storyline.remove_segment(8,10) # remove segments 8, 9, 10
storyline.print_story(index=True)
```
