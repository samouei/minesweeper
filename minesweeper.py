#!/usr/bin/env python3



def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)


# 2-D IMPLEMENTATION


def initialize_2d_board(num_rows, num_cols):
    """
    Initializes a 2D board with 0s.

    Parameters:
       num_rows (int): number of rows
       num_cols (int): number of columns
    
    Returns: a 2D board of size num_rows * num_cols
    """

    return [[0 for c in range(num_cols)] for r in range(num_rows)]


def initialize_2d_mask(num_rows, num_cols):
    """
    Initializes mask with False values.

    Parameters:
       num_rows (int): number of rows
       num_cols (int): number of columns

    Returns: a 2D mask of size num_rows * num_cols
    """

    return [[False for c in range(num_cols)] for r in range(num_rows)]


def get_all_cells_2d(num_rows, num_cols):
    """
    Makes a set with all inbound (r, c) values in a 
        num_rows * num_cols sized board

    Parameters:
       num_rows (int): number of rows
       num_cols (int): number of columns
      
    Returns: a set of all the valid cell cooridnate tuples    
    """    
    
    inbound_cells = set()
    for r in range(num_rows):
        for c in range(num_cols):
            inbound_cells.add((r, c))
    return inbound_cells
            

def get_neighbors_2d(num_rows, num_cols, cell):
    """    
    Gets a bomb's set of neighbors {(r,c), (r,c)}.

    Parameters:
       num_rows (int): number of rows
       num_cols (int): number of columns
       cell (tuple): cell coordinates
    
    Returns: a set with bomb neighbors as tuples. 
    """
        
    row = cell[0]
    col = cell[1]
    
    inbound_cells = get_all_cells_2d(num_rows, num_cols)

    neighbors = {(row - 1, col -1), (row - 1, col), (row - 1, col + 1),
                 (row, col - 1), (row, col + 1),
                 (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)}
    
    cell_neighbors = set()
    for n in neighbors:
        if n in inbound_cells:
            cell_neighbors.add(n)
            
    return cell_neighbors


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, False, False, False]
        [False, False, False, False]
    state: ongoing
    """

    return new_game_nd((num_rows, num_cols), bombs)  


############ Code Prior to Making new_game_nd ############
    

#    board = initialize_2d_board(num_rows, num_cols)    
#    mask = initialize_2d_mask(num_rows, num_cols)
#    
#    
#    for b in bombs:
#
#        bomb_neighbors = get_neighbors_2d(num_rows, num_cols, b)
#        for n in bomb_neighbors: 
#            neighbor_row, neighbor_col = n
#            board[neighbor_row][neighbor_col] += 1
#
#    
#    for r, c in bombs: # ?2?
#        board[r][c] = "."
#        
#    return {
#        'dimensions': (num_rows, num_cols),
#        'board' : board,
#        'mask' : mask,
#        'state': 'ongoing'}



           
############ Issues in The Original Code ############
 
#*#*#*# 1. if [r,c] in bombs or (r,c) in bombs #*#*#*#  
#*#*#*# 2. refactor: create mask WITH board #*#*#*# 
#*#*#*# 3. refactor: no helper function for getting inbound neighbors #*#*#*#   
       
#####################################################
    
    
def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['mask'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is visible on the board after digging (i.e. game['mask'][bomb_location] ==
    True), 'victory' when all safe squares (squares that do not contain a bomb)
    and no bombs are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    mask:
        [False, True, True, True]
        [False, False, True, True]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    mask:
        [True, True, False, False]
        [False, False, False, False]
    state: defeat
    """

    return dig_nd(game, (row, col))


############ Code Prior to Making dig_nd ############


