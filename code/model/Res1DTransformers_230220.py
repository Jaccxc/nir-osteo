import tensorflow as tf
from tensorflow.keras import layers
from components import resBlock

class Res1D_Transformer_230220(tf.keras.Model):
    def __init__(self, input_shape, num_classes, num_data_points):
        super(Res1D_Transformer_230220, self).__init__()

        self.num_data_points = num_data_points

        #ResNet for Branch1
        self.branch1_res1_b1 = resBlock.SingleResBlock(((64, 1),(64, 3),(256, 1)), 'branch1_res1_b1')
        self.branch1_res1_b2 = resBlock.SingleResBlock(((64, 1),(64, 3),(256, 1)), 'branch1_res1_b2')

        self.branch1_res2_b1 = resBlock.SingleResBlock(((128, 1),(128, 3),(512, 1)), 'branch1_res2_b1')
        self.branch1_res2_b2 = resBlock.SingleResBlock(((128, 1),(128, 3),(512, 1)), 'branch1_res2_b2')
        self.branch1_res2_b3 = resBlock.SingleResBlock(((128, 1),(128, 3),(512, 1)), 'branch1_res2_b3')

        self.branch1_res3_b1 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch1_res3_b1')
        self.branch1_res3_b2 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch1_res3_b2')
        self.branch1_res3_b3 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch1_res3_b3')
        self.branch1_res3_b4 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch1_res3_b4')

        self.branch1_res4_b1 = resBlock.SingleResBlock(((512, 1),(512, 3),(2048, 1)), 'branch1_res4_b1')
        self.branch1_res4_b2 = resBlock.SingleResBlock(((512, 1),(512, 3),(2048, 1)), 'branch1_res4_b2')

        #ResNet for Branch2
        self.branch2_res1_b1 = resBlock.SingleResBlock(((64, 1),(64, 3),(256, 1)), 'branch2_res1_b1')
        self.branch2_res1_b2 = resBlock.SingleResBlock(((64, 1),(64, 3),(256, 1)), 'branch2_res1_b2')

        self.branch2_res2_b1 = resBlock.SingleResBlock(((128, 1),(128, 3),(512, 1)), 'branch2_res2_b1')
        self.branch2_res2_b2 = resBlock.SingleResBlock(((128, 1),(128, 3),(512, 1)), 'branch2_res2_b2')
        self.branch2_res2_b3 = resBlock.SingleResBlock(((128, 1),(128, 3),(512, 1)), 'branch2_res2_b3')

        self.branch2_res3_b1 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch2_res3_b1')
        self.branch2_res3_b2 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch2_res3_b2')
        self.branch2_res3_b3 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch2_res3_b3')
        self.branch2_res3_b4 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch2_res3_b4')

        self.branch2_res4_b1 = resBlock.SingleResBlock(((512, 1),(512, 3),(2048, 1)), 'branch2_res4_b1')
        self.branch2_res4_b2 = resBlock.SingleResBlock(((512, 1),(512, 3),(2048, 1)), 'branch2_res4_b2')

        #ResNet for Branch3
        self.branch3_res1_b1 = resBlock.SingleResBlock(((64, 1),(64, 3),(256, 1)), 'branch3_res1_b1')
        self.branch3_res1_b2 = resBlock.SingleResBlock(((64, 1),(64, 3),(256, 1)), 'branch3_res1_b2')

        self.branch3_res2_b1 = resBlock.SingleResBlock(((128, 1),(128, 3),(512, 1)), 'branch3_res2_b1')
        self.branch3_res2_b2 = resBlock.SingleResBlock(((128, 1),(128, 3),(512, 1)), 'branch3_res2_b2')
        self.branch3_res2_b3 = resBlock.SingleResBlock(((128, 1),(128, 3),(512, 1)), 'branch3_res2_b3')

        self.branch3_res3_b1 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch3_res3_b1')
        self.branch3_res3_b2 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch3_res3_b2')
        self.branch3_res3_b3 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch3_res3_b3')
        self.branch3_res3_b4 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch3_res3_b4')

        self.branch3_res4_b1 = resBlock.SingleResBlock(((512, 1),(512, 3),(2048, 1)), 'branch3_res4_b1')
        self.branch3_res4_b2 = resBlock.SingleResBlock(((512, 1),(512, 3),(2048, 1)), 'branch3_res4_b2')

        #ResNet for Branch4
        self.branch4_res1_b1 = resBlock.SingleResBlock(((64, 1),(64, 3),(256, 1)), 'branch4_res1_b1')
        self.branch4_res1_b2 = resBlock.SingleResBlock(((64, 1),(64, 3),(256, 1)), 'branch4_res1_b2')

        self.branch4_res2_b1 = resBlock.SingleResBlock(((128, 1),(128, 3),(512, 1)), 'branch4_res2_b1')
        self.branch4_res2_b2 = resBlock.SingleResBlock(((128, 1),(128, 3),(512, 1)), 'branch4_res2_b2')
        self.branch4_res2_b3 = resBlock.SingleResBlock(((128, 1),(128, 3),(512, 1)), 'branch4_res2_b3')

        self.branch4_res3_b1 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch4_res3_b1')
        self.branch4_res3_b2 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch4_res3_b2')
        self.branch4_res3_b3 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch4_res3_b3')
        self.branch4_res3_b4 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch4_res3_b4')

        self.branch4_res4_b1 = resBlock.SingleResBlock(((512, 1),(512, 3),(2048, 1)), 'branch5_res4_b1')
        self.branch4_res4_b2 = resBlock.SingleResBlock(((512, 1),(512, 3),(2048, 1)), 'branch5_res4_b2')

        #ResNet for Branch5
        self.branch5_res1_b1 = resBlock.SingleResBlock(((64, 1),(64, 3),(256, 1)), 'branch5_res1_b1')
        self.branch5_res1_b2 = resBlock.SingleResBlock(((64, 1),(64, 3),(256, 1)), 'branch5_res1_b2')

        self.branch5_res2_b1 = resBlock.SingleResBlock(((128, 1),(128, 3),(512, 1)), 'branch5_res2_b1')
        self.branch5_res2_b2 = resBlock.SingleResBlock(((128, 1),(128, 3),(512, 1)), 'branch5_res2_b2')
        self.branch5_res2_b3 = resBlock.SingleResBlock(((128, 1),(128, 3),(512, 1)), 'branch5_res2_b3')

        self.branch5_res3_b1 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch5_res3_b1')
        self.branch5_res3_b2 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch5_res3_b2')
        self.branch5_res3_b3 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch5_res3_b3')
        self.branch5_res3_b4 = resBlock.SingleResBlock(((256, 1),(256, 3),(1024, 1)), 'branch5_res3_b4')

        self.branch5_res4_b1 = resBlock.SingleResBlock(((512, 1),(512, 3),(2048, 1)), 'branch5_res4_b1')
        self.branch5_res4_b2 = resBlock.SingleResBlock(((512, 1),(512, 3),(2048, 1)), 'branch5_res4_b2')
        
        self.merge_branch = layers.Add(name='merge_branch')
        
        self.transformer = layers.Transformer(d_model=128, num_heads=4, dropout=0.1)

        self.dense = layers.Dense(units=1, activation='linear')
    
    def call(self, inputs):
        # 1D convolution layers
        x0 = self.branch1_res1_b1(inputs[0])
        x1 = self.branch2_res1_b1(inputs[1])
        x2 = self.branch3_res1_b1(inputs[2])
        x3 = self.branch4_res1_b1(inputs[3])
        x4 = self.branch5_res1_b1(inputs[4])

        x0 = self.branch1_res1_b1(x0)
        x0 = self.branch1_res1_b2(x0)
        x0 = self.branch1_res2_b1(x0)
        x0 = self.branch1_res2_b2(x0)
        x0 = self.branch1_res2_b3(x0)
        x0 = self.branch1_res3_b1(x0)
        x0 = self.branch1_res3_b2(x0)
        x0 = self.branch1_res3_b3(x0)
        x0 = self.branch1_res3_b4(x0)
        x0 = self.branch1_res4_b1(x0)
        x0 = self.branch1_res4_b2(x0)

        x1 = self.branch2_res1_b1(x1)
        x1 = self.branch2_res1_b2(x1)
        x1 = self.branch2_res2_b1(x1)
        x1 = self.branch2_res2_b2(x1)
        x1 = self.branch2_res2_b3(x1)
        x1 = self.branch2_res3_b1(x1)
        x1 = self.branch2_res3_b2(x1)
        x1 = self.branch2_res3_b3(x1)
        x1 = self.branch2_res3_b4(x1)
        x1 = self.branch2_res4_b1(x1)
        x1 = self.branch2_res4_b2(x1)

        x2 = self.branch3_res1_b1(x2)
        x2 = self.branch3_res1_b2(x2)
        x2 = self.branch3_res2_b1(x2)
        x2 = self.branch3_res2_b2(x2)
        x2 = self.branch3_res2_b3(x2)
        x2 = self.branch3_res3_b1(x2)
        x2 = self.branch3_res3_b2(x2)
        x2 = self.branch3_res3_b3(x2)
        x2 = self.branch3_res3_b4(x2)
        x2 = self.branch3_res4_b1(x2)
        x2 = self.branch3_res4_b2(x2)

        x3 = self.branch4_res1_b1(x3)
        x3 = self.branch4_res1_b2(x3)
        x3 = self.branch4_res2_b1(x3)
        x3 = self.branch4_res2_b2(x3)
        x3 = self.branch4_res2_b3(x3)
        x3 = self.branch4_res3_b1(x3)
        x3 = self.branch4_res3_b2(x3)
        x3 = self.branch4_res3_b3(x3)
        x3 = self.branch4_res3_b4(x3)
        x3 = self.branch4_res4_b1(x3)
        x3 = self.branch4_res4_b2(x3)

        x4 = self.branch5_res1_b1(x4)
        x4 = self.branch5_res1_b2(x4)
        x4 = self.branch5_res2_b1(x4)
        x4 = self.branch5_res2_b2(x4)
        x4 = self.branch5_res2_b3(x4)
        x4 = self.branch5_res3_b1(x4)
        x4 = self.branch5_res3_b2(x4)
        x4 = self.branch5_res3_b3(x4)
        x4 = self.branch5_res3_b4(x4)
        x4 = self.branch5_res4_b1(x4)
        x4 = self.branch5_res4_b2(x4)

        concat = self.merge_branch([x0, x1, x2, x3, x4])
        
        # Transformer layers
        x_t = self.transformer(concat)
    
        # Dense layer
        outputs = self.dense(x_t)

        return outputs
