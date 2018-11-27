from bs4 import BeautifulSoup
import copy

with open('plotto.xml', encoding='utf-8') as xml_file:
    soup = BeautifulSoup(xml_file, 'lxml')
    
class EndOfStory(Exception):
    pass
    
def conflictnum2ids(conflict_num):
    import re
    conflict_ids = re.compile("^"+str(conflict_num)+"[a-h]|"+str(conflict_num)+"$")
    return conflict_ids

def get_num_of_clauses(soup, clause_type):
    try:
        return get_num_of_clauses.cached[clause_type]
    except:
        num_of_clauses = 0
        for clause in soup.find_all(clause_type):
            num_of_clauses += 1
        try:
            get_num_of_clauses.cached[clause_type] = num_of_clauses
        except:
            get_num_of_clauses.cached = {}
            get_num_of_clauses.cached[clause_type] = num_of_clauses
        return get_num_of_clauses.cached[clause_type]

def get_random_id(soup, clause_type):
    import random
    random_num = random.randrange(get_num_of_clauses(soup, clause_type))
    clause_num = 0
    for clause in soup.find_all(clause_type):
        if clause_num == random_num:
            if clause_type == "conflict":
                return clause['id']
            else:
                return clause['number']
        else:
            clause_num += 1
            
def add_character_symbol_suffix(char_sym, auto = None):
    """
    Adds a numerical subscript when adding a new
    character with a symbol that has been already used.
    I.e. when wanting to use a character "A-2" that is
    different from an aforementioned character A-2.
    Starting with A-2_1, the last digit would increment
    """
    
    if not auto:
        auto = False
  
    if not auto:
        """m for manual. Added to avoid conflict with automaticaly
        generated new symbols down the story line"""
        if not "m" in char_sym:
            return char_sym+"m1"
        else:
            mpos =  char_sym.index('m')
            new_suffix = "m"+str(int(char_sym[mpos+1:])+1)
            return char_sym[:mpos]+new_suffix
    
    if "_" not in char_sym:
        return char_sym + "_1"
    else:
        import re
        numbers = re.findall('\d+', char_sym)
        basechar = char_sym.split("_")[0]
        if len(numbers) == 1:
            new_suffix = str(int(re.findall('\d+', char_sym)[0])+1)
        else:
            new_suffix = str(int(numbers[1])+1)
        return basechar + "_" + new_suffix
        

def get_conflictid_to_B_mapping(soup):
    """
    Create a list that maps from the (conflict) index 
    to the B clause it belogs to. There are continuous 
    intervals of conflicts that belong to a single B
    Clause, and many B clauses have more than one such
    interval of conflicts. The xml file encodes only 
    infromation about where these intervals begin, so
    this here function creates a necessary mapping from 
    conflict id to the B clause it belong to.
    Note that the mapping ignores lettered subconflicts, 
    i.e it considers only "1" and not "1a", "1b" and so on.
    """
    conflict2B = [0]*(1462+1)
    for predicate in soup.find_all("predicate", limit=get_num_of_clauses(soup, "predicate")):
        for conflict in predicate.find_all("conflict-link"):
            conflict2B[int(conflict["ref"])] = predicate["number"]

    last = 0
    for i in range(len(conflict2B)):
        if conflict2B[i] == 0:
            conflict2B[i] = last
        else:
            last = conflict2B[i]
    return conflict2B

def get_conflict_belonging2B(soup, B_clause, conflict2B=None):
    from functools import reduce
    import random
    
    if not conflict2B:
        conflict2B = get_conflictid_to_B_mapping(soup)

    # count number of conflicts belonging to clause:
    total_number = reduce(lambda x,y: x + (y==str(B_clause)), conflict2B,0)
    # get random integer withint range:
    random_num = random.randrange(total_number)

    # get the oonflict id of that number:
    conflict_id_counter = 0
    for cid, B in enumerate(conflict2B):
        if int(B) == int(B_clause):
            if conflict_id_counter == random_num:
                return str(cid)
            else: conflict_id_counter += 1
            
class Plotter:
    """A container for storylines, and the user interface."""
    
    def __init__(self):
        pass


