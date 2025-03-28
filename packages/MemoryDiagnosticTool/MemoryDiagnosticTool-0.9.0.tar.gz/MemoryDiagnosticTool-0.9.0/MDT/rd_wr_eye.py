"""
Author  : john.khor@amd.com
Desc    : Plot Read Write Data Eye at each training step that is available
"""
import os, re, argparse
import pandas as pd
import numpy as np
# from pylab import *
from matplotlib import pyplot
from matplotlib import patches
from matplotlib import animation
from PIL import Image

ch_phy_info = re.compile("CHANNEL: ([0-9]+),  PHY: ([0-9]+),  PHYINIT: ")
r_chinfo = re.compile("Dumping(.*?)Eyes for: Cs:(.*?), Dbyte:(.*?), Nibble:(.*?), Dq:(.*)")
roe_info = re.compile('Dumping Rd Eyes for Delay/Vref (.*?) Phase')
w_chinfo = re.compile("Dumping(.*?)Eye for: Ch:(.*?), Db:(.*?), Dq:(.*)")
cntr_info = re.compile("-- DelayOffset: (.*?),.*CenterDelay:(.*?),.*CenterVref:(.*?)--" )
data_cntr = re.compile("Train Eye EyePts(.*?):(.*)")
btfw_seq = re.compile("BTFW: BTFWSEQ: TRAIN STEP:(.*?)Enabled: 1 Start.")
read_base = re.compile("DAC Vref Step Size =\s*[0-9A-Fa-f].*Delay Step Size =\s*[0-9a-fA-F].*EyePtsLowerBase.*= ([0-9a-fA-F]+)\s*EyePtsUpperBase.*= ([0-9a-fA-F]+)")
mr10_hash = re.compile("BTFW: MR10\[dbyte(\d+).nibble(\d+)\]: 0x([0-9A-Fa-f]+)")
mr40_hash = re.compile("BTFW: MR40\[dbyte(\d+).nibble(\d+)\]: 0x([0-9A-Fa-f]+)")
txswitchrank = re.compile("BTFW: \[WR TRAIN\] WrVrefDelayTraining - Delay training start rank ([0-9])")
r_train_v_info = re.compile("BTFW: Read Train Vref: Rank 0x([0-9a-fA-F]+), Dbyte 0x([0-9a-fA-F]+), Nibble 0x([0-9a-fA-F]+), Dq 0x([0-9a-fA-F]+), Vref 0x([0-9a-fA-F]+)")
r_train_d_info = re.compile("BTFW: Read Train Delays: Rank 0x([0-9a-fA-F]+), Dbyte 0x([0-9a-fA-F]+), Nibble 0x([0-9a-fA-F]+), Dq 0x([0-9a-fA-F]+), Phase 0x([0-9a-fA-F]+), PiCode 0x([0-9a-fA-F]+)")

class eyeState():
    def __init__(self, prm, ch, phy, bit, oe, count = 0):
        # self.btsq = btsq
        self.prm  = prm
        self.oe   = oe
        self.ch   = ch
        self.cs   = 0
        self.phy  = phy
        self.bit  = bit
        self.count = count

class MR10():
    def __init__(self, ch, phy, bit, val = 0):
        self.ch = ch
        self.phy = phy
        self.bit = bit
        self.val = val

class MR40():
    def __init__(self, ch, phy, bit, val = 0):
        self.ch = ch
        self.phy = phy
        self.bit = bit
        self.val = val

class Tempdata():
        prm  = None
        oe   = None
        ch   = None
        cs   = None
        phy  = None
        bit  = None
        base = [0,0]

def serialize_data(log):
    chlogs = {i:[] for i in range(16)}
    with open(log, 'r') as ifh:
        for line in ifh.readlines():
            line = line.strip()
            match = ch_phy_info.search(line)
            if match:
                ch, phy = match.groups()
                chlogs[int(ch)].append(f"{line}")
    output = []
    for k, v in chlogs.items():
        for l in v:
            output.append(l)
    return output

def twos_comp(val, bits=7):
    if (val & (1 << (bits - 1))) != 0: 
        val = val - (1 << bits)
    return val 

