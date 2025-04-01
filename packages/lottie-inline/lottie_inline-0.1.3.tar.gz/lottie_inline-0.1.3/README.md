# Lottie Inline Tool

A simple tool to inline images in Lottie JSON files.

## Installation

```bash
$ pip install lottie-inline
```
## Usage

Basic usage:

```bash
$ lottie-inline /path/to/input-lottie-file.json /path/to/output-lottie-file.json
```

Limit the size of the images to be inlined to 100KB:

```bash
$ lottie-inline /path/to/input-lottie-file.json /path/to/output-lottie-file.json --max-size=100
```

## Details

The tool will inline all images in the Lottie JSON file and save the result to the output file.

transform: 

```json
{
  "assets": [
    {
      "id": "image_0",
      "w": 500,
      "h": 500,
      "u": "images/",
      "p": "image.png",
      "e": 0
    },
  ],
}
```

to: 

```json
{
  "assets": [
    {
      "id": "image_0",
      "w": 500,
      "h": 500,
      "u": "",
      "p": "data:image/png;base64,...",
      "e": 1
    },
  ],
}
```

## License

MIT
