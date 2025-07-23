
# For libpython error:

- Check conda path:
    ```bash
    conda info -e
    ```
- Set LD_LIBRARY_PATH:
    ```bash
    export LD_LIBRARY_PATH=/home/caesar/anaconda3/envs/hvgym/lib:$LD_LIBRARY_PATH
    
    ```

- 确定pkl的动作时长
    ```bash
    python check_motion_duration.py path/to/motion.pkl
    
    ```



## 回旋踢训练
```bash
HYDRA_FULL_ERROR=1 python humanoidverse/train_agent.py \
+simulator=isaacgym \
+exp=motion_tracking \
+domain_rand=NO_domain_rand \
+rewards=motion_tracking/reward_motion_tracking_dm_2real \
+robot=g1/g1_29dof_anneal_23dof \
+terrain=terrain_locomotion_plane \
+obs=motion_tracking/deepmimic_a2c_nolinvel_LARGEnoise_history \
use_wandb=True \
+wandb.wandb_entity=caesar1457-uts \
+wandb.wandb_dir=./wandb_logs \
+checkpoint=logs/MotionTracking/20250723_234215-MotionTracking_CR7-motion_tracking-g1_29dof_anneal_23dof/model_100.pt \
num_envs=128 \
project_name=MotionTracking \
experiment_name=MotionTracking_CR7 \
robot.motion.motion_file="humanoidverse/data/motions/g1_29dof_anneal_23dof/TairanTestbed/singles/0-TairanTestbed_TairanTestbed_CR7_video_CR7_level1_filter_amass.pkl" \
rewards.reward_penalty_curriculum=True \
rewards.reward_penalty_degree=0.00001 \
env.config.resample_motion_when_training=False \
env.config.termination.terminate_when_motion_far=True \
env.config.termination_curriculum.terminate_when_motion_far_curriculum=True \
env.config.termination_curriculum.terminate_when_motion_far_threshold_min=0.3 \
env.config.termination_curriculum.terminate_when_motion_far_curriculum_degree=0.000025 \
robot.asset.self_collisions=1
```
-----

```bash
python humanoidverse/eval_agent.py \
+checkpoint=logs/MotionTracking/20250723_231712-MotionTracking_CR7-motion_tracking-g1_29dof_anneal_23dof/model_200.pt
```
-----

```bash
tensorboard --logdir=runs
```
-----