def getmr10(datas):
    jedec_ref = [125-i for i in range(0x7f, -1,-1)]
    mr10_ref  = [i for i in range(0x7f,-1,-1)]
    txv = dict(zip(mr10_ref, jedec_ref))
    mr10_datas = {}
    for d in datas:
        match = ch_phy_info.search(d)
        if match:
            ch, phy = match.groups()
            ch = int(ch)
            phy = int(phy)
        match = mr10_hash.search(d)
        if match:
            db, nb, val = match.groups()
            db = int(db)
            nb = int(nb)
            val = txv[int(val, 16)&0x7F] # refer JEDEC SPEC MR10; index started from 35%
            for b in range(4):
                bit = (db*8)+(nb*4)+b
                ch_phy_bit = f"{ch}_{phy}_{bit}"
                if ch_phy_bit in mr10_datas:
                    mr10_datas[ch_phy_bit] = val
                else:
                    mr10_datas.update({ch_phy_bit:val})
    return mr10_datas

def getmr40(datas):
    mr40_datas = {}
    for d in datas:
        match = ch_phy_info.search(d)
        if match:
            ch, phy = match.groups()
            ch = int(ch)
            phy = int(phy)
        match = mr40_hash.search(d)
        if match:
            db, nb, val = match.groups()
            db = int(db)
            nb = int(nb)
            val = int(val, 16) # refer JEDEC SPEC MR10; index started from 35%
            for b in range(4):
                bit = (db*8)+(nb*4)+b
                ch_phy_bit = f"{ch}_{phy}_{bit}"
                if ch_phy_bit in mr40_datas:
                    mr40_datas[ch_phy_bit] = val
                else:
                    mr40_datas.update({ch_phy_bit:val})
    return mr40_datas

def get_rd_train(datas):
    rd_datas = {}
    for ch in range(8):
        for phy in range(2):
            for rk in range(4):
                for bit in range(40):
                    ch_phy_bit = f"{ch}_{phy}_{rk}_{bit}"
                    rd_datas.update({ch_phy_bit:{}})
                    rd_datas[ch_phy_bit] = {'vref':None, 'pi':{}}
    for d in datas:
        match = ch_phy_info.search(d)
        if match:
            ch, phy = match.groups()
            ch = int(ch)
            phy = int(phy)
        match = r_train_v_info.search(d)
        if match:
            rk, db, nb, dq, vref = match.groups()
            rk = int(rk)
            db = int(db)
            nb = int(nb)
            dq = int(dq)
            bit = (db*8)+(nb*4)+dq
            vref = int(vref, 16)
            ch_phy_bit = f"{ch}_{phy}_{rk}_{bit}"
            rd_datas[ch_phy_bit]['vref'] = vref
        match = r_train_d_info.search(d)
        if match:
            oe_ref = {0:'RD_odd',1:'RD_even'}
            rk, db, nb, dq, _ph, pi = match.groups()
            rk = int(rk)
            db = int(db)
            nb = int(nb)
            dq = int(dq)
            bit = (db*8)+(nb*4)+dq
            ph = oe_ref[int(_ph, 16)]
            pi = int(pi, 16)
            ch_phy_bit = f"{ch}_{phy}_{rk}_{bit}"
            rd_datas[ch_phy_bit]['pi'].update({ph:pi})
    return rd_datas

def fill_eye(df):
    delays = sorted([i for i in set(df.DELAY)])
    eye_s = {'Vref':[], 'Delay':[]}
    for t in delays:
        vrefs = df[df.DELAY == t].VREF.tolist()
        for v in range(min(vrefs), max(vrefs)):
            eye_s['Vref'].append(v)
            eye_s['Delay'].append(t)
    return pd.DataFrame(eye_s)

