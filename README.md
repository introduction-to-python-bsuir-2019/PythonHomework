# RSS reader

A utility that is able to convert news received from RSS sources to either human-readable or .JSON format 

## Launching manual

The utility can be called via command-line interface using the 'rssreader' command. For more information on possible arguments run: rssreader -h

## Conflicting arguments

 * None other arguments will have effect on the output if --version is present
 * Using more (or less) than one of the following arguments will cause an error:
  * source 
  * --date 
  * --version
 * Entering a non-positive --limit will cause an error

## Caching details

News are cached in .JSON format, caching is not affected by --limit; related images are saved in .jpg format.
