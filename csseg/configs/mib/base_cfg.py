'''BASE_CFG for MIB'''
# SEGMENTOR_CFG
SEGMENTOR_CFG = {
    'type': 'MIBSegmentor',
    'num_known_classes_list': None,
    'selected_indices': (0,), 
    'align_corners': False, 
    'encoder_cfg': {
        'type': 'ResNetILT',
        'depth': 101,
        'outstride': 16,
        'out_indices': (3,),
        'norm_cfg': {'type': 'InPlaceABNSync', 'activation': 'leaky_relu', 'activation_param': 0.01},
        'act_cfg': None,
        'pretrained': True,
    }, 
    'decoder_cfg': {
        'type': 'MIBASPPHead',
        'in_channels': 2048,
        'feats_channels': 256,
        'out_channels': 256,
        'dilations': (1, 6, 12, 18),
        'pooling_size': 32,
        'norm_cfg': {'type': 'InPlaceABNSync', 'activation': 'leaky_relu', 'activation_param': 0.01},
    },
    'losses_cfgs': {
        'segmentation_init': {
            'loss_seg': {'CrossEntropyLoss': {'scale_factor': 1.0, 'reduction': 'mean', 'ignore_index': 255}}
        },
        'segmentation_cl' : {
            'loss_seg': {'MIBUnbiasedCrossEntropyLoss': {'scale_factor': 1.0, 'reduction': 'mean', 'ignore_index': 255}}
        },
        'distillation': {'scale_factor': 100, 'alpha': 1.0},
    },
}
# RUNNER_CFG
RUNNER_CFG = {
    'type': 'MIBRunner',
    'algorithm': 'MIB',
    'task_name': '',
    'task_id': -1,
    'num_tasks': -1,
    'work_dir': '',
    'benchmark': True,
    'save_interval_epochs': 10,
    'eval_interval_epochs': 10,
    'log_interval_iterations': 10,
    'choose_best_segmentor_by_metric': 'mean_iou',
    'logfilepath': '',
    'num_total_classes': -1,
    'random_seed': 42,
    'segmentor_cfg': SEGMENTOR_CFG,
}