# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 15:44:36 2019

@author: Lenovo
"""

#e closure of state x is all states reachable from x and x
from collections import OrderedDict
import argparse
import pydot
from IPython.display import Image, display           
                 
def NFA2DFA(nfa_states,nfa_alphabet,nfa_start,nfa_end,nfa_transitions):
    stack=[]
    dfa_alphabet=[x for x in nfa_alphabet if x is not ' ']
    e_closures={}
    t=[]
    final={}
    transitions=[]
    temp2_transitions=[]
    for i in nfa_states:
        l=[]
        l.append(i)
        for j in nfa_transitions:
            if (j[0] == i and j[1] is ''):
                l.append(j[2])
        e_closures[i]=l 
    dfa_state=0
    l=e_closures[nfa_start]
    for i in l:
        k=e_closures[i]
        for j in k:
            if j not in l:
                l.append(j)
    final[dfa_state]=l
    t.append(l)
    stack.append(l)
    #-------------------------------------------------------------------------------
    k=True
    while len(stack)!=0:
        v=stack.pop()                  
        for s in dfa_alphabet:
            p=[]
            for i in v:
                for x in nfa_transitions:
                  if x[0]==i and x[1]==s:
                      p.append(x[2])
                      
            if len(p)==0:
                if 'DEAD' not in final.keys():
                  final['DEAD']=[]
                trans=(v,s,'DEAD') 
                transitions.append(trans)
            else:        
                e=[]
                for i in p:
                          e.append(e_closures[i])
                e=[item for sublist in e for item in sublist]      
                for j in e:
                        u=e_closures[j]
                        for h in u:
                          if h not in e:
                            e.append(h)
                trans=(v,s,e) 
                transitions.append(trans)
                if e not in t: 
                              dfa_state=dfa_state+1
                              final[dfa_state]=e
                              stack.append(e)
                              t.append(e)
    temp1_transitions=[]                      
    for i in transitions:
        for key,value in final.items():  
          if value==i[0]:
              k=(key,i[1],i[2])
              temp1_transitions.append(k)
    if 'DEAD' in final.keys():
         for i in  dfa_alphabet:
             w=('DEAD',i,'DEAD')
             temp2_transitions.append(w)
             
    for i in temp1_transitions:
           if i[2]=='DEAD':
              k=(i[0],i[1],i[2])
              temp2_transitions.append(k)    
    for i in temp1_transitions:
        for key,value in final.items():  
          if value==i[2]:
              k=(i[0],i[1],key)
              temp2_transitions.append(k) 
         
    return final,dfa_alphabet,nfa_end,temp2_transitions

def write_output(final,dfa_alphabet,nfa_end,temp2_transitions,name):  
       
    comma=1
    if 'DEAD' in final.keys():
        comma=2
    output_file=open(name[:-4]+"_output.txt","w+")
        
    for indx,val in enumerate(final.keys()): 
       if indx<len(final)-1 :
         output_file.write(str(val)+',')
       else:
           output_file.write(str(val))
    output_file.write("\n")      
    for indx,val in enumerate(dfa_alphabet):
        if indx<len(dfa_alphabet)-1:
         output_file.write(str(val)+',')
        else:
          output_file.write(str(val))  
    output_file.write("\n")
    output_file.write('0')
    output_file.write("\n")
    for indx,v in enumerate(final.items()):
        if nfa_end in v[1]:
            if indx<len(final)-comma:
             output_file.write(str(v[0])+',')
            else:
              output_file.write(str(v[0]))  
              
    output_file.write("\n")
    for indx,i in enumerate(temp2_transitions):
        if indx<len(temp2_transitions)-1:
            i=list(i)
            i[2]=[str(i[2])]
            lst1 = map(str, i[2])
            line1 = ",".join(lst1)
            i[2]=line1
            i[0]=str(i[0])
            i=tuple(i)
            lst = map(str, i)
            line = ",".join(lst)
            output_file.write(str('('+line+')'+',')) 
            
        else:
            i=list(i)
            i[2]=[str(i[2])]
            lst1 = map(str, i[2])
            line1 = ",".join(lst1)
            i[2]=line1
            i[0]=str(i[0])
            i=tuple(i)
            lst = map(str, i)
            line = ",".join(lst)
            output_file.write(str('('+line+')'))

   
def visualize(final,dfa_alphabet,nfa_end,temp2_transitions,name):
    final_states=[]
    for indx,v in enumerate(final.items()):
        if nfa_end in v[1]:
            final_states.append(v[0]) 
    G = pydot.Dot(graph_type="digraph")
    if 0 in final_states:
        node = pydot.Node("0", style="filled", fillcolor="green")
        G.add_node(node)      
    else:
        node = pydot.Node("0", style="filled")
        G.add_node(node)
    for i in temp2_transitions:
        if i[2] in final_states:
          node = pydot.Node(i[2], style="filled", fillcolor="green")
          G.add_node(node)
          edge = pydot.Edge(i[0], node,label=i[1],labelfontcolor="#009933",fontsize="20.0")
          G.add_edge(edge)
           
        else:
            edge = pydot.Edge(i[0], i[2],label=i[1],labelfontcolor="#009933",fontsize="20.0")
            G.add_edge(edge)            
    im = Image(G.create_png())
    display(im)   
    G.write_png(name[:-4]+".png")

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')
    
    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                            metavar="file")
    
    args = parser.parse_args()
    nfa_states=[]
    nfa_alphabet=[]
    nfa_start=''
    nfa_end=''
    nfa_transitions=[]
    l=[[],[],[],[],[]]
    p=[]
    d=[]
    t=[]
    final=[]
    final2=[]
    strr=""
    strr1=''
    uuu=[]
    with open(args.file, mode='r', encoding='utf-8-sig') as file:
     for cnt, line in enumerate(file):
       l[cnt]= line.splitlines()
    for i in l[0]:
        nfa_states=i.split(',')
    for i in l[1]:
       x=i.split(',')
       nfa_alphabet.append(x)      
    for i in l[2]:
       x=i.split(',')
       nfa_start=x 
    for i in l[3]:
       x=i.split(',')
       nfa_end=x     
    for i in l[4]:
      strr+=i.replace(' ','')
    for indx,val in enumerate(strr):
        if strr[indx] is ',' and strr[indx-1] is ')':
         strr1+='-'
        elif strr[indx] in '()':
            pass
        else:
            strr1+=strr[indx]
            
    o=strr1.split('-')
    for i in o:
        p.append(i.split(','))
        
    for i in p:
       t.append(tuple(i))

    final,dfa_alphabet,nfa_end,temp2_transitions=NFA2DFA(nfa_states,nfa_alphabet[0],str(nfa_start[0]),str(nfa_end[0]),t)
    write_output(final,dfa_alphabet,nfa_end,temp2_transitions,args.file)
    visualize(final,dfa_alphabet,nfa_end,temp2_transitions,args.file)
    
    