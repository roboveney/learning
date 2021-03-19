Christina Veney 10845635
Yes, submitting as graded project
Python3
Linux

Code Structure:
Regardless of the mode if the input filename given does not exist then a blank board will be used.
1) Interactive
  The interactive code is set up to determine first whether the next player is going to be the computer or human based on the provided arguments. The next player value(1or2) given in the txt file is set as the name given in argument 3 (computer-next/human-next). At the begining of either turn the board is checked to see if it is full. If so the score is calculated and Game Over is printed to the terminal.
  During the computers turn it uses minimax function to pick its move. The minimax function performs alpha beta pruning and orders the successor lists based on max or min value depending on if it is currently in a max or min loop. Scoring is done using 2d convolutions across the game board. During the minimax function the heuristics for the score are that a all 4 or greater connections give 1000pts, connected 3s or split connections give 100pts and connected 2s give 10pts. The max players score is subtracted from the minplayers score to give the total evaluation. After the move is selected and made the current board is printed to the screen and saved to the computer.txt file then it switches to the human player.
  During the human's turn they are prompted to pick a value between 1 and 7 that value is shifted to be 0 indexed. If the input is between 1-7 and the move legal then it is made. The new board is saved in human.txt and printed to the screen.
  The game ends once the board is full and the total scores are calculated based off the number of connected 4's.

2) One-Move
  During this mode the board and next player are extracted from the input file. A move is calculated using the minimax function where the provided next player is the maximizer. The move is then made the board is saved in the provided outfile and also printed to screen.

Lastly the overal algorithm was assessed by playing the interactive mode where the "human" player randomly selected from the available legal moves. The algorithm was shown to be consistently win every game from a depth of 3 to 6 with games of depth 6 taking about 15sec.  

How to Run:
1) unzip the folder where ever desired
2) Move desired input files to same location or use full location in arguments
3) In terminal cd to file location and run the below command
	$chmod +x maxconnect4
	Note: The helper functions script uses scipy.signal for the 2dconvolutions if not already downloaded also run pip install scipy
4) Use the following arguments depending on mode. 
	Interactive:
	$python3 maxconnect4 interactive [input_file] [computer-next/human-next] [depth]

	One-Move:
	$python3 maxconnect4.py one-move [input_file] [output_file] [depth]

