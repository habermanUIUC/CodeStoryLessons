wget 'https://raw.githubusercontent.com/NSF-EC/INFO490Assets/master/src/datasets/hamlet/pg2265.txt' -O 1.txt
wget 'http://www.gutenberg.org/cache/epub/2265/pg2265.txt' -O 2.txt

md5sum will be differnt from stream before file write
you can see the 0x0a0d and 0x0a diffeernces
between hexdumps of before and after writing to file