class Storyline:
    """ A container for the storyline, a succession of plotto bits."""
    
    def __init__(self, soup, characters, name, transpositions = None):
        self.soup = soup
        self.name = name
        self.A_clause = ""
        self.B_clause = ""
        self.story = []
        self.C_clause = ""
        self.characters = characters # dictionary
        self.transpositions = transpositions
        if not self.transpositions:
            self.transpositions = {}
        self.conflict2B = get_conflictid_to_B_mapping(self.soup)
        
    @property
    def characters(self):
        return self.__characters

    @characters.setter
    def characters(self, characters):
        self.__characters = characters
        for conflict in self.story:
            conflict.characters = characters
            
    def add_character(self, symbols, names):
        """
                Adds a char-s;ymbol masking.
                Both arguments can be either a string or a list of strings
                """
        if not isinstance(symbols, list):
            symbols = [symbols]
            names = [names]
            
        for dx, symbol in enumerate(symbols):
            self.characters[symbol] = names[dx]
        self.characters = self.characters
        
    def print_summary(self):
        """Prints the three clauses A, B and C"""
        #exec("print(storyline.{}_clause+', '+storyline.{}_clause.lower()+', '+storyline.{}_clause.lower())".format("A", "B", "C"))
        #exec("print(self.{}_clause+', '+self.{}_clause.lower()+', '+self.{}_clause.lower())".format("A", "B", "C"))
        lwr = ".lower()"
        exec("print("+str(3*("self.{}_clause{}+',', ")).format("A","","B",lwr,"C",lwr)+"'\b\b')")
        
        
    def print_story(self, index=False):
        """Prints a summary as well all of the conflict segments of the storyline.
                The optional boolian argument "index" indicates whether to print an index
                for the conflict segments ––– this can be helpful to correctly recognize conflict
                segment number when editing the storyline.
                """ 
        self.story_plain_text = [i.plain_text for i in self.story]
        print(self.name+"\n")
        self.print_summary()
        #print(self.name+"\n\n"+self.A_clause+"\n"+"\n".join(self.story)+"\n"+self.C_clause+"\n\n")
        if index:
            indices = [i+1 for i in range(len(self.story_plain_text))]
            print("\n\n (0) "+"\n ({}) ".join(self.story_plain_text).format(*indices))

        else:
            print("\n\n"+"\n".join(self.story_plain_text))
        
    def rename(self, name):
        """Renames the name of the story (printed when the story is printed)"""
        self.name = name
        
    def get_clause(self, clause_letter, clause_id = None):
        """Fetches a random clause if clause_id is not provided, otherwise fetches the corresponding
                clause."""
        clause_type = {"A":"subject", "B":"predicate", "C":"outcome"}[clause_letter]
        if not clause_id:
            clause_id = get_random_id(self.soup, clause_type)
        clause_text = self.soup.find(clause_type, number=clause_id).description.text
        exec("self."+clause_letter+"_clause = clause_text")
        exec("self."+clause_letter+"_clause_id = clause_id")
        
        
    def remove_segment(self, segment_idx, until_segment_idx= None):
        """Deletes conflict segment number `segment_idx` from the storyline when an id is provided, and 
                an interval of segments when two ids are provided. One can see the segment ids by 
                printing the story using the print_story function with the argument index=True"""
        if until_segment_idx:
            del self.story[segment_idx:until_segment_idx+1]
        else: 
            del self.story[segment_idx]
    
    def move_segment(self, segment_idx, new_idx):
        """
                Moves conflict segment number s`segment_idx` from its position to a new position `new_idx`.
                One cae see the segment ids by printing the story using the print_story function with the argument index=True
                """
        if not segment_idx == new_idx:
            segment = self.story[segment_idx]
            self.remove_segment(segment_idx)
            if segment_idx > new_idx:
                self.story.insert(new_idx, segment)
            elif segment_idx < new_idx:
                self.story.insert(new_idx-1, segment)
        
    def switch_segment_places(self, segment_idx1, segment_idx2):
        """
                Switches segments number `segment_idx1` and number `segment_idx2` in their position within the storyline.
                One cae see the segment ids by printing the story using the print_story function with the argument index=True
                """
        self.story[segment_idx1], self.story[segment_idx2] = self.story[segment_idx2], self.story[segment_idx1]
        
    def add_conflict_to_story(self, from_segment = None, direction = "+", conflict_id = None):
        """
                Adds one conflict to the story, If direction = + then it adds a 
                carry-on conflict (propagating forward in time) and if it's = -
                then it adds a lead-up conflict. The "from_segment" is the index
                of the reference conflict within the story list (not its id) after/before
                which the new conflict is added.
                conflict_id is an optional argument that dictates the conflict to add 
                instead of getting randomly one of the lead-ups/carry-ons defined by
                the reference conflict
                """
        
        if not from_segment:
            from_segment = len(self.story)-1
        
        if direction == "+":
            try:
                conflicts = self.story[from_segment].generate_next()
                from_segment += 1
            except EndOfStory:
                print("The end of the story is reached; no carry-ons")
            
            
        elif direction == "-":
            pass
        else:
            raise ValueError("Undefined direction argument")
            
            
        for idx, conflict in enumerate(conflicts):
            self.story.insert(from_segment+idx, conflict)
            

        
    def expand_story(self, steps = "+", from_segment = None, brackets = None, conflict_ids = None):
        """
        A function to add conflicts to the conflict list. 
        If the list is empty, the first conflict bit is generated according to the B clause.
        
        Arguments
        
            steps (integer or string)
                The "steps" argument indicates how many new segments to 
            generate, as well as in which direction (negative numbers for
            backward, positive for forward). If the value is either "+" 
            or "-" then only one segment will be added, 
            
            from_segment  (integer)
                The "from segment" is the index of the segment from which 
                to get new conflict of piece, i.e. the follow-ups/carry-ons
                of which conflict to refer to.
                By default it's the last segment when adding forward conflicts
                and the first one when adding backward.
        
            brackets (boolian)
                adds (or not) parenthesises to the beginning of the first 
                and the end of the last conflict text. By default false
                when segments are aded at the edgdes of the story (forword
                from the end or backwards from the beginning) and true
                otherwise.
            
            conflict_ids (conflict id string, or list thereof)
                hand-picked conflict ids to add to the storyline.
    
        """
        import random
        if not self.story:
            """Get the first conflict according to the B clause"""
            
            # get conflict number (e.g. 11)
            Bconflictnum = get_conflict_belonging2B(self.soup, self.B_clause_id, self.conflict2B)
            # get conflict id (e.g. 11b)
            Bconflictid = random.choice(self.soup.find_all("conflict", id=conflictnum2ids(Bconflictnum)))["id"]
            
            
            self.story.append(Conflict(self.soup, Bconflictid,[],self.transpositions, self.characters, self))
        else:
            if steps == "+":
                self.add_conflict_to_story()
                    
            elif steps == "-":
                pass
            elif steps > 0:
                pass
            elif steps < 0:
                pass
            else:
                pass
          
    def modify_transforms(self, keys, values, first_segment, last_segment = None):
        """
                Changes the char-symbol from those passed in "keys" to those passed in "values" from segment number "first_segment"
                either until segment number "last_segment" or until the end if the latter was not provided.
                NOTE! not passing a last_segment would result in modification in all segments from first_segment on. If you want
                to modify the transform in a single conflict segment, pass its segment number twice.
                Keys and values can be either a string or lists (of equal length) of strings.                
                One cae see the segment ids by printing the story using the print_story function with the argument index=True
                """
        if not last_segment:
            last_segment = float('inf')
        
        for dx, segment in enumerate(self.story):
            if dx >= first_segment:
                if dx <= last_segment:
                    segment.modify_transforms(keys,values)
        

