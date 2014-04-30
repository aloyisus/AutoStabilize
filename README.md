AutoStabilize
=============

using SIFT to automatically detect and track features in a video and use them to transform the image to effect a 2D stabilization

This was an experiment with openCV I did a while back, to explore automatic detection of interesting features and the tracking of those features through a video sequence. The 2d tracks are then used to transform the image to effect a 'stabilize', with no manual intervention.

SIFT is a great algorithm for scale invariant feature detection which was invented by David Lowe. It is described in this paper http://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf which is extremely readable.

![alt tag](https://raw.github.com/aloyisus/AutoStabilize/resize.gif)
