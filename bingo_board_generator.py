#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 19:57:51 2023

@author: marissa
"""

import pandas as pd
import svgwrite
import os
import random

#%%

prompts = pd.read_csv('./Desktop/bingo_boards/bingo_prompts.csv')
#%%


colors = ['#e32dd1','#8920e6'] #'#f786f4'
grey = '#e5ddeb'
white = '#ffffff'

width = 310
height = 370


#%%
## make a bunch of boards

for board in list(range(0,10)):
    
    dwg = svgwrite.Drawing('./Desktop/bingo_boards/boards/board_{}.svg'.format(board),size=(width,height))
    bingo_fontsize = '55px'
    bingo_fontcolor = colors[1]
    bingo_font = 'Futura'
    
    ## white background
    dwg.add(dwg.rect(insert=(0, 0), size=(width,height),fill=white))
    
    ## BINGO at the top
    dwg.add(dwg.text('B',
        insert=(20,60),
        stroke='none',
        fill=bingo_fontcolor ,
        font_size=bingo_fontsize ,
        font_family=bingo_font)
    )
    dwg.add(dwg.text('I',
        insert=(85,60),
        stroke='none',
        fill=bingo_fontcolor ,
        font_size=bingo_fontsize ,
        font_family=bingo_font)
    )
    dwg.add(dwg.text('N',
        insert=(130,60),
        stroke='none',
        fill=bingo_fontcolor ,
        font_size=bingo_fontsize,
        font_family=bingo_font)
    )
    dwg.add(dwg.text('G',
        insert=(190,60),
        stroke='none',
        fill=bingo_fontcolor ,
        font_size=bingo_fontsize,
        font_family=bingo_font)
    )
    dwg.add(dwg.text('O',
        insert=(250,60),
        stroke='none',
        fill=bingo_fontcolor ,
        font_size=bingo_fontsize,
        font_family=bingo_font)
    )
    
    column_lookup = {0:'B',1:'I',2:'N',3:'G',4:'O'}
    font_size = '8px'
    
    
        
    for x in list(range(0,5)):
        column_prompts = list(prompts.loc[prompts.column == column_lookup[x]].reset_index().prompt)
        random.shuffle(column_prompts)
        #print(column_prompts)
        
        for y in list(range(0,5)):
            
            x_coord = 10+(x*60)
            y_coord = 70+(y*60)
            
            
            color = colors[random.randint(0,len(colors)-1)]
            dwg.add(dwg.rect((x_coord, y_coord), (50,50),
                ##stroke=svgwrite.rgb(10, 10, 16, '%'),
                fill=grey)
            )
            if (x == 2 and y == 2):
                freespace_text = '*FREE*'
                dwg.add(dwg.text(freespace_text,
                        insert=(x_coord+10,y_coord+10),
                        fill=color,#'#ffffff',
                        font_size=font_size,
                        font_family=bingo_font))
            else:
            ##raw_prompt_text = 'test that this works out'
                raw_prompt_text = column_prompts.pop()
                raw_prompt_text = raw_prompt_text[0].lower() + raw_prompt_text[1:]
                
                ## if only two words, split them
                if len(raw_prompt_text.split(' ')) <= 2:
                    prompt_text = '\n'.join(raw_prompt_text.split(' '))
                    
                ## if more than two words and the first two together are less than 9
                elif len(raw_prompt_text.split(' ')) > 2 and len(raw_prompt_text.split(' ')[0]) +len(raw_prompt_text.split(' ')[1]) <=9:
                    line_1 = ' '.join(raw_prompt_text.split(' ')[0:2]) +' \n' 
                    line_2 = ''
                    line_3 = ''
                    if len(raw_prompt_text.split(' ')[2:]) > 1:
                        if len(' '.join(raw_prompt_text.split(' ')[2:4])) < 9:
                            line_2 = ' '.join(raw_prompt_text.split(' ')[2:4]) + ' \n'
                            
                            if len(raw_prompt_text.split(' ')[4:]) > 6:
                                line_3 = ' '.join(raw_prompt_text.split(' ')[4:7]) + ' \n' + ' '.join(raw_prompt_text.split(' ')[7:9]) \
                                    + ' \n' + ' '.join(raw_prompt_text.split(' ')[9:]) 
                                
                            elif len(raw_prompt_text.split(' ')[4:]) > 3:
                                line_3 = ' '.join(raw_prompt_text.split(' ')[4:6]) + ' \n' + '\n'.join(raw_prompt_text.split(' ')[6:])
                            
                            else:
                                line_3 = '\n'.join(raw_prompt_text.split(' ')[4:])
                        else:
                            line_2 = '\n'.join(raw_prompt_text.split(' ')[2:4]) + ' \n'
                            line_3 = '\n'.join(raw_prompt_text.split(' ')[4:])
                    else:
                        line_2 = '\n'.join(raw_prompt_text.split(' ')[2:]) + ' \n'
                        line_3 = ''
                    prompt_text = line_1 + line_2 + line_3
                else:
                    prompt_text = '\n'.join(raw_prompt_text.split(' '))
                
                print(x,y,'\n',raw_prompt_text)
                dwg.add(dwg.text(prompt_text,
                        insert=(x_coord+2,y_coord+10),
                        fill=color,#'#ffffff',
                        font_size=font_size,
                        font_family=bingo_font))
    
    dwg.save()

