# The Atlas Project 📖
A specialized system that allows users to create an effective atlas system with Raylib-py! With the help of Python, Raylib-py and coffee, this simple module can help you optimize your game by reducing draw calls.

## How to use 🚀
### 1. Installing:
   - Install it with pip: `pip install the-atlas-project`

### 2. Importing:
- Import it to your project
```python
# Import the AtlasReader class
from the_atlas_project import AtlasReader
```

### 3. Instance Creation
- Create an instance of the class and pass in the file name of your JSON Atlas properties (e.g. 'atlas.json')
```python
# Create an instance of the AtlastReader class with it's respective arguments
atlas = AtlasReader("atlas.json")
```


- **Note: The atlas properties file must follow this syntax in order to properly recognize the assets:**
```json
{
  "atlas": "assets/atlas.jpg",
  "entries": {
    "sprite1": {
      "x": 0,
      "y": 0,
      "w": 16,
      "h": 16
    },
    "sprite2": {
      "x": 17,
      "y": 0,
      "w": 16,
      "h": 16
    }
  }
}
```
- **Explanation:**
  - `atlas` is the name of your atlas picture.
  - `entries` are where your sprite entries reside. You must put your sprite entries within here.
  - `sprite1` and `sprite2` are custom names that you must assign in order to properly get use it in `draw_sprite()` later.
  - `x`, `y`, `w` and `h` correspond to x position, y position, width, and height respectively. This is important because this is how the module can actually find the texture.

### 4. Drawing:
- Finally draw the sprite with the `draw_sprite()` function and pass in the name of your sprite, corresponding to the atlas.json file, while also passing the x and y positions of where you want to place your sprite.
- Optionally, you can pass scaling arguments to scale your sprite with type float. The default scaling factor is 1.0
``` python
# Draw the sprite
atlas.draw_sprite("sprite2", 20, 20, scalex=5.0, scaley=5.0)
```

### 5. Unloading
- Ensure to unload the atlas after use with the `unload()` function. This ensure that no memory leaks can happen.
```python
atlas.unload()
```
