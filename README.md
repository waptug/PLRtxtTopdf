# PLRtxtTopdf

A simple python script to convert a nested folder of PLR text articles 
into PDF files and add header information which is injected as the articles are converted into PDf
and create a html index linking to each rendered PDF file.

This script will recursively dig down into all nested folders looking for any file with a .txt or .TXT
file extention and convert it to PDF format. It will skip any files that do not have .txt or .TXT 

As it is parsing each file it will adjust the line length to 
80 charecters long and inject paragraphs. It will insert a blank line between each paragraph.
During the text parsing it will detect the charecter encoding and set it to UTF8 if the file is not in that
format.

As it is building the PDF file it will set the type face to Monospaced Courier font at 12 PX.
It will add a 1 inch header box with a border around it and add 3 lines of text.
Line one is a branding section
Line two is a file name of the source text file that was converted.
Line three is more call to action with a link to the PLRImporter.Com site

During the creation of the PDF files a html index file will be created linking to each generated pdf file for easy viewing.

THe script is interactive to allow a user to specify a source folder containing the txt files and a destination folder to hold the 
rendered PDF files.
The rendered PDF folder will mimic the folder structure of the source folder.

The main purpose of this script it to organize and manage over 200K PLR files and create a open web site to allow access to thises articles.

