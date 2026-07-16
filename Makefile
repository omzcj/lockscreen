build:
	mkdir -p bin
	clang -F /System/Library/PrivateFrameworks -framework login -o bin/lockscreen src/main.c