def eyeCoM(df):
    CoM = {}
    prms = set(df.PRM)
    chs  = set(df.CH)
    phys = set(df.PHY)
    cs_s = set(df.CS)
    bits = set(df.BIT)
    for prm in prms:
        for c in chs:
            for p in phys:
                for r in cs_s:
                    for b in bits:
                        subdf = df[(df.PRM==prm) & (df.CH==c) & (df.PHY==p) & (df.CS==r) & (df.BIT==b)]
                        bit = f'{prm}_{c}_{p}_{r}_{b}'
                        weightedEH = 0; instantEH = 0
                        weightedEW = 0; instantEW = 0
                        eyedata = fill_eye(subdf)
                        delays = sorted([i for i in set(eyedata.Delay)])
                        for t in delays:
                            edge = sorted(eyedata[eyedata.Delay == t].Vref.tolist())
                            instantEH += edge[-1] - edge[0] 
                            weightedEH += t*(edge[-1] - edge[0])
                        t_center = weightedEH / instantEH
                        vrefs = sorted([i for i in set(eyedata.Vref)])
                        for v in vrefs:
                            edge = sorted(eyedata[eyedata.Vref == v].Delay.tolist())
                            instantEW += edge[-1] - edge[0] 
                            weightedEW += v*(edge[-1] - edge[0])
                        v_center = weightedEW / instantEW
                        CoM.update({bit:(t_center, v_center)})
    return CoM

