build:
	mkdir bin
	clang -F /System/Library/PrivateFrameworks -framework login -o bin/lockscreen src/main.c
	cp src/lockscreend bin/lockscreend