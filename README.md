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

Text to PDF Converter

This is a Python script that converts all .txt files in a folder and its subfolders to .pdf files. It also creates an index.html file in the destination folder with links to the converted files.
Setup Guide for WSL2

    Install WSL2: First, you need to install WSL2 on your Windows machine. You can follow the official Microsoft guide here.
    Install Python: Once you have WSL2 installed, open a new WSL2 terminal window and install Python. You can do this by running the following commands:

    sudo apt update
    sudo apt install python3 python3-pip

    Install Required Python Libraries: The script requires several Python libraries. You can install them using pip:

    pip3 install chardet textwrap reportlab tqdm

    Create a New Python Script: Now, you can create a new Python script in your preferred directory. You can use a text editor like nano to create and edit the file:

    nano txt2pdf.py

    Then, copy and paste the provided Python script into the nano editor. Save and exit by pressing Ctrl+X, then Y to confirm saving changes, and finally Enter to confirm the file name.
    Run the Script: You can now run the script using Python:

    python3 txt2pdf.py

    The script will prompt you to enter the path to the source folder and the destination folder. These paths should be relative to the WSL2 filesystem. For example, if you have a folder named txt_files in your Windows Documents folder, the path would be /mnt/c/Users/YourUsername/Documents/txt_files.
    Remember, Linux is case-sensitive, so be sure to enter the paths correctly. Also, spaces in directory or file names should be preceded by a backslash (\). For example, a folder named My Documents should be entered as My\ Documents.

That's it! The script should now convert all .txt files in the source folder and its subfolders to .pdf files and create an index.html file in the destination folder with links to the converted files.