#    board_rows = game['dimensions'][0]
#    board_cols = game['dimensions'][1]
#    
#    # If game is over or won or cell has been revealed already do nothing
#    if game['state'] == 'defeat' or game['state'] == 'victory' or game['mask'][row][col]: 
#        return 0
#
#    game['mask'][row][col] = True
#    revealed = 1
#    
#    # Base Case: If cell has a value other that zero (number or bomb)
#    if game['board'][row][col] == '.': 
#        game['state'] = 'defeat'
#        return revealed
#    
#    # Iterative Case: If cell has a value zero
#    if game['board'][row][col] == 0:
#        neighbors = get_neighbors_2d(board_rows, board_cols, (row, col))
#        for n in neighbors:
#            revealed += dig_2d(game, n[0], n[1]) 
#    
#    # Check for victory
#    uncovered_cells = 0  
#    num_bombs = 0     
#    for r in range(board_rows):
#        for c in range(board_cols):
#            if game['board'][r][c] == '.':
#                num_bombs += 1
#            if game['board'][r][c] != '.' and game['mask'][r][c]:
#                uncovered_cells += 1
#                
#    if uncovered_cells == (board_rows ) * (board_cols) - num_bombs:
#        game['state'] = 'victory'
#
# 
#    return revealed
            


                                   
############ Issues in The Original Code ############

#*#*#*# 1. refactor: unnecessary #*#*#*#  
        
#    if game['state'] == 'defeat' or game['state'] == 'victory':
#        game['state'] = game['state']  # This is unnecessary!  
#        return 0
    
#*#*#*# 2. missing code: didn't check if game['mask'][row][col] #*#*#*#  
#*#*#*# 3. refactor: no helper function for getting inbound neighbors #*#*#*#  
#*#*#*# 4. refactor: unnecessary code for checking for victory  #*#*#*#  
       
#####################################################


def render_2d(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring bombs).
    game['mask'] indicates which squares should be visible.  If xray is True (the
    default is False), game['mask'] is ignored and all cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A 2D array (list of lists)

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """

    return render_nd(game, xray)


############ Code Prior to Making render_nd ############
    
#    render = game['board'][:]
#    
#    for r in range(game['dimensions'][0]):
#        for c in range(game['dimensions'][1]):
#            if xray:
#                render[r][c] = game['board'][r][c]
#            
#            if game['mask'][r][c] == False and not xray:
#                render[r][c] = '_'   
#            else:
#                if game['board'][r][c] == 0 and game['mask'][r][c] == True:
#                    render[r][c] = ' '
#
#                    
#            # Convert to string
#            render[r][c] = str(render[r][c])
#    return render
            
    
def render_ascii(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function 'render_2d(game)'.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A string-based representation of game

    >>> print(render_ascii({'dimensions': (2, 4),
    ...                     'state': 'ongoing',
    ...                     'board': [['.', 3, 1, 0],
    ...                               ['.', '.', 1, 0]],
    ...                     'mask':  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """

    render = render_2d(game, xray)
        
    render_ascii = ""
    for r in range(game['dimensions'][0]):
        for c in range(game['dimensions'][1]):
            
            # Add space for 0s
            if render[r][c] == '0':
                render[r][c] = " "
                
            render_ascii += render[r][c]
   
            # Separate rows
            if c + 1 == game['dimensions'][1]:
                render_ascii += "\n"
    return render_ascii[:-1]
    
    
# N-D IMPLEMENTATION

def initialize_tensor_board(dimensions, value):
    """
    Initializes board with 0s.

    Parameters:
       dimensions (tuple): dimensions of the board
    
    Returns: an nD board

    """
    
    # Base case
    if len(dimensions) == 1: 
        return [value for i in range(dimensions[0])]
    
    # Iterative case
    return [initialize_tensor_board(dimensions[1:], value) for j in range(dimensions[0])]


def get_neighbors_tensor(dimensions, cell):
    """    
    Gets all of the cell's neighbors in an nD board.
    
    Parameters:
       dimensions (tuple): dimensions of the board  
       cell (tuple): cell coordinates
    
    Returns: a list of the cell's neighbors
    """
    
    # Base Case (1D board)
    if len(dimensions) == 1:
        l = []
        for i in range(-1, 2):
            c = cell[0] + i
            
            # Keep inbound neighbors
            if 0 <= c < dimensions[0]:
                l.append((c,))
        return l
    
    # Iterative Case
    else:
        l2 = get_neighbors_tensor(dimensions[1:], cell[1:])
        l3 = []
        for i in range(-1, 2):
            c = cell[0] + i
            if 0 <= c < dimensions[0]:
                for i in l2:
                    l3.append((c,) + i)
        return l3
    


