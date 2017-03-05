# Mullet
Mullet provides a library of functions which can be iterated over using json configuration files.

Use cases include:
* Setting up a new computer by automatically:
  * installing a list of packages;
  * cloning git repositories;
  * copying files across, with stored permissions and ownership; and
  * importing keys.
* Syncronising a remote FLAC, WAV and ZIP music collection with a local mp3 collection.
* Copying files to or from a remote location.
* Maintaining a hosts file, with different sources.
* Dynamically merging and processing data, such as proding png financial overview graphs from different sources of downloaded financial statements.

Usage: python3 ./mullet.py myConf.json
