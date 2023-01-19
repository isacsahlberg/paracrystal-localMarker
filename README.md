
### Averaging a local topological marker

For more details, see the paper arXiv:

In theoretical condensed matter physics, it is sometimes useful to calculate a local topological marker representing e.g. a Chern number, for a finite lattice. The average of this marker corresponds to the true topological index. For _non-crystalline_ systems, there exists substantial variation in the surroundings for each lattice point, and the local markers therefore also have significant fluctuations. Furthermore, the sum of the local Chern marker over the entire finite system gives zero, and this is seen in the borders behaving "erratically." Thus, to evaluate the topological index, it is useful to only consider bulk points. In practice, we exclude a finite-width border, and only take into account the inner points of the system.

But many neighboring points may have correlated values, and so averaging a local marker over all points may not be so useful. The set of points makes up the _distribution_ of local marker values, and calculating all of them can be computationally very costly. Here we show that _randomly_ choosing a set of points from the bulk is a good way to sample this distribution of local values. Repeating this over several random configurations very quickly converges to the mean value that we are after.


Running 
```bash
$ python plot_subDistr.py
```
produces and saves the figure _**bulkHeart-vs-points_L40.png**_ here below.

!---[image](bulkHeart-vs-points_L40.png)

In **a**, we show the local marker calculated ~~for all of the~~— I mean for _most_ of bulk points, and they show characteristic fluctuations. In **b**, we sample the marker at random points within the red boundary which defines the bulk.
For only 1 configuration, the distributions are not of very high quality, as seen in **c**, and the few random points certainly do not make up a good final result. The average local marker for both the random points (in red [CHANGE THESE]) and the bulk points (in black) are decent, but clearly deviate from the true value 1. But repeating this process for N=10 configurations means we are getting closer to the true distribution of values, and that gives us **d**, where all calculated values have been included. In (black), we show all bulk points — not just the heart :) — and see that the distributions match very well, including predicting almost exactly the same mean value for the Chern number.


### Notes:
- The language of the data set itself (i.e. the output) is Finnish
- The yle website doesn't have data for all days of the year, only 1-2 days backwards, and a handful of days forward.
- One "day" typically runs from 6AM to 6AM
- Due to the html data used being so un-clean and varied, it's kind of hopeless to try and even separate composer vs. piece... 😒
- Sometimes, parts of the day's program is missing from the page we use, even if it is available elsewhere. Maybe one day we'll switch over to that other page if it seems like a good idea, but for now, ```¯\_(ツ)_/¯```
- Requires ```python3```, only non-standard package is ```termcolor```



### License

MIT