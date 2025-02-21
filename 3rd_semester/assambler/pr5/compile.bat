@set file="2.1"
@set toolchain=C:\SysGCC\risc-v\bin\riscv64-unknown-elf

@%toolchain%-as.exe -o %file%.o %file%.s
@%toolchain%-ld.exe -o %file%.elf -Ttext 0x80000000 %file%.o
@%toolchain%-objcopy.exe -O binary %file%.elf %file%.img

@if exist %file%.o del %file%.o
@if exist %file%.elf del %file%.elf

@pause 0