def update_cell_value_tensor(board, cell, value):
    """    
    Updates a cell's value. Possible update values are =+ 1, '.', and True.

    Parameters:
       board (list): baord of cell values  
       cell (tuple): cell coordinates 
       value: 'bomb', True, or 1
    
    Returns: nothing
    """

    # Base case:

    # Updates game['board']
    if len(cell) == 1:
        if value == 'bomb':
            board[cell[0]] = '.'
        
        # Updates game['mask']
        elif value is True:
            board[cell[0]] = True
        
        # Updates game['board']
        elif value == 1:
            board[cell[0]] += 1
            
        
    # Recursive Case
    else:   
        update_cell_value_tensor(board[cell[0]], cell[1:], value) 


def update_render_value_tensor(board, cell, value):
    """    
    Updates the render board value. Possible values are ' ', '_', or the original cell value.

    Parameters:
       board (list): board of cell values    
       cell (tuple): cell coordinates 
       value: ' ', '_', or the original cell value
    
    Returns: nothing
    """   
    
    # Base case:     
    if len(cell) == 1:
        if value == 0:
            board[cell[0]] = " " 
        elif value == "_":
            board[cell[0]] = "_"
        else:
            board[cell[0]] = str(value)
            
    # Recursive Case
    else:   
        update_render_value_tensor(board[cell[0]], cell[1:], value) 
     
        
def get_cell_value_tensor(board, cell):
    """    
    Gets a cell's value from an nD board recursively. 

    Parameters:
       board (list): board of cell values    
       cell (tuple): cell coordinates 
       
    Returns: cell value
    """

    # Base case:
    if len(cell) == 1:
        return board[cell[0]]
    
    # Recursive Case
    else:   
        return get_cell_value_tensor(board[cell[0]], cell[1:])    
        
        
def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of lists, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: ongoing
    """
    
    # Make mask (all False) and board (all 0)
    board = initialize_tensor_board(dimensions, 0)
    mask = initialize_tensor_board(dimensions, False)

    # For each bomb get its neighbors
    for b in bombs:
        bomb_neighbors = get_neighbors_tensor(dimensions, b)  
        
        # Update bomb's neighbor values
        for n in bomb_neighbors: 
            update_cell_value_tensor(board, n, 1)
    
    # Update board with "." for all bombs
    for i in bombs: 
        update_cell_value_tensor(board, i, 'bomb')
        
    return {
        'dimensions': dimensions,
        'board' : board,
        'mask' : mask,
        'state': 'ongoing'}    
    
    
def get_all_cells_tensor(dimensions, board):
    """
    Gets all cell values of an nD board recursively.
    
    Parameters:
       dimensions (tuple): dimensions of the board  
       board (list): board of cell values   
       
    Returns: a set with all cell coordinates
    """    
    
    # Base Cases:
    if len(dimensions) == 0:
        return set()
    
    if len(dimensions) == 1:
        return {(i,) for i in range(dimensions[0])}
    
    # Recursive Case
    all_cells = set()
    recursive_set = get_all_cells_tensor(dimensions[1:], board[1:])
    for i in recursive_set:
        for j in range(dimensions[0]):
            all_cells.add((j,) + i)
            
    return all_cells
        

def is_won(board, mask, cell_locs):
    """
    Checks if the game is won.

    Parameters:
       board (list): board of cell values 
       mask (list): board of cell visibility values
       cell_locs (set): all cell coordinates
       
    Returns: True or False
    """
    
    num_cells = 0
    num_bombs = 0  
    uncovered_cells = 0  
    
    # Get total number of cells, cell values, and uncovered cells
    for c in cell_locs:
        num_cells += 1
        cell_value = get_cell_value_tensor(board, c)
        cell_mask = get_cell_value_tensor(mask, c)
        
        if cell_value != '.' and not cell_mask:
            break
        if cell_value == '.':
            num_bombs += 1   
        if cell_value != '.' and cell_mask:
            uncovered_cells += 1  
            
    # Check for victory
    if uncovered_cells == num_cells - num_bombs:
        return True  
    return False      
        

def dig_nd(game, coordinates, cell_locs = None):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the mask to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    mask:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    state: defeat
    """
    
    # Get cell locations once!
    if cell_locs == None:
        cell_locs = get_all_cells_tensor(game['dimensions'], game['board'])    
    
    # If game is over or won or cell has been revealed already do nothing
    if game['state'] == 'defeat' or game['state'] == 'victory' or get_cell_value_tensor(game['mask'], coordinates): 
        return 0


    update_cell_value_tensor(game['mask'], coordinates, True)
    revealed = 1

    
    # Base Case: If cell has a value other that zero (number or bomb)
    if get_cell_value_tensor(game['board'], coordinates) == '.': 
        game['state'] = 'defeat'
        return revealed
    
    # Recursive Case: If cell has a value zero
    if get_cell_value_tensor(game['board'], coordinates) == 0:
        
        neighbors = get_neighbors_tensor(game['dimensions'], coordinates)
        for n in neighbors:
            revealed += dig_nd(game, n, cell_locs)

    # Check for victory 
    if is_won(game['board'], game['mask'], cell_locs):
        game['state'] = 'victory'
 
    return revealed