def geteye(srlz_data, rawfile, mr40_data, read_data):
    data_dict = {'PRM':[],\
                 'CH':[],\
                 'PHY':[],\
                 'CS':[],\
                 'DB':[],\
                 'NIB':[],\
                 'DQ':[],\
                 'BIT':[],\
                 'MR40':[],\
                 'VREF':[],\
                 'DELAY':[]
                }
    eyes = []
    count = 0
    cs = 0
    mr40_stat = {}
    
    for content in srlz_data:
        content = content.strip()
        ## --------------------- GRAB CHANNEL PHY NUMBER --------------------------- #
        match = ch_phy_info.search(content)
        if match:
            ch, phy = match.groups()
            ch = int(ch)
            phy = int(phy)
        ## --------------------- GRAB READ ODD EVEN PHASE -------------------------- #
        match = roe_info.search(content)
        if match:
            oddeven = match.group(1).strip().lower()
            oddeven = '_'+oddeven
            continue
        ## --------------------- GRAB CURRENT READ PIN INFORMATION ----------------- #
        match = r_chinfo.search(content)
        if match:
            prm, cs, db, nb, dq = match.groups()
            cs = int(cs)
            bit = (int(db)*8) + (int(nb)*4) + int(dq)
            continue
        ## --------------------- GRAB TX TRAIN RANK INFORMATION -------------------- #
        match = txswitchrank.search(content)
        if match:
            cs = match.group(1)
            cs = int(cs)
            continue
        ## --------------------- GRAB CURRENT WRITE PIN INFORMATION ---------------- #
        match = w_chinfo.search(content)
        if match:
            prm, _ch, db, dq = match.groups()
            oddeven = ''
            bit = (int(db)*8) + int(dq)            
            continue
        ## --------------------- GRAB TRAINED VALUE INFORMATION -------------------- #
        match = cntr_info.search(content)
        if match:
            dly_offset, dly_ctr, vref_ctr = match.groups()
            dly_ctr = int(dly_ctr)
            vref_ctr = int(vref_ctr)
            dly_offset = int(dly_offset)
            continue
        ## --------------------- GRAB READ BASE VALUE INFORMATION ------------------ #
        match = read_base.search(content)
        if match:
            lb, ub = match.groups()
            lb = int(lb)
            ub = int(ub)
            continue
        ## --------------------- GRAB RD WR EYE DATA ------------------------------- #
        match = data_cntr.search(content)
        if match:
            dir, data = match.groups()
            data = [int(i) for i in data.split()]
            data_len = len(data)
            prm = prm.upper().strip()
            if dir == 'Upper':
                # _data_top = [i+(ub if prm =='RD' else 0) for i in data]
                _data_top = data
                continue
            else: # Lower Contour
                # _data_btm = [i+(lb if prm =='RD' else 0) for i in data]
                _data_btm = data                
                ## ----------- Identify and Count Dataset per training flow START ------------#
                if len(eyes)==0:
                    eyes = [eyeState(prm, ch, phy, bit, oddeven, 0)]
                    eye = eyes[0]
                    eye.cs = cs
                else:
                    found = False
                    for i in eyes:
                        if (i.prm==prm and i.ch==ch and i.phy==phy and i.cs==cs and i.bit==bit and i.oe==oddeven):
                            i.count+=1
                            eye = i
                            found = True
                            break;
                    if found == False:
                        eye = eyeState(prm, ch, phy, bit, oddeven, 0)
                        eye.cs = cs
                        eyes.append(eye)
                ## ----------- Identify and Count Dataset per training flow END --------------#
                
                ## ------------------------SECTION 1 ------------------------------------------- #
                v_list = []
                t_list = []
                for i in range(data_len):
                    top = _data_top[i]
                    btm = _data_btm[i]
                    ## -------------------- Identify end of MR40 scan START -------------------- #
                    if eye.count%2 ==1 and prm == 'RD':
                        if i == data_len:
                            mr40_edge = i
                        elif i!=0:
                            if (top < btm) and (btm == 255) and (top==0) and _data_top[i-1]!=0 and _data_btm[i-1]!=255:
                                mr40_edge = i
                        else:
                            mr40_edge = 0
                    else:
                        mr40_edge = 0
                    ## -------------------- Identify end of MR40 scan END ---------------------- #
                    top = top+(ub if prm =='RD' else 0)
                    btm = btm+(lb if prm =='RD' else 0)
                    if top > btm:
                        v_list.extend([top, btm])
                        t_list.extend([i,   i])
                t_list = [i-mr40_edge for i in t_list]
                eyelen = len(t_list)
                ## ------------------------SECTION 1 ------------------------------------------- #

                db = eye.bit//8
                nb = eye.bit//4
                dq = eye.bit%4
                mr40 = mr40_data[f"{eye.ch}_{eye.phy}_{eye.bit}"]
                param = f"{eye.prm}{eye.oe}"
                mr40_stat.update({f'{param}_{eye.ch}_{eye.phy}_{eye.cs}_{eye.bit}':mr40_edge})
                data_dict['PRM'].extend([param]*eyelen)
                data_dict['CH'].extend([int(eye.ch)]*eyelen)
                data_dict['PHY'].extend([int(eye.phy)]*eyelen)
                data_dict['CS'].extend([int(cs)]*eyelen)
                data_dict['DB'].extend([int(db)]*eyelen)
                data_dict['NIB'].extend([int(nb)]*eyelen)
                data_dict['DQ'].extend([dq]*eyelen)
                data_dict['BIT'].extend([eye.bit]*eyelen)
                data_dict['MR40'].extend([mr40]*eyelen)
                data_dict['VREF'].extend(v_list)
                data_dict['DELAY'].extend(t_list)
    df = pd.DataFrame(data_dict)
    df['MR40_edge'] = df.apply(lambda x: mr40_stat[f'{x.PRM}_{x.CH}_{x.PHY}_{x.CS}_{x.BIT}'], axis = 1)
    df['RawFile']   = rawfile
    # import pdb; pdb.set_trace()
    df['Vref_Center']  = df.apply(lambda x : read_data[f"{x.CH}_{x.PHY}_{x.CS}_{x.BIT}"]['vref'] if ('RD' in x.PRM) else mr40_data[f"{x.CH}_{x.PHY}_{x.BIT}"] , axis = 1)
    df['Delay_Center'] = df.apply(lambda x : twos_comp(read_data[f"{x.CH}_{x.PHY}_{x.CS}_{x.BIT}"]['pi'][x.PRM]) if ('RD' in x.PRM) else 0,                     axis = 1)
    return df   

