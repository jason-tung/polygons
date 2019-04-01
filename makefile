
run: main.py display.py draw.py matrix.py parser.py
	python main.py

alt:
	python alt.py

gif:
	python gif.py

clean:
	rm -f *.pyc
	rm -f *~
	rm -f *.png
	rm -f *.gif
