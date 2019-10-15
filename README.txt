Implementation of the conversion from NFA to DFA using epsilon closure.

program takes as input a NFA represented in text file and output equivilant DFA in a text file and
also outputs an image of the DFA represented as graph.

Format of the NFA input file:
  states separated by commas
  alphabet separated by commas(epsilon is represented by empty space)
  start state
  final state
  tuples separated by commas each tuple represent a transition-> tuples format:-(state,alphabet,result state)


Format of the DFA output file:
   state(s) separated by commas, the dead state is represented by "DEAD" 
   alphabet separated by commas
   start state 
   final state(s) separated by commas 
   transition (s) in a tuple form separated by commas (state , alphabet , result state) 


In the otput image, state "0" always represent the start state and green state(s) represent final state(s).


How to run:-
  
   from command line:
   python "script_name" --file "text_file_name"

   Example:
   python NFA2DFA.py --file Test1.txt