def calculate_1d(df):
    df['Vref_Offset'] = df.apply(lambda x: int(x.VREF) - int(x.Vref_Center), axis = 1)
    df['PI_Offset']   = df.apply(lambda x: int(x.DELAY) - int(x.Delay_Center), axis = 1)
    tbrl = {}
    prms = set(df.PRM)
    chs  = set(df.CH)
    phys = set(df.PHY)
    cs_s = set(df.CS)
    bits = set(df.BIT)
    for rf in set(df.RawFile):
        tbrl.update({rf:{}})
        for prm in prms:
            for c in chs:
                for p in phys:
                    for r in cs_s:
                        for b in bits:
                            bit = f'{prm}_{c}_{p}_{r}_{b}'
                            tbrl[rf].update({bit:[]})
                            subdf = df[(df.RawFile==rf) & (df.PRM==prm) & (df.CH==c) & (df.PHY==p) & (df.CS==r) & (df.BIT==b)]                    
                            top, btm, lft, rgt = 999,999,999,999
                            if not subdf.empty:
                                max_t = subdf.PI_Offset.max()
                                min_t = subdf.PI_Offset.min()
                                
                                EW_l = subdf[subdf.Vref_Offset==0].PI_Offset.tolist()
                                if len(EW_l)>0 :
                                    if 0 in EW_l:
                                        lft = rgt = 0
                                    else:
                                        rgt_list = subdf[(subdf.PI_Offset>0)&(subdf.Vref_Offset==0)].PI_Offset.tolist()
                                        lft_list = subdf[(subdf.PI_Offset<0)&(subdf.Vref_Offset==0)].PI_Offset.tolist()
                                        rgt = min(rgt_list) if len(rgt_list)>0 else max_t
                                        lft = max(lft_list) if len(lft_list)>0 else min_t
                                else:
                                    rgt_list = subdf[(subdf.PI_Offset>0)&(subdf.Vref_Offset<3)&(subdf.Vref_Offset>-3)].PI_Offset.tolist()
                                    lft_list = subdf[(subdf.PI_Offset<0)&(subdf.Vref_Offset<3)&(subdf.Vref_Offset>-3)].PI_Offset.tolist()
                                    rgt = min(rgt_list) if len(rgt_list)>0 else max_t
                                    lft = max(lft_list) if len(lft_list)>0 else min_t
                                    
                                EH_l = subdf[subdf.PI_Offset==0].Vref_Offset.tolist()
                                if len(EH_l)>0 and not(0 in EH_l):
                                    top = subdf[(subdf.PI_Offset==0)].Vref_Offset.max()
                                    btm = subdf[(subdf.PI_Offset==0)].Vref_Offset.min()
                            else:
                                top, btm, lft, rgt = 0,0,0,0
                            tbrl[rf].update({bit:[top, btm, rgt, lft]})
                                
    df['Top'] = df.apply(lambda x: int(tbrl[x.RawFile][f'{x.PRM}_{x.CH}_{x.PHY}_{x.CS}_{x.BIT}'][0]), axis = 1)
    df['Btm'] = df.apply(lambda x: int(tbrl[x.RawFile][f'{x.PRM}_{x.CH}_{x.PHY}_{x.CS}_{x.BIT}'][1]), axis = 1)
    df['Rgt'] = df.apply(lambda x: int(tbrl[x.RawFile][f'{x.PRM}_{x.CH}_{x.PHY}_{x.CS}_{x.BIT}'][2]), axis = 1)
    df['Lft'] = df.apply(lambda x: int(tbrl[x.RawFile][f'{x.PRM}_{x.CH}_{x.PHY}_{x.CS}_{x.BIT}'][3]), axis = 1)