def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares
    neighboring bombs).  The mask indicates which squares should be
    visible.  If xray is True (the default is False), the mask is ignored
    and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    the mask

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [True, True], [True, True]],
    ...               [[False, False], [False, False], [True, True], [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """

    # Get all cell locations
    cell_locs = get_all_cells_tensor(game['dimensions'], game['board'])
    
    # Initialize render baord with 0s
    render = initialize_tensor_board(game['dimensions'], 0)
    
    
    for c in cell_locs:
        # If xray, show board values
        if xray:
            update_render_value_tensor(render, c, get_cell_value_tensor(game['board'], c))
        else:
            if get_cell_value_tensor(game['mask'], c) == False:
                update_render_value_tensor(render, c, '_') 
                
            else:
                cell_value = get_cell_value_tensor(game['board'], c)
                
                # Hide 0s with spaces
                if cell_value == 0:
                    update_render_value_tensor(render, c, ' ') 
                else:
                    update_render_value_tensor(render, c, cell_value) 

    return render   


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    #doctest.testmod(optionflags=_doctest_flags) #runs ALL doctests
    #doctest.run_docstring_examples(render_2d, globals(), optionflags=_doctest_flags, verbose=False)

#    doctest.run_docstring_examples(new_game_2d, globals(), optionflags=_doctest_flags, verbose=True)
#    doctest.run_docstring_examples(dig_2d, globals(), optionflags=_doctest_flags, verbose=True)
#    doctest.run_docstring_examples(dig_nd, globals(), optionflags=_doctest_flags, verbose=False)
#    doctest.run_docstring_examples(render_nd, globals(), optionflags=_doctest_flags, verbose=False)
  #######################################################
    
    ####  Test 1: Testing render_ascii ####
    
#    game = {'dimensions': (2, 4),
#                         'state': 'ongoing',
#                         'board': [['.', 3, 1, 0],
#                                   ['.', '.', 1, 0]],
#                         'mask':  [[True, True, True, False],
#                                   [False, False, True, False]]}
#    print(render_ascii(game, xray=False))
    
  #######################################################
    
    ####  Test 2: Testing 2d board and mask initializers #### 
    
#    print(initialize_2d_board(2, 4))
#    print(initialize_2d_mask(2, 4))    
    
  #######################################################
    
    ####  Test 3: Testing get_neighbors_2d #### 
    
#    bomb = (0,0)
#    rows, cols = (2, 4)
#    print(get_neighbors_2d(rows, cols, bomb))
    
  #######################################################
    
    ####  Test 4: Testing get_all_cells_2d #### 
      
#    num_rows = 2
#    num_cols = 4
#    print(get_all_cells_2d(num_rows, num_cols))
    
  #######################################################

    ####  Test 5: Testing get_neighbors_tensor ####  
     
#    print(get_neighbors_tensor((2, 4), (0,0)))
    
  #######################################################

    ####  Test 6: Testing get_all_cells_tensor ####  
    
#    board = [['.', 3, 1, 0], ['.', '.', 1, 0]]
#    print(get_all_cells_tensor((2, 2), board))
    
  #######################################################
    
    


  


