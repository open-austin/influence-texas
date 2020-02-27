import os
import sys
import subprocess

tabula_path = os.getcwd() + "/" + sys.argv[1]
tablua_path = tabula_path.replace(" ", "\\ ")
walk_dir = sys.argv[2]

if not tabula_path:
    print ("Usage {sys.argv[0]} $TABULA_JAR_PATH $DIRECTORY_TO_WALK")
    print("You may need to use the relative path to Tabula since" \
        + "this script expects that the tabula.jar is in its current directory ")
#print('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('Processing ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):
    #print('--\nroot = ' + root)
    list_file_path = os.path.join(root, 'my-directory-list.txt')
    #print('list_file_path = ' + list_file_path)

    with open(list_file_path, 'wb') as list_file:
        #for subdir in subdirs:
            #print('\t- subdirectory ' + subdir)

        for index, filename in enumerate(files):
            file_path = os.path.join(root, filename)
            print(f"Trying to process {file_path}")

            filename, extension = os.path.splitext(file_path)
            if extension == ".pdf":
                out_filename = filename + ".csv"
                if not os.path.exists(out_filename):
                    out_filename = filename + ".csv"
                    command = f"java -jar {tabula_path}"
                        
                    #without the -p arg, tabula only does the first page
                    # -o is for output file
                    args =  "java " + "-jar " + tabula_path + " " \
                         + "-p all " \
                         + filename.replace(" ", "\\ ") + ".pdf " \
                         + " -o "+ filename.replace(" ", "\\ ") +  ".csv "
                    try:
                        subprocess.check_output(args,shell = True)
                        print("Successfully Created " + filename.replace(" ", "\\ ") +  ".csv ")
                    except subprocess.CalledProcessError as e:
                        print("ERROR: ")
                        print(e)
                else:
                    print(filename + ".csv" + " already exists, skipping")
            else:
                print("Not a PDF, skipping")
