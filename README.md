# Connect Four

Terminal-based version of the classic game of connecting four.

Play against one of the bots, or pit two of the bots against each other and find out which strategies are strongest.

## Issues

1. There is some sort of bug in at least some of the bots. For example, `InARowAllowBlanksBot` had two choices at the end, where it could either tie or lose, and it chose the losing move. Possible it has to do with behavior near the end of the game (within `maxDepth` turns of filling up the whole board).