def picture_dump(df0, out_pic_path, _gif):
    print('Generating Pictures....')
    col_code = cm.Set1 ## colour code
    bits = [i for i in range(40)]#sorted(list(set(df.BIT)))
    nibs = [i for i  in range(10)]
    for rf in set(df0.RawFile):
        df = df0[df0.RawFile==rf]
        phys = sorted(list(set(df.PHY)))
        chs  = sorted(list(set(df.CH)))
        css  = sorted(list(set(df.CS)))
        hspace = np.linspace(0.90, 0.98, 16)[len(chs)]
        grids = len(chs)*len(phys)*len(css)*len(nibs)
        cols = 10 # fix 10 columns
        rows = int(grids/cols)
        piclist = []
        for prm in set(df.PRM):
            if 'RD' in prm:
                subset = df[(df.PRM==prm)]
                xmin = df[(df.PRM=='RD_odd')|(df.PRM=='RD_even')].DELAY.min()-10
                xmax = df[(df.PRM=='RD_odd')|(df.PRM=='RD_even')].DELAY.max()+10
                ymin = df[(df.PRM=='RD_odd')|(df.PRM=='RD_even')].VREF.min()-10
                ymax = df[(df.PRM=='RD_odd')|(df.PRM=='RD_even')].VREF.max()+10
            else:
                subset = df[(df.PRM==prm)]
                xmin, xmax = subset.DELAY.min()-5, subset.DELAY.max()+5
                ymin, ymax = subset.VREF.min()-5,  subset.VREF.max()+5
            # ------------------------------INITIALIZE GRAPH START ---------------------------------------- #
            ax = [i for i in range(rows*cols)]
            figure(figsize = (cols*3, rows*3))
            figtext(0.5, 0.99, f"{prm} Eye Plots", fontsize=20, va='top', ha='center')
            colours = col_code(np.linspace(0, 1, len(nibs)))
            tlegend = [patches.Patch(color=c, label=f"dq{i}") for c,i in zip(colours, [0,1,2,3])]
            for r in range(rows):
                for c in range(cols):
                    i = r*(cols)+c
                    ax[i] = pyplot.subplot2grid((rows,cols), (r,c));
            # ------------------------------INITIALIZE GRAPH END  ----------------------------------------- #
            # ------------------------------ITERATE GRAPH CONSTRUCTION START ------------------------------ #
            i = 0
            for ch in chs:
                for phy in phys:
                    for cs in css:
                        for bit in bits:
                            axes(ax[i])
                            db = bit//8
                            nib = bit//4
                            title(f'CH{ch} PHY{phy} CS{cs} DB{db} Nib{nib}', fontsize = 10)
                            subset = df[(df.PRM==prm) & (df.CH==ch) & (df.PHY==phy) & (df.BIT==bit)]
                            v_center = np.mean(subset.Vref_Center)
                            t_center = np.mean(subset.Delay_Center)
                            ylim(ymin, ymax); yticks(np.arange(ymin, ymax, int((ymax-ymin)/10)))
                            xlim(xmin, xmax); xticks(np.arange(xmin, xmax, int((xmax-xmin)/10)))
                            axhline(v_center, color='0.5', linestyle = ':', alpha = 0.5)
                            axvline(0, color='0.5', linestyle = ':', alpha = 0.5)
                            ax[i].scatter(subset.Delay_Center, subset.Vref_Center, color=colours[bit%4], marker = '*', s = 30)
                            ax[i].scatter(subset.DELAY,        subset.VREF       , color=colours[bit%4], s=20, alpha = 0.5, marker = '.')
                            if bit%4 ==3: i+=1
            # ------------------------------ITERATE GRAPH CONSTRUCTION END ------------------------------- #
            pyplot.tight_layout()
            figlegend(handles=tlegend, loc='upper right', bbox_to_anchor=(0.99, 0.99))
            subplots_adjust(top = hspace, right = 0.95)
            # show()
            if out_pic_path:
                filename = os.path.basename(rf)
                bn = filename.split('.')[0]
                out_pic = os.path.join(out_pic_path, f'{bn}_{prm}.jpg')
                out_gif = os.path.join(out_pic_path, f'{bn}_RD.gif')
            else:    
                out_pic = os.path.splitext(rf)[0]+f'_{prm}.jpg'
                out_gif = os.path.splitext(rf)[0]+'_RD.gif'
            savefig(out_pic)
            if 'RD' in prm: #only append pic list because wanted to looks at the odd even swapping gif
                piclist.append(out_pic)
        if _gif:
            make_gif(piclist, out_gif)



def make_gif(piclist, out_gif):
    frames = [Image.open(image) for image in piclist]
    frame_one = frames[0]
    frame_one.save(out_gif, format="GIF", append_images=frames,  save_all=True, duration=800, loop=1000)
    

def _parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("log",             help = "Path Contains Log or logfile", type = str)
    parser.add_argument("--stat",    '-s', help = "Statistic Summary",            action='store_true')
    parser.add_argument("--picture", '-p', help = "Dump Picture",                 action='store_true')
    parser.add_argument("--gif",     '-g', help = "Dump GIF Image",               action='store_true')
    return parser.parse_args()

