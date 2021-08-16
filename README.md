# Deobfuscation: recovering an OLLVM-protected program
**Note: This is a Translated Version of the original text over here: [https://github.com/cq674350529/deflat](https://github.com/cq674350529/deflat) with additional information of this specific fork**

## Flat_control_flow

### Description

Based on the [deflat](https://github.com/SnowGirls/deflat) of `SnowGirls`, the [angr](https://github.com/angr/angr) framework is used to achieve the removal of control flow flattening. For details, please Refer to [Using symbolic execution to remove control flow flattening](https://security.tencent.com/index.php/blog/msg/112).

> The script only depends on the `angr` framework, the version of `angr` used in the test is `8.19.4.5`

### Usage

> `0x400530` is the address of the function `check_password()`.

```shell
(angr-dev) <path>/deflat/flat_control_flow$ python3 deflat.py -f samples/bin/check_passwd_x8664_flat --addr 0x400530
*******************relevant blocks************************
prologue: 0x400530
main_dispatcher: 0x400554
pre_dispatcher: 0x40099b
retn: 0x40098f
relevant_blocks: ['0x40086a', '0x40080d', '0x4008ee', '0x40094f', '0x40084e', '0x400819', '0x400886', '0x40095b', '0x4007ec', '0x40092e', '0x4008a8cc', '0x4008a8' , '0x40091b', '0x40097c', '0x400837']
*******************symbolic execution*********************
-------------------dse 0x40086a---------------------
-------------------dse 0x40080d---------------------
-------------------dse 0x4008ee---------------------
-------------------dse 0x40094f---------------------
-------------------dse 0x40084e---------------------
-------------------dse 0x400819---------------------
-------------------dse 0x400886---------------------
-------------------dse 0x40095b---------------------
-------------------dse 0x4007ec---------------------
-------------------dse 0x40092e---------------------
-------------------dse 0x4008a9---------------------
-------------------dse 0x4008cc---------------------
-------------------dse 0x40091b---------------------
-------------------dse 0x40097c---------------------
-------------------dse 0x400837---------------------
-------------------dse 0x400530---------------------
************************flow************************* *****
0x40084e: ['0x40086a', '0x40095b']
0x40086a: ['0x400886', '0x40094f']
0x400530: ['0x4007ec']
0x4008a9: ['0x4008cc', '0x40094f']
0x400886: ['0x4008a9', '0x40094f']
0x4007ec: ['0x400819', '0x40080d']
0x40091b: ['0x40098f']
0x40080d: ['0x40084e']
0x40092e: ['0x40094f']
0x4008ee: ['0x40091b', '0x40092e']
0x400819: ['0x400837']
0x40094f: ['0x40097c']
0x40095b: ['0x40097c']
0x40097c: ['0x40098f']
0x400837: ['0x4007ec']
0x4008cc: ['0x4008ee', '0x40094f']
0x40098f: []
************************patch************************* ****
Successful! The recovered file: check_passwd_flat_recovered
```

## Bogus_control_flow

### Description

Use [angr](https://github.com/angr/angr) framework to remove false control flow. For details, please refer to [Deobfuscation: recovering an OLLVM-protected program](https://blog.quarkslab.com/deobfuscation -recovering-an-ollvm-protected-program.html).

The main idea of ​​the original text is to "simplify" the constraints when performing symbolic execution. By replacing `x * (x + 1)% 2 `with `0`, so that `(y <10 || x * (x + 1)% 2 == 0)` Constantly established, so as to obtain the correct basic block and avoid endless loops.

When using the [angr](https://github.com/angr/angr) framework to solve this problem, you can also follow the above ideas. Another idea is to directly set the value of `x` or `y` to `0`, which can also make the above constraints always hold. Under the default conditions, the values ​​of `x` and `y` will be initialized to 0, so there is no need to set them manually. In other words, you can directly use symbolic execution to solve the problem without encountering the problem of infinite loops.

Through symbolic execution, after obtaining all the executed basic blocks, you can use `patch` to remove redundant basic blocks.

> After simplifying the control flow, check the pseudo code through `F5`, which is basically the same as the source code. In addition, the control flow can be further simplified on this basis, such as removing redundant instructions.

### Usage

> `0x080483e0` is the address of the function `target_function()`.

```shell
(angr-dev) <path>/deflat/bogus_control_flow$ python3 debogus.py -f samples/bin/target_x86_bogus --addr 0x80483e0
*******************symbolic execution*********************
executed blocks: ['0x8048686', '0x804868b', '0x8048991', '0x8048592', '0x8048914', '0x8048715', '0x8048897', '0x8048720', '0x8048725', '0x80484ab', '0x804862ce', '0x804804842ce ', '0x80484b6', '0x80484bb', '0x80487bb', '0x80487c0', '0x80486c7', '0x8048950', '0x8048551', '0x80488d3', '0x8048955', '0x8048556', '0x8048489d8', '0 '0x80488d8', '0x804885b', '0x80483e0', '0x80485e0', '0x8048761', '0x80485eb', '0x80485f0', '0x80484f7', '0x80487fc']
************************patch************************* *****
Successful! The recovered file: ./target_bogus_recovered
```

## Description

### Supported Arch

Currently, the script is only tested on programs with the following architectures:

+ `x86` series: `x86`, `x86_64`
+ `arm` series: `arm`(`armv7`), `arm64/aarch64`(`armv8`)

### Misc

#### `am_graph.py`
The `am_graph.py` script is from [angr-management/utils/graph.py](https://github.com/angr/angr-management/blob/master/angrmanagement/utils/graph.py), used to `CFG` is converted to `supergraph`, because `CFG` in `angr` framework is not the same as that in `IDA`.

> A super transition graph is a graph that looks like IDA Pro's CFG, where calls to returning functions do not terminate basic blocks.

Usually when installing `angr`, `angr-managerment` (GUI of `angr`) is not installed, so here directly put [angr-management/utils/graph.py](https://github.com/angr /angr-management/blob/master/angrmanagement/utils/graph.py) to the current directory and rename it to `am_graph.py`.

#### `multi.py`
This script allows user to deobfuscate multiple functions in one single run provided all the addresses. 
For usage of the script type `python3 multi.py -h`

## Requirements

-`python3`
-`angr`
-`python-magic`

## Reference

+ [deflat](https://github.com/SnowGirls/deflat)
+ [Use symbolic execution to remove control flow flattening](https://security.tencent.com/index.php/blog/msg/112)
+ [Deobfuscation: recovering an OLLVM-protected program](https://blog.quarkslab.com/deobfuscation-recovering-an-ollvm-protected-program.html)
+ [obfuscator-llvm wiki](https://github.com/obfuscator-llvm/obfuscator/wiki)
