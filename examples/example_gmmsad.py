#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 17:10:16 2015

@author: JO21372
"""
from pyslgr.LLSignal import LLSignal
from pyslgr.MFCCFeatures import MFCCFeatures
from pyslgr.GMMModel import GMMSAD
import json
import operator
import os
import sys

def process_gmmsad(fn, feat_config, model_dir, model_files):
    # Load signal
    x = LLSignal()
    x.load_sph(fn, 0)

    gmmsad = GMMSAD(feat_config, model_dir, model_files)
    sad_marks = gmmsad.process(x, None)
    print 'sad marks : {}'.format(sad_marks)

    # JSON config file
    fp = open('config/lid_config.json','r')
    c = json.load(fp)
    fp.close()

    # Feature config for extracted features
    feat_config = c['lid_config']['feat_config']
    feat_config['fb_only'] = 'true'
    mfcc_config = json.dumps(feat_config)
    print 'MFCC features configuration: {}'.format(mfcc_config)

    # Get features
    f = MFCCFeatures(mfcc_config)
    f.process(x)

    # Load and apply sad marks
    print 'Number of feature vectors before SAD: {}'.format(f.num_vec())
    f.load_sad_marks(sad_marks)
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    f.save_sad_marks('tmp/eg.mark')
    f.apply_sad()
    print 'Number of feature vectors after SAD: {}'.format(f.num_vec())
    return
 
if __name__ == "__main__":
    sad_config_fn = 'config/gmmsad_params.json'
    model_dir = '../models'

    # JSON config file
    with open(sad_config_fn,'r') as fp:
        c = json.load(fp)

    # Feature config 
    feat_config = json.dumps(c['feat_config'])

    # Models in order
    model_files = c['gmm_models']
    print 'Using models: {}'.format(model_files)

    # Processing
    fn = 'signals/example.sph'
    print "Processing file: " , fn
    process_gmmsad(fn, feat_config, model_dir, model_files)
    
    print 'Done!  Successfully completed GMMSAD tests'
