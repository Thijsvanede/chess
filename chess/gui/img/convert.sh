for filename in *.svg; do
	inkscape -w 1024 -h 1024 "$filename" -o "${filename/%.svg/.png}"
done
