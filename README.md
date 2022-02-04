![Tests](https://github.com/itsjustmustafa/ALTakeHomeTest2022/actions/workflows/tests.yml/badge.svg?event=push)
![Black](https://github.com/itsjustmustafa/ALTakeHomeTest2022/actions/workflows/autoblack.yml/badge.svg?event=push)

# ALTakeHomeTest2022
The Animal Logic Take Home Test for Mustafa Barodawala

# Documentation
Find documentation ![here](Sphinx-docs/_build/markdown/index.md)

# TODO

- Make the scenes in the dataFileCLIView their own class and objects
- Allow different datatypes for columns in DataFile DataFrames, rather than just string
- Create a class for the display module
  - look at how software such as Photoshop handle plugins, since this is just a display plugin

# Challenges
- **Figuring out how to structure this project**
  - For API and software interaction, used the MVC pattern, for which structuring also proved a challenge
    - Found a few good resources on how MVC is laid out which helped me understand how to approach this better (![An example of a drawing program](http://www.cs.utsa.edu/~cs3443/mvc-example.html))
- **Test dataFile.py without using any external .csv files, to keep the API file-type-agnostic**
  - Created an abstract class DataFileIO from which I can extent any serialization
  - Used MagicMock from unittest to create mock implementations of uninplementated DataFileIO methods
- **Managing scenes**
  - Took advantage of how Python treats methods as their own objects, and was therefore able to implement scenes as functions, but still treat them similar to objects
- **Handling sourcing the displays**
  - Similar to above, took advantage of how Python treats modules as their own objects, and was therefore able to pass around modules containing methods for displaying DataFile

This is how I diagrammed out the scenes:

![scene_diagram.jpg](https://raw.githubusercontent.com/itsjustmustafa/ALTakeHomeTest2022/main/scene_diagram.jpg)
