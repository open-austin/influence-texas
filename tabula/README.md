Downloaded tabula from here: https://github.com/tabulapdf/tabula-java

Their page contains better documentation.

Here's what I did:

```
# Run tabula as a batch job on all pdfs in ./pdf directory
java -jar ./tabula-1.0.3-jar-with-dependencies.jar -b ./pdf
# Copy outputted csv files in ./pdf directory into the csv directory
mv ./pdf/*.csv ./csv
```

Yay.