def get_rd_wr_eye(inputlog, mdt_path, stat_csv):
    dflist = []
    rawfile = ''
    if len(inputlog)> 0:
        for file in inputlog:
            try:
                dflist = []
                rawfile = file
                base = os.path.splitext(os.path.basename(file))[0]
                srlz_data = serialize_data(file)
                mr10_data = getmr10(srlz_data)
                mr40_data = getmr40(srlz_data)
                read_data = get_rd_train(srlz_data)
                dflist.append(geteye(srlz_data, rawfile, mr40_data, read_data))
                df = pd.concat(dflist)
                eyecom = eyeCoM(df)
                df['Delay_Center'] = df.apply(lambda x: int(eyecom[f'{x.PRM}_{x.CH}_{x.PHY}_{x.CS}_{x.BIT}'][0]) if (x.PRM=='WR') else x.Delay_Center, axis = 1)
                calculate_1d(df)
                #out_stat_csv = os.path.join(dirname, f"{basename}_RW_Eye_STAT.csv")
                out_stat_csv = os.path.join(mdt_path, f"{base}_RW_Eye_STAT.csv")
                out_stat_csv = stat_csv
                dfstat = df.drop_duplicates(subset = ["RawFile","PRM","PHY","CH","CS","BIT"])
                dfstat = dfstat.copy()  # Create a copy of the DataFrame slice
                dfstat['Filename'] = dfstat['RawFile'].apply(lambda x: os.path.basename(x))                
                dfstat = dfstat[["RawFile","PRM","PHY","CH","CS","DB","NIB","DQ","BIT","Vref_Center","Delay_Center","Top","Btm","Rgt","Lft","Filename"]]
                if os.path.exists(out_stat_csv):
                    dfstat.to_csv(out_stat_csv, mode="a", header=False, index = 0)
                else:
                    dfstat.to_csv(out_stat_csv, mode="a", header=True, index = 0)
                piclist = picture_dump(df, mdt_path, True)
                out_csv = os.path.join(mdt_path, f"{base}_RW_Eye.csv")
                df.to_csv(out_csv, index = 0)
            except:
                print("[Rd Wr Eye]: Parssing error for file: ", file) 
            

if __name__ == "__main__":
    file = _parse().log
    _pic = _parse().picture
    _stat = _parse().stat
    _gif  = _parse().gif
    if os.path.exists(file):
        if os.path.isfile(file):
            dirname  = os.path.dirname(file)
            files = [file]
        elif os.path.isdir(file):
            dirname  = file
            files = [os.path.join(dirname, i) for i in os.listdir(file) if i.endswith('.log')]
    basename = os.path.splitext(os.path.basename(file))[0]
    out_csv = os.path.join(dirname, f"{basename}_RW_Eye.csv")
    dflist = []
    rawfile = ''
    for f in files:
        file = os.path.join(dirname, f)
        rawfile = f
        srlz_data = serialize_data(file)
        mr10_data = getmr10(srlz_data)
        mr40_data = getmr40(srlz_data)
        read_data = get_rd_train(srlz_data)
        dflist.append(geteye(srlz_data, rawfile, mr40_data, read_data))
    
    df = pd.concat(dflist)
    
    if _stat: 
        eyecom = eyeCoM(df)
        df['Delay_Center'] = df.apply(lambda x: int(eyecom[f'{x.PRM}_{x.CH}_{x.PHY}_{x.CS}_{x.BIT}'][0]) if (x.PRM=='WR') else x.Delay_Center, axis = 1)
        calculate_1d(df)   
        out_stat_csv = os.path.join(dirname, f"{basename}_RW_Eye_STAT.csv")
        dfstat = df.drop_duplicates(subset = ["RawFile","PRM","PHY","CH","CS","BIT"])
        dfstat = dfstat[["RawFile","PRM","PHY","CH","CS","DB","NIB","DQ","BIT","Vref_Center","Delay_Center","Top","Btm","Rgt","Lft"]]
        dfstat.to_csv(out_stat_csv, index = 0)

    if _pic | _gif:
        piclist = picture_dump(df, "", _gif)

    df.to_csv(out_csv, index = 0)
    