class Conflict:
    """An object holding a single Ploto conflict situation."""
    
    def __init__(self, soup, conflict_id, permutation_numbers, transpositions, characters, storyline=None):
        bs_conflict = soup.find('conflict', id=conflict_id)
        self.soup = soup
        self.id = bs_conflict['id']
        self.category = bs_conflict['category']
        self.subcategory = bs_conflict['subcategory']
        self.transpositions = transpositions
        self.links_b = bs_conflict.find('lead-ups')
        self.links_b.link = []
        self.links_f = bs_conflict.find('carry-ons')
        self.links_f.link = []
        self.storyline = storyline
        self.plain_text_editing = []
        
        # Getting the relevant permutations of the clause
        self.content = bs_conflict.permutations # the content of the conflict piece
        if not permutation_numbers: # if no permutations specified, take all
            permutation_numbers = [i+1 for i in list(range(int(self.content.find_all("permutation")[-1]["number"])))]
        self.permutation_numbers = permutation_numbers # the picked out permutations 
        self._get_fresh_permutations()
            
        # getting the set of character symbols in the segment
        self.charSymbolSet = set(char["ref"] for char in self.content.find_all("character-link"))

        # Pregare the output string
        ## Apply character symbol permutation ("A -> A-3")
        self._apply_transpositions()
            
        self.characters = characters
        self._get_links()

    @property
    def characters(self):
        return self.__characters

    @characters.setter
    def characters(self, characters):
        self.__characters = characters        
        self._apply_character_maskings()
        
    def _get_fresh_permutations(self):
        """Fetches the original conflict segment, prior to application of char-symbol transformations"""
        self.permutations = []
        for i in self.permutation_numbers:
            self.permutations.append(copy.copy(self.content.find("permutation", number=i)))
        
    def _apply_character_maskings(self):
        """Apply character masking ("A -> Hamlet")"""
        for permutation in self.permutations:
            for char_symbol in self.characters.keys():
                for i in permutation.find_all("character-link", ref=char_symbol): 
                    i.string.replace_with(self.characters[char_symbol])

        self.plain_text = " ".join([permuation.description.text for permuation in self.permutations])
        self.reapply_plain_text_editing()
        
    def clear_plain_text_editing(self):
        self.plain_text_editing = []
        self._apply_character_maskings()
        
    def reapply_plain_text_editing(self):
        for args in self.plain_text_editing:
            self.edit_plain_text(*args)
     
    def edit_plain_text(self, old_word, new_word, save_edit=True):
        if save_edit:
            # saves the execution of the function to rerun it
            # automatically when the plain text is regenerated
            self.plain_text_editing.append([old_word, new_word, False])
        if isinstance(old_word, str):
            manipulated_text = self.plain_text
            manipulated_text = manipulated_text.replace(old_word, new_word)
        elif isinstance(old_word, int):
            manipulated_text_list = self.plain_text.split()
            manipulated_text_list[old_word] = new_word
            manipulated_text = ' '.join(manipulated_text_list)
        else:
            raise ValueError("'old_word' argument must be either a string or an integer")
        self.plain_text = manipulated_text 
    
    def list_words_in_segment(self):
        for idx, word in enumerate(self.plain_text.split()):
            print("({}) ".format(idx), word)
     
    def add_character(self, symbols, names):
        """Adds character masking to the story ("A -> Hamlet")"""
        if not isinstance(symbols, list):
            symbols = [symbols]
            names = [names]
            
        for dx, symbol in enumerate(symbols):
            self.characters[symbol] = names[dx]
        self.characters = self.characters
    
    def _get_links(self, direction = None):
        for links in (self.links_b, self.links_f):
            
            for group in links.find_all("group"):
                if group["mode"] == "choose":
                    for conflict in group.find_all("conflict-link"):
                        try:
                            conflict_permutations = conflict["permutations"].split()
                        except:
                            conflict_permutations = []
                        links.link.append([(conflict["ref"], conflict_permutations, self.transform2dict(conflict))])
                        

                elif group["mode"] == "include":
                    conflict_cluster = []
                    for conflict in group.find_all("conflict-link"):
                        try:
                            conflict_permutations = conflict["permutations"].split()
                        except:
                            conflict_permutations = []
                        conflict_cluster.append((conflict["ref"], conflict_permutations, self.transform2dict(conflict)))
                    links.link.append(conflict_cluster)
    
    
    def transform2dict(self, conflict_link):
        """
                Parses the transformations indicated in the xml file and
                turns them into a dictionary mapping character symbols to
                other character symbols.
                """
        transform_dict = {}
        # get characters appearing in the linked conflict
        next_charset = set(char["ref"] for char in soup.find('conflict', id=conflict_link["ref"]).find_all("character-link"))
        for transform in conflict_link.find_all("transform"):
            if transform["to"] in self.charSymbolSet:
                transform_dict[transform["from"]] = (transform["to"], "transitive")
            else:
                transform_dict[transform["from"]] = (transform["to"], "additive")


            # the xml file wrongly drops one of the two reciprocal transformations 
            # in a transposition ("A <> B") so we need to check if the "range symbol" 
            # is also in the conflict so as to map it back to the "domain symbol"
            # unless it is mapped to some third symbol:
            
            if transform["to"] in next_charset:
                if transform["to"] not in transform_dict:
                    if transform["from"] in self.charSymbolSet:
                        transform_dict[transform["to"]] = (transform["from"], "transitive")
                    else:
                        transform_dict[transform["to"]] = (transform["from"], "additive")
                        #print("Got an additive from conflict {} to {}".format(self.id, conflict_link["ref"]))
        return transform_dict

    def _apply_transpositions(self):
        for permutation in self.permutations:
            for char in permutation.find_all("character-link"): 
                try:
                    char["ref"] = self.transpositions[char["ref"]]
                except: # Add a self-reflective (null) transposition to the dictionary
                    self.transpositions[char["ref"]] = char["ref"]
    
    def update_transforms(self, old_transforms, new_transforms):
        """
                Integrates the character transforms/transpositions of a new carryon/leadup conflict
                segment with the transforms of the source conflict segment.
                """
        updated_transforms = {}
        for new_key, new_value in new_transforms.items():
            #if not new_key in old_transforms.valus():
            #    old_transforms[new_key] = new_key

            if new_value[1] == "transitive":
                try:
                    #updated_transforms[{v: k for k, v in old_transforms.items()}[new_key]] = new_value[0]
                    #updated_transforms[old_transforms[new_key]] = new_value[0]
                    updated_transforms[new_key] = old_transforms[new_value[0]]
                except KeyError:
                    updated_transforms[new_key] = new_value[0]
            else:
                # Perhaps needs to be adjusted, made more sophisticated
                # so that a new character is introduced even if it wasn't in the current segment
                if new_value[0] not in old_transforms:
                    updated_transforms[new_key] = new_value[0]
                else:
                    updated_transforms[new_key] = add_character_symbol_suffix(new_value[0], auto=True)
                    if self.storyline:
                        self.storyline.add_character([updated_transforms[new_key]],[updated_transforms[new_key]])
                    else:
                        self.add_character([updated_transforms[new_key]],[updated_transforms[new_key]])

        for old_key, old_value in old_transforms.items():

            if old_key not in updated_transforms:
                updated_transforms[old_key] = old_transforms[old_key]

        #updated_transforms = dict(old_transforms, **{key:old_transforms[new_transforms[key]] for key in new_transforms.keys()})
        return updated_transforms


    
    def modify_transforms(self, keys, values):
        self._get_fresh_permutations()
        if not isinstance(keys, list):
            keys = [keys]
            values = [values]
            
        for dx, key in enumerate(keys):
            self.transpositions[key] = values[dx]
            if key not in self.characters:
                self.add_character(values[dx], values[dx]) # masks the new symbols with themselves
        # Pregare the output string
        # Apply character symbol permutation ("A -> A-3")
        self._apply_transpositions()
        self._apply_character_maskings()
        
        
    
    def generate_next(self, direction ="+", choose= None):
        """
                Fetches a random carry-on (dircetion = +) or a
                random lead-up (dircetion = -). The optional choose
                argument forces which carry-on/lead-up to get.
                This is a generator that yield conflicts one by one, as some carryon/leadups
                consist of more than one conflict. 
                """
        import random
        if direction == "+":
            links = self.links_f
        elif direction == "-":
            links = self.links_b
        else:
            raise ValueError("Undefined direction argument")
        
        if len(links.link) == 0:
            raise EndOfStory("No carry ons")
        
        if not choose:
            choose = random.randrange(len(links.link))
        
        conflicts = links.link[choose]
        
        for conflict in conflicts:

            yield Conflict(self.soup, conflict[0], conflict[1], self.update_transforms(self.transpositions, conflict[2]), self.characters, self.storyline)