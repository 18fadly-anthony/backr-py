# Change BackTrack (Branch)

This branch will used be to change backtrack to only store the backup
location.

The number of backups will be determined by the number of entries in the
backtrack file and the whether or not the backups are compressed will be
determined by the presence of ".tar.gz" in the backup location.

This will make backr partially incompatible with previous backups for
that reason I felt it warranted its own branch.
