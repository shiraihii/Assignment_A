# Mirrors and Lasers

Code Assignment of Ascent Robotics  
Author: Lyu Zheming

## Problem Solution

To solve the position of available mirrors that make the safe open.

First, we assume a virtual light beam start from the laser emitter, called as **_forward light_**. When the **_forward light_** reaches any mirrors, it reflects during the mirror's orientation (_polarity_). Do this until the light beam reaches the boundary (_wall_) of map.

Secondly, we assume a virtual light beam start from the laser detector (_receiver_) called as **_backward light_**, according to principle of light reversibility. Do the same process.

After that, a cross point (_intersection_) between **_forward light_** and **_backward light_** is an available solution. Since _A position where both a / and a \ mirror open the safe counts just once._, we don't have to consider the light's direction.

So, we just count the number of such _intersection_ and output the best solution that has the _smallest row / column position_.

Separately from that, if the **_forward light_** finally reached the _receiver_'s position during _forwarding search_, that means the safe-system opens without inserting a mirror, we just output 0.

And if there are no mirrors, the only available case is the number of row's is exactlly 1.

## Files

-   mirrors.py  
    This program is a prototype for verification
    of this problem.

    I used the sparse matrix to store mirror's arrangement and light beam.  
    Mirror's arrangement matrix is same size of given safe-map, which's entries range in [-1(_backslash mirror_), 0(_empty_), 1(_slash mirror_)].
    Light Beam is calculated step by step.  
    _Forward Light Beam_ and _Backward Light Beam_ are stored in separated matrices, which's entries range in [0(_no light_), 1(_light exists_)].  
    To get the final solution, I added 2 matrices and judge the number of '2' in the summation.

*   mirrors_fast.py  
    mirrors.py calculated light beam step by step and store mirrors and light beam in matrix, causing it becomes insufferable slow when numbers of row and column become large.

    In this program, I realized compress sparse matrix in row(_mat_csr_) and column(_mat_csc_) from sketch, which allows indexing next mirror's position in O(log n).  
    That is by a _find_next_mirror_ code below:

    -   Given the light beam's direction and current mirrors's position.
    -   Find the index in _mat_csr_/_mat_csc_ for current mirror's position
    -   Increase/decrease the found index based on light direction
    -   Check boundary condiction and return next position with next light direction

    For this procedure, this laser emitter and laser detector are added as 2 virtual mirrors, as _find_next_mirror_ assumes there must be a mirror in the start position.

    For light beam storing, I used a sorted list for horizontal and vertical beams.  
    Also, to get solution a just search intersection in range of possible indices.

*   gen_testcase.py  
    This file is for generating a large scale testcase.

## Usage

### Dependence

-   python >= 3.6
-   numpy
    -             pip install numpy

### Command

    python mirros_fast.py testcase.txt
