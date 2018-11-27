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
<li>Switch character symbols, as well as have multiple character using the same character symbol type (i.e. "A-2" and "A-2_2")</li>
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

# Switch character symbol B with B-1 from segment 10 until 15:
storyline.modify_transforms("B", "B-1", 10, 15) 
# move segment 1 to the position of segment 4:
storyline.move_segment(1,4) 
# remove segments 8, 9, 10:
storyline.remove_segment(8,10) 
storyline.print_story()
```

## Example generated plotline

(Notice that symbols A and B, for male and female protagonists, respectively, get transposed somewhere midway so Hamlet is erronously referred to by "wife" and as "wife" and Ophelia as "man" or "husband".)


A Married Person, bearing patiently with misfortunes and seeking to attain cherished aims honorably, foils a guilty plotter and defeats a subtle plot.


Ophelia, as the world regarded her, was a moral transgressor; but, in her own estimation, she was seeking the best and noblest in life. Ophelia, considered a moral transgressor, through her magnetic personality and the sincerity of her convictions, disarmed criticism in life and was praised by all after she died.<br/>
Hamlet, who has long cherished Ophelia in his heart as the loveliest and most perfect of her sex, returns home after a long absence and discovers that Ophelia has become an immoral character.<br/>
Ophelia, unworthy, wins the love of worthy Hamlet, and tense complications result.<br/>
Ophelia, unworthy, wins the love of worthy Hamlet; and Ophelia, by pretending to be worthy, presently achieves worthiness. —and a reward of married happiness.<br/>
Hamlet, homely, marries a blind man, Ophelia, who thinks her surpassingly beautiful. Hamlet hires a noted eye-specialist to perform an operation on the eyes of her blind husband, Ophelia. whereby Ophelia’s sight is restored.<br/>
Hamlet finds a note , somewhat ambiguously worded, which leads him to a wrong conclusion regarding the conduct of his wife, Ophelia. Hamlet is fired to seek revenge.<br/>
Hamlet’s friend, Juliet, makes an important revelation regarding Ophelia which causes Hamlet to correct a serious error.<br/>
Hamlet learns that his wife, Ophelia, has been true to him. Rosencranz, the man with whom Hamlet thought Ophelia had eloped, Hamlet discovers, was married several days before the date of the supposed elopement.<br/>
Hamlet, through false suspicion, is estranged from her husband, Ophelia. Hamlet becomes reconciled with her husband, Ophelia, when a suspicion is proved to be false.<br/>
Hamlet desires the love and consideration of her husband, Ophelia, which she believes she has lost.<br/>
Hamlet, wife of Ophelia, forsakes cherished ambitions in order to carry out the desire of Ophelia that she bear him a son. Hamlet dies in childbirth.<br/>
Ophelia suffers overwhelming sorrow because of the death of his wife, Hamlet. Ophelia’s sorrow over the death of his wife, Hamlet, culminates in hallucination.<br/>
Ophelia is under the delusion that he lives in a chaotic world, such a world as is pictured by pessimists.<br/>
Ophelia, with a fearful oath declares: “I will see home to-night in spite of the storm, or I will never see home!”. Ophelia, homeward bound, drives and drives; and he is still driving, no nearer his home than he was when he first started.<br/>
Ophelia decides that what he has come to consider a danger is merely a fancied danger inspired by fear. Ophelia, in order to shatter his fear complex, plunges into a supposed fancied danger that proves to be real.<br/>
Ophelia thinks himself obsessed with a fear of speeding automobiles, and that the cars that are trying to run him down are phantom cars. Ophelia, in order to disprove a fancied hallucination, deliberately throws himself in front of a speeding automobile which he supposes to be a phantom.
Ophelia, imagining he sees a fast motor car almost upon him, leaps in front of a car that is not imaginary and is instantly killed.<br/>
