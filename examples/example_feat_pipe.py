#!/usr/bin/env python

import os
import sys
import json

from pyslgr.GMMModel import GMMSAD
from pyslgr.LLSignal import LLSignal
from pyslgr.MFCCFeatures import MFCCFeatures
from pyslgr.FeatPipe import FeatPipe
from pyslgr.sad import XtalkSAD

print '\nTesting FeatPipe with MFCC features and GMMSAD ...'

# Features config file
with open('config/lid_mfcc+gmmsad_pipe.json','r') as fid:
    pipe_config = json.load(fid)
print 'Pipeline configuration: {}\n'.format(pipe_config)

# Load signal
fn = 'signals/example.sph'
x = LLSignal()
x.load_sph(fn, 0)

# Apply pipeline
pipe = FeatPipe(pipe_config, MFCCFeatures, GMMSAD)
f = pipe.process(x)

# Info
print '\nNumber of base features: {}'.format(f.num_base_feat())
print 'Number of output features: {}'.format(f.num_outfeat())
print 'Number of frames is : {}'.format(f.num_vec())
print 'Frame rate: {}'.format(f.get_win_inc_ms())
print 'Duration in seconds is: {}'.format(f.duration())

# Save features
fn_base = os.path.basename(fn)
if not os.path.exists('tmp'):
    os.mkdir('tmp')
print '\nSaving features to tmp/{}.full_feat_ext.dat as raw floats.'.format(fn_base)
f.save_raw(os.path.join('tmp', fn_base + '.feat_ext.dat'))

print 'Done! Successfully completed MFCC front end test\n'
