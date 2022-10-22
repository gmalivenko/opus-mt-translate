# opus-mt-translate

A wrapper for [Helsinki-NLP/Opus-MT](https://github.com/Helsinki-NLP/Opus-MT) models to translate texts with bash pipes.

## Installation

```
pip install git+https://github.com/gmalivenko/opus-mt-translate
```


## Usage

```
opus-mt-translate [-h] [--device DEVICE] [--batch_size BATCH_SIZE]
                    [--beam_size BEAM_SIZE] [-s SRC_LANG]
                    [-t TARGET_LANG]
                    [src_lang] [target_lang]
```

### Translate single line

```
$ echo 'A text to translate' | opus-mt-translate en ru
Текст для перевода
```

### Translate a whole text file

```
$ cat input.txt | opus-mt-translate en ru
...

```

### Translate a whole text file

```
$ cat input.txt | opus-mt-translate en ru > result.txt
...

```

### Translate using cpu / gpu

The `--device` argument corresponds to the PyTorch device selection. It may be 'cpu', 'cuda', 'cuda:1', etc.


## License

The wrapper is covered by MIT license.

To get models legal information, please follow corresponding link format: 
https://huggingface.co/Helsinki-NLP/opus-mt-ru-en
where 'ru' and 'en' should be replaces with 'source_lang' and 'target_lang' you want to use.