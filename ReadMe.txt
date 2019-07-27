Version Check Tool:

Introduction:
Version Check Tool compares two revision's (or) a revision against it's “Master Manifest Config File”. This master manifest file should be a JSON file which has list of all the packages and contents listed. In future we will add or remove sections when the package contents change.
This tool, accepts config file (or) two revision versions and report any mismatch into a excel output file.

Input:
1) Two release number (or)
2) One release number and respective Master-Manifest Config.JSON file.

--help					-h					Show this help message and exit
--verbose,				-v					Increase output verbosity [0-Quite mode, Default/1-Only required, 2-Few execution stmts, 3-Debug mode]
--username <USERNAME>,	-u USERNAME			Your quicklook user id
--password PASSWORD,	-p PASSWORD			Password for authentication of distribution server
--primaryRelease,		-r1 PRIMARYRELEASE	Primary release number as rXXXXX
--secondaryRelease,		-r2 2nd RELEASE		If you want to compare Release-to-Release
--primaryDirectory,		-d1 PRIMARYDIR		Directory Primary release number
--secondaryDirectory, 	-d2 SECONDARYDIR	Directory Secondary realease number, if you want to compare Release-to-Release
--file FILE,			-f FILE				If you want to compare Release-to-MasterFile

Example Run:  ./versionCheckTool.py -u cg186034 -r1 r50905 -d2 r54363
In the above example,
./versionCheckTool.py	: File name
-u cg186034		: UserName
-r1 r50905		: Primary release no WITH prefix "r"
-d2 r54363		: Secondary release no WITH prefix "r"
Note:
1) When prompted, please enter respective password for authentication.
2) We are using -d2, as all the files are saved under that folder before hand.

Scenario- 1
Example:
Input: rXXXXX
Release no- 1: r48130
Release no- 2: r53816
Check the comparison output (.csv file) and logs under Output folder.

Scenario- 2 Process:
Read release number and respective Master-Manifest Config.JSON file.
Example:
Input:
1) Release no- 1: r53816
2) File name    : Aster Release AC6.21.json
Check the comparison output (.csv file) and logs under Output folder.

Compare File-information from both Inputs.
Note- diff, similarities, new / missing files and print the output into an excel sheet.

Output (.csv) file contains:
	Common files in both releases
	Unique files of particular release, with 'release NAME as TITLE'
	Compare size & MD5 of each common file inside release respectively (of it's file name).
	Total number of files remain the same /modified for each platform (with size & MD5sum)
	ZERO file or ZERO folder size(s)
