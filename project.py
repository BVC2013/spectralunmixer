from fluorochrome import flurochrome
from concatFile import concatFile
#main file
# step one, import fluorochromes into directory (files which carry the spectral data for each reagent)
# step two, create the flurochrome class with the filepath
# step three, create the concatFile class with the fluorochromes
fluorochromes = []

for i in '/data/fluorochromes':
    fluorochromes.add(fluorochrome.fluorochrome(i))
    print(i + "succesfully converted.")
concatfile = concatFile(fluorochromes)
print("succesfully produced concatfile")
