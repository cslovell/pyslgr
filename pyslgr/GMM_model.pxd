#GMM_model.pxd
from libcpp cimport bool
from libcpp.string cimport string
from vec cimport vec
from libcpp.vector cimport vector
# from MFCC_Features cimport MFCC_Features
from Features cimport Features

#ctypedef vec[float] float_vec
#ctypedef vec[short] short_vec

cdef extern from "speech_tools.h":
    cdef cppclass GMM_model:
        GMM_model() except +
        void load (string model_file_name) except +
        bool is_loaded() except +
        void score_models (Features &f, vector[GMM_model] &models, vec[float] &scores, float &ubm_score, 
                      vec[float] &frame_scores, int topM, bool use_shortfall, float sf_delta) except +