ass := pr2.asm
obj := pr2.obj
exe := pr2.exe

.PHONY: createobj
createobj: $(ass)
	nasm -f win32 $(ass) -o $(obj)

.PHONY: compileexe
compileexe: $(obj)
	golink /entry:Start /console kernel32.dll user32.dll msvcrt.dll $(obj)

.PHONY: comp
comp: createobj compileexe

.PHONY: run
run: $(exe)
	./$(exe)