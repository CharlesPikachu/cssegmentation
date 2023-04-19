'''mib_r101iabnd16_aspp_512x512_vocaug15-1'''
import os
from .base_cfg import RUNNER_CFG


# modify DATASET_CFG
RUNNER_CFG['DATASET_CFG'].update({
    'type': 'VOCDataset',
    'rootdir': os.path.join(os.getcwd(), 'VOCdevkit/VOC2012'),
    'overlap': False,
})
RUNNER_CFG['DATASET_CFG']['train']['set'] = 'trainaug'
# modify OPTIMIZER_CFGS
RUNNER_CFG['OPTIMIZER_CFGS'] = [{
    'constructor_cfg': {'type': 'DefaultParamsConstructor', 'filter_params': True, 'paramwise_cfg': None},
    'type': 'SGD',
    'momentum': 0.9, 
    'nesterov': True,
    'weight_decay': 1e-4,
} for _ in range(6)]
# modify SCHEDULER_CFGS
RUNNER_CFG['SCHEDULER_CFGS'] = [
    {'type': 'PolyScheduler', 'max_iters': -1, 'max_epochs': 30, 'lr': 0.01, 'min_lr': 0.0, 'power': 0.9},
    {'type': 'PolyScheduler', 'max_iters': -1, 'max_epochs': 30, 'lr': 0.001, 'min_lr': 0.0, 'power': 0.9},
    {'type': 'PolyScheduler', 'max_iters': -1, 'max_epochs': 30, 'lr': 0.001, 'min_lr': 0.0, 'power': 0.9},
    {'type': 'PolyScheduler', 'max_iters': -1, 'max_epochs': 30, 'lr': 0.001, 'min_lr': 0.0, 'power': 0.9},
    {'type': 'PolyScheduler', 'max_iters': -1, 'max_epochs': 30, 'lr': 0.001, 'min_lr': 0.0, 'power': 0.9},
    {'type': 'PolyScheduler', 'max_iters': -1, 'max_epochs': 30, 'lr': 0.001, 'min_lr': 0.0, 'power': 0.9},
]
# modify RUNNER_CFG
RUNNER_CFG.update({
    'task_name': '15-5s',
    'num_tasks': 6,
    'num_total_classes': 21,
    'work_dir': 'mib_r101iabnd16_aspp_512x512_vocaug15-1',
    'logfilepath': 'mib_r101iabnd16_aspp_512x512_vocaug15-1/mib_r101iabnd16_aspp_512x512_vocaug15-1.log',
})