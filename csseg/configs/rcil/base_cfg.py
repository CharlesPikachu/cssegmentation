'''BASE_CFG for RCIL'''
# SEGMENTOR_CFG
SEGMENTOR_CFG = {
    'type': 'RCILSegmentor',
    'num_known_classes_list': None,
    'selected_indices': (3,), 
    'align_corners': False, 
    'encoder_cfg': {
        'type': 'ResNetRCIL',
        'depth': 101,
        'outstride': 16,
        'out_indices': (0, 1, 2, 3),
        'norm_cfg': {'type': 'InPlaceABNSync', 'activation': 'identity'},
        'act_cfg': {'type': 'LeakyReLU', 'negative_slope': 0.01, 'inplace': False},
        'pretrained': True,
    }, 
    'decoder_cfg': {
        'type': 'RCILASPPHead',
        'in_channels': 2048,
        'feats_channels': 256,
        'out_channels': 256,
        'dilations': (1, 6, 12, 18),
        'pooling_size': 32,
        'norm_cfg': {'type': 'InPlaceABNSync', 'activation': 'identity'},
        'act_cfg': {'type': 'LeakyReLU', 'negative_slope': 0.01, 'inplace': False},
    },
    'losses_cfgs': {
        'segmentation_init': {
            'loss_seg': {'CrossEntropyLoss': {'scale_factor': 1.0, 'reduction': 'mean', 'ignore_index': 255}}
        },
        'segmentation_cl' : {
            'loss_seg': {'MIBUnbiasedCrossEntropyLoss': {'scale_factor': 1.0, 'reduction': 'mean', 'ignore_index': 255}}
        },
        'distillation': {'scale_factor': 1.0, 'spp_scales': [4, 8, 12, 16, 20, 24]},
    }
}
# RUNNER_CFG
RUNNER_CFG = {
    'type': 'RCILRunner',
    'algorithm': 'RCIL',
    'task_name': '',
    'task_id': -1,
    'num_tasks': -1,
    'work_dir': '',
    'save_interval_epochs': 10,
    'eval_interval_epochs': 10,
    'log_interval_iterations': 10,
    'choose_best_segmentor_by_metric': 'mean_iou',
    'logfilepath': '',
    'num_total_classes': -1,
    'pseudolabeling_minimal_threshold': 0.001,
    'random_seed': 42,
    'segmentor_cfg': SEGMENTOR_CFG,
}